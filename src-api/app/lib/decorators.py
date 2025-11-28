import random
import redis.exceptions
import threading
import time
from collections import deque
from functools import wraps
from loguru import logger


class ThrottleException(Exception):
    """Raised when throttling limit is hit, and we choose not to wait."""
    pass


# Global throttle registry: key -> (lock, deque)
_throttle_registry = {}
_registry_lock = threading.Lock()


class registry:
    _redis_client = None

    @classmethod
    def get_redis_client(cls):
        """Returns a connected Redis client instance."""
        if cls._redis_client is None:
            # Example: Replace with your actual connection logic
            import redis
            from app import redis as redis_client

            try:
                cls._redis_client = redis_client
                # Verify connection
                cls._redis_client.ping()
            except redis.exceptions.ConnectionError:
                logger.error("Failed to connect to Redis. Throttling will not work correctly.")
                raise
        return cls._redis_client


def throttle(
        calls: int,
        period: float,
        *,
        mode = 'sleep',
        key = None,
        backoff_strategy = 'fixed',  # 'fixed' or 'exponential'
        backoff_base: float = 1.0,  # base seconds for backoff
        backoff_cap: float = 60.0,  # max seconds for backoff
        jitter = False  # True = apply random jitter
):
    """
    Throttle with backoff support.

    Args:
        calls: Max calls in period
        period: Time window (s)
        mode: 'sleep' or 'raise'
        key: group key or key function
        backoff_strategy: 'fixed' or 'exponential'
        backoff_base: base backoff seconds
        backoff_cap: max backoff seconds
        jitter: add random 0-1s to backoff if True
    """

    def decorator(func):
        group_key = key or f"{func.__module__}.{func.__qualname__}"

        @wraps(func)
        def wrapper(*args, **kwargs):
            import random
            from loguru import logger

            resolved_key = group_key(args, kwargs) if callable(group_key) else group_key

            while True:
                now = time.monotonic()
                wait = 0  # Initialize wait time

                with _registry_lock:
                    if resolved_key not in _throttle_registry:
                        _throttle_registry[resolved_key] = (threading.Lock(), deque(), 0)

                    lock, history, current_attempt = _throttle_registry[resolved_key]

                    with lock:
                        # 1. Clean up old history
                        while history and (now - history[0]) > period:
                            history.popleft()

                        # 2. Check if we are clear to call the function
                        if len(history) < calls:
                            history.append(now)
                            _throttle_registry[resolved_key] = (lock, history, 0)
                            break  # Exit while loop to run func
                        else:
                            # 3. Throttled: calculate backoff logic (while loop continues after sleep)
                            if mode == 'raise':
                                raise ThrottleException(
                                    f"Exceeded {calls} calls in {period}s for key '{resolved_key}'.")

                            elif mode == 'sleep':

                                # --- Tweak: Calculate MINIMUM required wait time ---
                                # The wait time must be at least long enough for the oldest entry to expire.
                                time_until_first_clears = period - (now - history[0])

                                # Calculate the base backoff time
                                if backoff_strategy == 'fixed':
                                    base_wait_calculated = backoff_base
                                elif backoff_strategy == 'exponential':
                                    base_wait_calculated = min(float(backoff_base) * (2 ** current_attempt),
                                                               backoff_cap)
                                else:
                                    raise ValueError(f'Unknown backoff_strategy: {backoff_strategy}')

                                # Use the GREATER of the base backoff OR the minimum required time to clear the window
                                wait = max(base_wait_calculated, time_until_first_clears)

                                if jitter:
                                    wait += random.uniform(0, 1)

                                # Increment the attempt counter *in the registry* for the next loop iteration
                                new_attempt = current_attempt + 1
                                _throttle_registry[resolved_key] = (lock, history, new_attempt)

                                logger.warning(
                                    f'[{resolved_key}] Backing off for {wait:.2f}s (attempt {new_attempt}, min_to_clear: {time_until_first_clears:.2f}s)')

                                # Locks must be released before sleeping

                # Sleep happens outside any lock context
                time.sleep(wait)
                # Loop restarts, re-acquires locks, and re-evaluates the throttle condition

                # Only reached via 'break'
            return func(*args, **kwargs)

        return wrapper

    return decorator


def throttle_burst(
        max_tokens: int,
        refill_rate: float,
        *,
        mode='sleep',
        key=None,
        backoff_strategy='fixed',
        backoff_base=1.0,
        backoff_cap=60.0,
        jitter=False
):
    """
    Throttle decorator with burst, backoff, shared key.

    Args:
        max_tokens: burst capacity
        refill_rate: tokens per second
        mode: 'sleep' or 'raise'
        key: shared group key or key function
        backoff_strategy: 'fixed' or 'exponential'
        backoff_base: base backoff seconds
        backoff_cap: max backoff seconds
        jitter: add random jitter if True
    """

    def decorator(func):
        group_key = key or f"{func.__module__}.{func.__qualname__}"
        backoff_state = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            import random
            from loguru import logger

            resolved_key = group_key(args, kwargs) if callable(group_key) else group_key

            with _registry_lock:
                if resolved_key not in _throttle_registry:
                    _throttle_registry[resolved_key] = {
                        'lock': threading.Lock(),
                        'tokens': max_tokens,
                        'last_refill': time.monotonic()
                    }
                state = _throttle_registry[resolved_key]

            while True:
                with state['lock']:
                    now = time.monotonic()
                    elapsed = now - state['last_refill']
                    refill = elapsed * refill_rate
                    if refill > 0:
                        state['tokens'] = min(max_tokens, state['tokens'] + refill)
                        state['last_refill'] = now

                    if state['tokens'] >= 1:
                        state['tokens'] -= 1
                        backoff_state[resolved_key] = 0
                        return func(*args, **kwargs)
                    else:
                        # Apply backoff
                        attempt = backoff_state.get(resolved_key, 0)
                        if mode == 'raise':
                            raise ThrottleException(f"Throttled: {resolved_key}")
                        elif mode == 'sleep':
                            if backoff_strategy == 'fixed':
                                wait = backoff_base
                            elif backoff_strategy == 'exponential':
                                wait = min(backoff_base * (2 ** attempt), backoff_cap)
                            else:
                                raise ValueError(f'Unknown backoff_strategy: {backoff_strategy}')

                            if jitter:
                                wait += random.uniform(0, 1)

                            logger.warning(f'[{resolved_key}] Backing off for {wait:.2f}s (attempt {attempt + 1})')
                            backoff_state[resolved_key] = attempt + 1
                            time.sleep(wait)
                        else:
                            raise ValueError(f"Unknown mode: {mode}")

        return wrapper

    return decorator


def redis_throttle(
        calls: int,
        period: float,
        *,
        mode='sleep',
        backoff_strategy='fixed',  # 'fixed' or 'exponential'
        backoff_base: float = 1.0,  # base seconds for backoff
        backoff_cap: float = 60.0,  # max seconds for backoff
        jitter=False,  # True = apply random jitter
        key=None,
):
    """
    A throttling decorator that uses Redis for cross-process/thread synchronization.

    Throttle with backoff support.

    Args:
        calls: Max calls in period
        period: Time window (s)
        mode: 'sleep' or 'raise'
        backoff_strategy: 'fixed' or 'exponential'
        backoff_base: base backoff seconds
        backoff_cap: max backoff seconds
        jitter: add random 0-1s to backoff if True
        key: group key or key function
    """

    # Define Redis keys structure
    HISTORY_KEY_PREFIX = "throttle:history:"
    ATTEMPT_KEY_PREFIX = "throttle:attempts:"

    def decorator(func):
        # Default group key
        group_key = key or f"{func.__module__}.{func.__qualname__}"

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get the Redis client
            r = registry.get_redis_client()

            # Resolve the dynamic key if necessary
            resolved_key = group_key(args, kwargs) if callable(group_key) else group_key

            # Specific keys for this function call
            history_key = HISTORY_KEY_PREFIX + resolved_key
            attempts_key = ATTEMPT_KEY_PREFIX + resolved_key

            while True:
                # Use server time from Redis for consistency across processes
                now = r.time()[0]
                wait = 0

                # Use a Redis pipeline/transaction for atomic operations within the while loop iteration
                with r.pipeline() as pipe:
                    try:
                        pipe.watch(history_key, attempts_key)

                        # 1. Clean up old history and get current count
                        # Use ZREMRANGEBYSCORE to remove timestamps older than (now - period)
                        min_score_to_keep = now - period
                        pipe.zremrangebyscore(history_key, 0, min_score_to_keep)

                        # Get current number of calls remaining in the window
                        current_calls = pipe.zcard(history_key)

                        # Get the current attempt count (for backoff calculation)
                        current_attempt_str = pipe.get(attempts_key)
                        current_attempt = int(current_attempt_str) if current_attempt_str else 0

                        # 2. Check if we are clear to call the function
                        if current_calls < calls:
                            # Use MULTI/EXEC block for atomic update
                            pipe.multi()
                            # Add the current timestamp to the sorted set (score=timestamp, member=unique_id)
                            # Using 'now' as member is problematic if multiple calls happen in the same second.
                            # Use a UUID or an index, but for simplicity here we assume time precision is enough
                            # Or better, just use ZADD if Redis version >= 6.2 supports ZADD NX/CH

                            # Simple ZADD with a unique member (e.g., now.timestamp + random)
                            member_id = f"{now}:{random.random()}"
                            pipe.zadd(history_key, {member_id: now})

                            # Set the key to expire to prevent indefinite growth if the application stops
                            pipe.expire(history_key, int(period + 5))  # Set TTL slightly longer than the period

                            # Reset attempts counter on success
                            pipe.delete(attempts_key)

                            # Execute the pipeline
                            pipe.execute()
                            break  # Exit while loop to run func

                        else:
                            # 3. Throttled: calculate backoff logic (while loop continues after sleep)
                            if mode == 'raise':
                                raise ThrottleException(
                                    f"Exceeded {calls} calls in {period}s for key '{resolved_key}'.")

                            elif mode == 'sleep':
                                # Time until the oldest entry clears
                                # We need the score of the oldest entry, which is the first one in the sorted set
                                # ZRANGE returns members, we need ZRANGE with WITHSCORES to get the time back
                                # The above pipeline didn't fetch the oldest time explicitly. Let's adjust the logic slightly

                                # We can rely on ZREMRANGEBYSCORE keeping the set minimal.
                                # To get the oldest time without another call, we'd need a more complex WATCH/MULTI block
                                # Let's assume we can get it in a separate step if we fail the 'if current_calls < calls' check

                                # Exit pipeline context temporarily to get the oldest time reliably if throttled
                                pass

                    except redis.exceptions.WatchError:
                        # If the key was modified by another client during our watch, restart the while loop iteration
                        logger.warning(f"WatchError on key {resolved_key}. Retrying throttle check.")
                        continue  # continue the while loop

                # Logic that happens OUTSIDE the Redis WATCH/MULTI block but still within the while True loop (if throttled)
                if current_calls >= calls and mode == 'sleep':
                    # We need the timestamp of the *oldest* item currently in the list to calculate time_until_first_clears
                    # Since we are outside the atomic block, we run one more redis command.
                    # This is safe because even if it changes, our calculation will lead to a 'sleep' that ends up re-evaluating correctly.
                    oldest_entry = r.zrange(history_key, 0, 0, withscores=True)
                    if oldest_entry:
                        oldest_time = oldest_entry[0][1]  # (member_id, timestamp)
                        time_until_first_clears = period - (now - oldest_time)
                        if time_until_first_clears < 0: time_until_first_clears = 0  # Safety check

                        if backoff_strategy == 'fixed':
                            base_wait_calculated = backoff_base
                        elif backoff_strategy == 'exponential':
                            base_wait_calculated = min(float(backoff_base) * (2 ** current_attempt), backoff_cap)
                        else:
                            raise ValueError(f'Unknown backoff_strategy: {backoff_strategy}')

                        wait = max(base_wait_calculated, time_until_first_clears)

                        if jitter:
                            wait += random.uniform(0, 1)

                        # Increment the attempt counter *in Redis* for the next loop iteration
                        # Use INCR for atomicity
                        new_attempt = r.incr(attempts_key)
                        # Set a TTL for the attempt counter just in case
                        r.expire(attempts_key, int(max(wait, period) + 5))

                        logger.warning(
                            f'[{resolved_key}] Backing off for {wait:.2f}s (attempt {new_attempt}, min_to_clear: {time_until_first_clears:.2f}s)')

                        # Sleep happens outside any Redis interaction
                        time.sleep(wait)
                        # Loop restarts, fetches new time, and re-evaluates
                    else:
                        # Should theoretically not happen if zcard >= calls, but as a safeguard:
                        time.sleep(1)
                        continue

            # Only reached via the 'break' statement in the success path
            return func(*args, **kwargs)

        return wrapper

    return decorator


def redis_cache(expire: int = 300, prefix: str = "cache"):
    """
    Decorator to cache function results in Redis.

    Args:
        expire (int): Cache expiration time in seconds (default 300).
        prefix (str): Optional prefix for cache keys.
    """

    def decorator(func):
        from functools import wraps

        @wraps(func)
        def wrapper(*args, **kwargs):
            import hashlib, json, pickle
            from pickle import PickleError, UnpicklingError
            from app import redis

            if len(args) > 0:
                first_arg = args[0]
                if hasattr(first_arg, '__class__'):
                    args_to_cache = args[1:]
                else:
                    args_to_cache = args
            else:
                args_to_cache = args

            # Build a unique cache key
            key_data = {
                'func': f"{func.__module__}.{func.__qualname__}",
                'args': args_to_cache,
                'kwargs': kwargs
            }
            key_str = json.dumps(key_data, sort_keys=True, default=str)
            key_hash = hashlib.sha256(key_str.encode()).hexdigest()
            redis_key = f"{prefix}:{key_hash}"

            # Try to get from cache
            try:
                cached = redis.get(redis_key)
                if cached is not None:
                    return pickle.loads(cached)
            except (PickleError, UnpicklingError):
                pass

            # Call the actual function
            result = func(*args, **kwargs)

            # Cache the result (must be JSON-serializable)
            try:
                redis.setex(redis_key, expire, pickle.dumps(result))
            except Exception:
                pass

            return result

        return wrapper

    return decorator
