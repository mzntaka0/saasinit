from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Tenant


User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = (
            'url',
            'id',
            'username',
            'password',
        )
        # Make sure that the password field is never sent back to the client.
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        updated = super().update(instance, validated_data)

        # We save again the user if the password was specified to make sure it's properly hashed.
        if 'password' in validated_data:
            updated.set_password(validated_data['password'])
            updated.save()
        return updated


class TenantSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Tenant
        fields = (
            'id',
            'name',
            'address',
        )


class AccountSerializer(serializers.Serializer):
    """Serializer that has two nested Serializers: tenant and user"""

    tenant = TenantSerializer()
    user = UserSerializer()

    def create(self, validated_data):
        tenant_data = validated_data['tenant']
        user_data = validated_data['user']

        # Call our TenantManager method to create the Tenant and the User
        tenant, user = Tenant.objects.create_account(
            tenant_name=tenant_data.get('name'),
            tenant_address=tenant_data.get('address'),
            username=user_data.get('username'),
            password=user_data.get('password'),
        )

        return {'tenant': tenant, 'user': user}

    def update(self, instance, validated_data):
        raise NotImplementedError('Cannot call update() on an account')
