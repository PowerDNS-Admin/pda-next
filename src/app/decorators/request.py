
def verify_user(func):
    """ This decorator is used to verify the user status before allowing access to a view. """

    def wrapper(request, *args, **kwargs):
        from django.shortcuts import redirect, reverse
        from apps.user.models import User

        user: User = request.user

        if user.status == User.STATUS_PENDING_VERIFICATION:
            return redirect(reverse('user:pending-verification'))

        if user.status == User.STATUS_PENDING_APPROVAL:
            return redirect(reverse('user:pending-approval'))

        if user.status == User.STATUS_PENDING_SETUP:
            return redirect(reverse('user:index'))

        if user.status == User.STATUS_INACTIVE:
            return redirect(reverse('user:inactive'))

        if user.status == User.STATUS_LOCKED:
            return redirect(reverse('user:locked'))

        if user.status == User.STATUS_DELETED:
            return redirect(reverse('user:deleted'))

        return func(request, *args, **kwargs)

    return wrapper


def has_account(func):
    """ This decorator is used to verify that the user is linked to at least one account. """

    def wrapper(request, *args, **kwargs):
        from django.shortcuts import redirect, reverse
        from apps.account.models import AccountUser
        from apps.user.models import User

        user: User = request.user

        link: AccountUser = AccountUser.objects.filter(user=user).first()

        if link is None:
            return redirect(reverse('account:start'))

        return func(request, *args, **kwargs)

    return wrapper
