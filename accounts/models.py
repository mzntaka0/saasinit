import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models, transaction
from django.db.models.signals import post_save
from django.contrib.auth.base_user import BaseUserManager

import factory


class TenantManager(models.Manager):
    """Manager for the Tenant model. Also handles the account creation"""

    @transaction.atomic
    def create_account(self, tenant_name, username, password, tenant_address=None):
        """Creates a Tenant along with the User and returns them both"""

        tenant = Tenant(
            name=tenant_name,
            address=tenant_address,
        )
        tenant.save()

        user = User.objects.create_user(
            tenant=tenant,
            username=username,
            password=password,
        )

        return tenant, user

    @transaction.atomic
    def create_superuser(self, tenant, username, password, tenant_address=None):
        if None in [tenant, username, password]:
            raise TypeError('Superusers must have a password.')

        tenant, user = self.create_account(tenant, username, password, tenant_address)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        tenant.is_superuser = True
        tenant.is_staff = True
        tenant.save()
        return tenant, user


class Tenant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('name', max_length=100, unique=True)
    address = models.CharField('address', max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = TenantManager()

    class Meta:
        db_table = 'tenants'

    def __str__(self):
        return self.name


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, related_name='%(class)s', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f'({self.tenant.name}) - {self.username}'


class TenantRelatedModel(models.Model):
    """Abstract class used by models that belong to a Company"""

    # TODO: if this id is defined here, isn't each id in certain field needed?? -> may not be needed.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey('accounts.Tenant', related_name='%(class)s', on_delete=models.PROTECT, editable=False)

    class Meta:
        abstract = True


class UserWithTenant(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    username = 't.mizuno'


class TenantWithUser(factory.django.DjangoModelFactory):

    class Meta:
        model = Tenant

    name = 'AI-dea Inc.'
    address = 'Ginza5-9-16'
    relatedtenant = factory.RelatedFactory(UserWithTenant, 'tenant')
