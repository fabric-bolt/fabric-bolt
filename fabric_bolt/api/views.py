from rest_framework import viewsets
from fabric_bolt.api.serializers import DeploymentSerializer
from fabric_bolt.projects.models import Deployment


class DeploymentViewSet(viewsets.ModelViewSet):
    queryset = Deployment.objects.all()
    serializer_class = DeploymentSerializer