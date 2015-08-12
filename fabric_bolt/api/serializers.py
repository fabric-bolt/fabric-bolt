from rest_framework import serializers
from fabric_bolt.projects.models import Deployment


class DeploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deployment
    is_finished = serializers.BooleanField()