from loguru import logger
from queue import Queue
from threading import Event, Thread
from typing import Any
from app.lib.config.services import ServicesConfig


class ZabbixMetric:
    host: str = None
    key: str
    value: Any
    clock: int
    ns: int

    def __init__(self, key: str, value: Any, host: str = None):
        self.host = host
        self.key = key
        self.value = value
        self.set_timestamp()

    def __str__(self):
        return f'{self.host}:{self.key}:{self.value}'

    def set_timestamp(self, timestamp: int = None):
        import time

        if timestamp is None:
            timestamp = time.time_ns()

        self.clock = timestamp // 1_000_000_000
        self.ns = timestamp % 1_000_000_000

    def to_json(self):
        return {
            'host': self.host,
            'key': self.key,
            'value': self.value,
            'clock': self.clock,
            'ns': self.ns,
        }


class ZabbixSender:
    _config: ServicesConfig.ZabbixConfig

    def __init__(self, config: ServicesConfig.ZabbixConfig):
        self._config = config

    def send(self, metrics: list[ZabbixMetric]) -> str:
        """Send the given list of metrics to the Zabbix server."""
        import json, socket, struct

        if not self._config.reporter_enabled:
            return 'Reporter disabled by configuration.'

        if not self._config.sender_enabled:
            return 'Sender disabled by configuration.'

        payload = {
            'request': 'sender data',
            'data': [m.to_json() for m in metrics],
        }
        data = json.dumps(payload).encode('utf-8')
        header = b'ZBXD\x01' + struct.pack('<Q', len(data))
        packet = header + data

        with socket.create_connection((self._config.hostname, self._config.port)) as s:
            s.sendall(packet)
            response_header = s.recv(13)
            response_len = struct.unpack('<Q', response_header[5:])[0]
            response_body = s.recv(response_len)
            response_text = response_body.decode('utf-8')

        return response_text


class ZabbixReporter:
    _config: ServicesConfig.ZabbixConfig
    _queue: Queue
    _stop_event: Event
    _thread: Thread

    def __init__(self, config: ServicesConfig.ZabbixConfig):
        self._config = config
        self._queue = Queue()
        self._stop_event = Event()
        self._thread = Thread(target=self._worker, daemon=True)

    def start(self):
        """Start the background worker thread."""
        if self._config.reporter_enabled and not self._thread.is_alive():
            self._thread.start()

    def stop(self):
        """Signal the worker thread to stop and wait for it."""
        self._stop_event.set()
        if self._thread.is_alive():
            self._thread.join(timeout=5)

    async def stop_async(self):
        """Signal the worker thread to stop and wait for it asynchronously."""
        import asyncio
        self._stop_event.set()
        if self._thread.is_alive():
            await asyncio.to_thread(self._thread.join)

    def report(self, metrics: list[ZabbixMetric]):
        """Add the given list of metrics to the Zabbix send queue."""
        for metric in metrics:
            if metric.host is None:
                metric.host = self._config.default_node_name
            metric.set_timestamp()
            self._queue.put(metric)

    def _worker(self):
        """Background thread that flushes metrics periodically."""
        sender = ZabbixSender(self._config)

        while not self._stop_event.is_set() or not self._queue.empty():
            batch: list[ZabbixMetric] = []

            try:
                while not self._queue.empty():
                    batch.append(self._queue.get_nowait())

                if batch:
                    batch_str = [f'{m}' for m in batch]
                    logger.debug(f'[ZabbixReporter] Sending {len(batch)} metrics: {batch_str}')
                    result = sender.send(batch)
                    logger.debug(f'[ZabbixReporter] Sent {len(batch)} metrics: {result}')

            except Exception as e:
                logger.error(f'[ZabbixReporter] Error sending metrics to Zabbix server: {e}')

            # Pause before next batch
            self._stop_event.wait(self._config.send_interval)
