from django.shortcuts import get_object_or_404
from rest_framework import views, generics, permissions, status, viewsets
from rest_framework.response import Response
from django_filters import rest_framework as filters

from . import models
from . import serializers
#from accounts.permissions import IsAdminUser
from accounts.models import Tenant


class UserIDView(views.APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, request, *args, **kwargs):
        return Response({'userID': request.user.id}, status=views.HTTP_200_OK)


class TenantIDView(views.APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, request, *args, **kwargs):
        return Response({'userID': request.user.tenant.id}, status=views.HTTP_200_OK)


#@JWTManager.requires_scope('read:document')
class DocumentView(views.APIView):
    permission_classes = (
        permissions.IsAuthenticated,
        #IsAdminUser,
    )

    def get(self, request):
        tenant_document = models.Document.objects.filter(tenant=request.user.tenant)
        serializer = serializers.DocumentListSerializer(instance=tenant_document)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = serializers.DocumentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        _t = Tenant.objects.filter
        # TODO: add tenant checker that checks requested tenant is already made in db.
        tenant = _t(name=request.data.get('tenant'))[0] if request.user.is_staff else request.user.tenant
        serializer.save(tenant=tenant)
        return Response(serializer.data, status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        pass

    def delete(self, request):
        pass


class DocumentRetrieveView(generics.RetrieveAPIView):
    serializer_class = serializers.DocumentSerializer

    def get_object(self):
        condition = {"document_content__contains": val
                     for key, val in self.request.query_params.items() if key is not None}  # change this condition later
        documents = models.Document.objects.filter(tenant=self.request.user.tenant)
        documents = documents.filter(**condition)
        obj = get_object_or_404(documents)
        self.check_object_permissions(self.request, obj)
        return obj


class TableCreate(generics.CreateAPIView):
    name = 'table-create'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.TableSerializer


class DocumentFilter(filters.FilterSet):
    permission_classes = (
        permissions.IsAuthenticated,
        #permissions.AllowAny,
    )

    class Meta:
        models = models.Document
        exclude = ['created_at']


class DocumentCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.DocumentSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = models.Document.objects.all()
    serializer_class = serializers.DocumentSerializer
