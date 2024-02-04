from django.contrib.auth.backends import ModelBackend


class EmailOrUsernameModelBackend(ModelBackend):
    """ A Django authentication backend that allows users to log in using their email or username. """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """ Authenticate a user based on email or username. """
        from django.contrib.auth import get_user_model
        from django.db.models import Q

        UserModel = get_user_model()

        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        if username is None or password is None:
            return

        email_field_name = UserModel.get_email_field_name()
        username_field_name = UserModel.USERNAME_FIELD

        # Attempt to authenticate the user by email or username
        try:
            user = UserModel._default_manager.get(
                Q(**{"%s__iexact" % email_field_name: username, "is_active": True})
                | Q(**{"%s__iexact" % username_field_name: username, "is_active": True})
            )
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
