# django
from django.db.models import Q
from django.shortcuts import get_object_or_404

# properties
from properties.models import Owner, Estate
from properties.api.serializers import OwnerSerializer, EstateSerializer

# rest_framework
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST)
from rest_framework.viewsets import ViewSet


class OwnerViewSet(ViewSet):
    lookup_field = 'uuid'

    def list(self, request):
        queryset = Owner.objects.all()
        serializer = OwnerSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = Owner.objects.all()
        owner = get_object_or_404(queryset, uuid=kwargs['uuid'])
        serializer = OwnerSerializer(owner)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = OwnerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        owner = Owner.objects.create(**serializer.data)
        print(OwnerSerializer(instance=owner).data)
        return Response(OwnerSerializer(owner).data, status=HTTP_201_CREATED)

    def partial_update(self, request, pk=None, *args, **kwargs):
        data = request.data
        owner = get_object_or_404(Owner, uuid=kwargs['uuid'])
        # Actualizar los datos de los campos proporcionados
        for field, value in data.items():
            setattr(owner, field, value)

        try:
            owner.save()
        except Exception as e:
            return Response({'error': str(e)}, status=HTTP_400_BAD_REQUEST)

        serializer = OwnerSerializer(owner)
        return Response(serializer.data, status=HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None, *args, **kwargs):
        owner = get_object_or_404(Owner, uuid=kwargs['uuid'])
        owner.delete()
        return Response({}, status=HTTP_204_NO_CONTENT)


class EstateViewSet(ViewSet):
    lookup_field = 'uuid'

    def list(self, request):
        query_arguments = Q()
        if request.query_params:
            name = request.query_params.get('name')
            cadastral_certificate = request.query_params.get(
                'cadastral_certificate')
            owner_name = request.query_params.get('owner_name')
            owner_identification = request.query_params.get(
                'owner_identification')
            estate_type = request.query_params.get('estate_type')
            if name:
                query_arguments = query_arguments & Q(name__icontains=name)
            if cadastral_certificate:
                query_arguments = query_arguments & Q(
                    cadastral_certificate__icontains=cadastral_certificate)
            if estate_type:
                query_arguments = query_arguments & Q(estate_type=estate_type)
            if owner_name:
                query_arguments = query_arguments & Q(
                    owners__name__icontains=owner_name)
            if owner_identification:
                query_arguments = query_arguments & Q(
                    owners__identification__icontains=owner_identification)
        queryset = Estate.objects.filter(query_arguments).distinct()
        serializer = EstateSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = Estate.objects.all()
        estate = get_object_or_404(queryset, uuid=kwargs['uuid'])
        serializer = EstateSerializer(estate)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        owners_data = []
        if 'owners' in request.data:
            owners_data = request.data['owners']
            request.data['owners'] = []

        serializer = EstateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer_data = dict(serializer.data)
        if 'owners' in serializer_data:
            serializer_data.pop("owners", None)

        estate = Estate.objects.create(**serializer_data)
        if owners_data:
            owners = Owner.objects.filter(uuid__in=owners_data)
            for owner in owners:
                estate.owners.add(owner)
        return Response(
            EstateSerializer(instance=estate).data,
            status=HTTP_201_CREATED)

    def partial_update(self, request, pk=None, *args, **kwargs):
        data = request.data
        estate = get_object_or_404(Estate, uuid=kwargs['uuid'])

        # verificar si viene el campo owners
        owners_data = []
        if 'owners' in data:
            owners_data = data['owners']
            del data['owners']

        # Actualizar los datos de los campos proporcionados
        for field, value in data.items():
            setattr(estate, field, value)

        try:
            estate.save()
        except Exception as e:
            return Response({'error': str(e)}, status=HTTP_400_BAD_REQUEST)

        # eliminar los propietarios anteriores
        estate.owners.clear()

        # almacenar los dueños del predio
        if owners_data:
            owners = Owner.objects.filter(uuid__in=owners_data)
            for owner in owners:
                estate.owners.add(owner)

        serializer = EstateSerializer(estate)
        return Response(serializer.data, status=HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None, *args, **kwargs):
        estate = get_object_or_404(Estate, uuid=kwargs['uuid'])
        estate.delete()
        return Response({}, status=HTTP_204_NO_CONTENT)
