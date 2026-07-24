from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission


@receiver(post_migrate)
def create_roles(sender, **kwargs):

    #ROLE PERMISSIONS ARE PENDING DATABASE SETUP 
    roles = {
        "HR": [],
        "Manager": [],
        "Employee": [],
    }

    for role_name, perms in roles.items(): 
        group, created = Group.objects.get_or_create(name=role_name) #Creates the role in the 


        for perm_codename in perms:
            try:
                perm = Permission.objects.get(codename=perm_codename) #gets the codenames for the permissions
                group.permissions.add(perm) #adds the perimssions to the new group created

            except Permission.DoesNotExist: #Ensures this doesn't error on first migration
                pass