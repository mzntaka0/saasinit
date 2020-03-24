# -*- coding: utf-8 -*-
"""
"""
#import json

from rest_framework import serializers
from . import models
#from accounts.models import Tenant


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Document
        exclude = ['created_at']


class DocumentListSerializer(serializers.ListSerializer):
    child = DocumentSerializer()


# TODO: idk these are correct or not. Check it out.
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = (
            'id',
            'category_name',
            'category_type',
        )


class DataSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Data
        exclude = ['created_at']


class DataListSerializer(serializers.ListSerializer):
    child = DataSerializer()


class FieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Field
        fields = (
            'id',
            'field_num',
            'is_indexed',
            'field_name',
            'field_type',
        )


class FieldListSerializer(serializers.ListSerializer):
    child = FieldSerializer()


class TableSerializer(serializers.Serializer):
    category = CategorySerializer()
    fields = FieldSerializer(many=True)

    # TODO: add creation process
    def create(self, validated_data):
        category_data = validated_data['category']
        field_data = validated_data['fields']

        category, fields = models.Category.objects.create_table(
            category_name=category_data.get('category_name'),
            category_type=category_data.get('category_type'),
            field_data=field_data
        )
        return {'category': category, 'fields': fields}

    def update(self, instance, validated_data):
        raise NotImplementedError('Cannot call update() on an account')
