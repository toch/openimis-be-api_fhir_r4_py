from medical.models import Item
from rest_framework import viewsets

from api_fhir_r4.mixins import MultiIdentifierRetrieverMixin, MultiIdentifierUpdateMixin
from api_fhir_r4.model_retrievers import CodeIdentifierModelRetriever, UUIDIdentifierModelRetriever
from api_fhir_r4.permissions import FHIRApiMedicationPermissions
from api_fhir_r4.serializers import MedicationSerializer
from api_fhir_r4.views.fhir.fhir_base_viewset import BaseFHIRView


class MedicationViewSet(BaseFHIRView, MultiIdentifierRetrieverMixin, MultiIdentifierUpdateMixin, viewsets.ModelViewSet):
    retrievers = [UUIDIdentifierModelRetriever, CodeIdentifierModelRetriever]
    serializer_class = MedicationSerializer
    permission_classes = (FHIRApiMedicationPermissions,)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        identifier = request.GET.get("identifier")
        if identifier:
            return self.retrieve(request, *args, **{**kwargs, 'identifier': identifier})
        else:
            queryset = queryset.filter(validity_to__isnull=True)
        serializer = MedicationSerializer(self.paginate_queryset(queryset), many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, *args, **kwargs):
        response = super().retrieve(self, *args, **kwargs)
        return response

    def get_queryset(self):
        return Item.get_queryset(None, self.request.user).order_by('validity_from')
