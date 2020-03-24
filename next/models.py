import uuid
from typing import List, Tuple, Dict, Optional
import json

import jsonfield
from django.db import models, transaction
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.conf import settings

from . import consts
from . import utils
from accounts.models import TenantRelatedModel


User = get_user_model()


#class TenantProfile(models.Model):
#    PLAN_TYPE = consts.PLAN_TYPE
#
#    tenant = models.OneToOneField('accounts.Tenant', on_delete=models.CASCADE)
#    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
#    # TODO: Is this needed?
#    plan = models.CharField(choices=PLAN_TYPE, max_length=20, verbose_name='Plan Type')
#
#    def __str__(self):
#        return self.tenant.name
#
#
#def tenantprofile_receiver(sender, instance, created, *args, **kwargs):
#    if created:
#        tenantprofile = TenantProfile.objects.create(tenant=instance)
#        return tenantprofile


class Document(TenantRelatedModel):
    DOCUMENT_TYPE = [
        ("invoice", "Invoice"),
        ("bill", "Bill"),
        ("receipt", "Receipt"),
        ("businesscard", "Business Card"),
        ("contract", "Contract"),
    ]

    name = models.CharField(max_length=100, verbose_name='Document Name')
    document_type = models.CharField(choices=DOCUMENT_TYPE, max_length=20, verbose_name='Document Type')
    document_content = jsonfield.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'next_documents'

    def __str__(self):
        return f'({self.tenant.name}) - [{self.document_type}] {self.name}'


class Membership(TenantRelatedModel):
    ACCESS = [
        ("R", "READ_ONLY"),
        ("W", "READ_WRITE"),
        ("X", "ADMIN")
    ]

    class Meta:
        db_table = 'next_memberships'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access = models.CharField(choices=ACCESS, max_length=1)


class UserClient(TenantRelatedModel):
    client = models.CharField(max_length=100)

    class Meta:
        db_table = 'next_user_clients'
        verbose_name = 'User Client'
        verbose_name_plural = 'User Clients'


class CategoryManager(models.Manager):
    """Manager for the Category model. Also handles the Table creation"""

    @transaction.atomic
    def create_table(self, category_name: str, category_type: str, field_data: List[Dict[str, str]]) -> Tuple:
        """Creates a Tenant along with the User and returns them both"""
        category = Category(
            category_name=category_name,
            category_type=category_type,
        )
        category.save()

        fields = list()
        for fd in field_data:
            field = Field(
                category=category,
                field_num=fd.get('field_num'),
                name=fd.get('name'),
                #is_indexed=fd.get('is_indexed'),
                field_type=fd.get('field_type'),
                default_args=fd.get('default_args'),
                field_args=fd.get('field_args'),
            )
            field.save()
            fields.append(field)

        return category, fields

    def get_fields(self, category_name: str, exclude: List[str] = ['id', 'category', 'field_options']) -> List[List[str]]:
        category_fields = Field.objects.filter(category__name=category_name)
        fields = [[str(getattr(field, field_name.name))
                   for field_name in Field._meta.fields if field_name.name not in exclude]
                  for field in category_fields]
        return fields


# These DB models below are inspired by this site: https://www.publickey1.jp/blog/09/3_2.html
# changed the model name of "Object" -> "Category" (cuz it's a reserved term in Python)
#class Category(models.Model):
class Category(TenantRelatedModel):
    CATEGORY_TYPE = consts.CATEGORY_TYPE

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name='Category Name')
    type = models.CharField(choices=CATEGORY_TYPE, max_length=50, verbose_name='Category Type')

    objects = CategoryManager()

    class Meta:
        db_table = 'next_categories'
        verbose_name_plural = 'Categories'

    def __str__(self):
        fields_ = Category.objects.get_fields(self.name)
        fields = ', '.join('-'.join(f) for f in fields_)
        return f'{self.name} [{self.type}] -- {fields}'


#class Field(models.Model):
class Field(TenantRelatedModel):
    FIELD_TYPE = utils.DRFAbstractInfo.Fields.FIELD_TYPE
    _default_args = {key: str(val) for key, val in utils.DRFAbstractInfo.Fields.default_args.items()}
    DEFAULT_ARGS = json.dumps(_default_args)
    field_args_ = utils.DRFAbstractInfo.Fields.args_  # function object

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True, verbose_name='Field Name')
    field_num = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(500)])
    field_type = models.CharField(choices=FIELD_TYPE, max_length=50, verbose_name='Field Type')
    #is_indexed = models.BooleanField()
    default_args = jsonfield.JSONField(null=True, blank=True, default=DEFAULT_ARGS)
    field_args = jsonfield.JSONField(null=True, blank=True)  # TODO: change default value depending on field_type using field_args_
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'next_fields'

    def __str__(self):
        return f'({self.category.name}) - {self.field_num} - {self.name} - {self.field_type}'


#class Data(models.Model):
class Data(TenantRelatedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    for i in range(501):  # defining var_i column (0 <= i <= 500) '500' might be a magic number
        locals()[f'var_{i}'] = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'next_data'
        verbose_name_plural = 'Data'


# TODO: is sender ok to be user model?
#post_save.connect(tenantprofile_receiver, sender=settings.AUTH_USER_MODEL)
