from tokenize import group

from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission


@receiver(post_migrate)
def create_roles(sender, **kwargs):

    roles = {
        "HR": [
            'add_team',
            'change_team',
            'delete_team',
            'view_team',
            'add_teammembership',
            'change_teammembership',
            'delete_teammembership',
            'view_teammembership',
            'add_profile',
            'change_profile',
            'delete_profile',
            'view_profile',
            'add_group',
            'change_group',
            'view_group',
            'add_user',
            'change_user',
            'delete_user',
            'view_user',
            'view_auditlog',
            'add_entitlement',
            'change_entitlement',
            'delete_entitlement',
            'view_entitlement',
            'add_leaverequest',
            'change_leaverequest',
            'delete_leaverequest',
            'view_leaverequest',
            'view_notification',
            'add_specialleaverequest',
            'change_specialleaverequest',
            'delete_specialleaverequest',
            'view_specialleaverequest',
        ],

        "Manager": [
            'view_team',
            'view_teammembership',
            'view_profile',
            'view_group',
            'view_user',
            'view_entitlement',
            'add_leaverequest',
            'change_leaverequest',
            'delete_leaverequest',
            'view_leaverequest',
            'view_notification',
            'add_specialleaverequest',
            'change_specialleaverequest',
            'delete_specialleaverequest',
            'view_specialleaverequest',
        ],

        "Employee": [
            'view_team',
            'view_teammembership',
            'view_profile',
            'view_group',
            'view_user',
            'view_entitlement',
            'add_leaverequest',
            'change_leaverequest',
            'delete_leaverequest',
            'view_leaverequest',
            'view_notification',
            'add_specialleaverequest',
            'change_specialleaverequest',
            'delete_specialleaverequest',
            'view_specialleaverequest'
        ],
    }

    for role_name, perms in roles.items(): 
        group, created = Group.objects.get_or_create(name=role_name)

        group.permissions.clear()


        for perm_codename in perms:
            try:
                perms = Permission.objects.filter( #gets the codenames for the permissions
                    codename=perm_codename
                )

                for perm in perms:
                    group.permissions.add(perm) #adds the permissions to the new group created

            except (Permission.DoesNotExist, Permission.MultipleObjectsReturned): #Ensures this doesn't error on first migration
                pass