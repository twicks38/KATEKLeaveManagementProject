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
            'add_userprofile',
            'change_userprofile',
            'delete_userprofile',
            'view_userprofile',
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
            'view_userprofile',
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
            'view_userprofile',
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
                perm = Permission.objects.get(codename=perm_codename) #gets the codenames for the permissions
                group.permissions.add(perm) #adds the perimssions to the new group created

            except Permission.DoesNotExist: #Ensures this doesn't error on first migration
                pass