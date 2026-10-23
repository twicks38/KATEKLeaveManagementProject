class PermissionService:

    @staticmethod
    def is_hr_user(user):
        return (
            user.is_authenticated
            and user.groups.filter(
                name__in=["HR", "HR Superuser"]
            ).exists()
        )

    @staticmethod
    def is_hr_superuser(user):
        return (
            user.is_authenticated
            and user.groups.filter(
                name="HR Superuser"
            ).exists()
        )