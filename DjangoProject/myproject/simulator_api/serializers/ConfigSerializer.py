from rest_framework import serializers
from simulator_api.models import *
from .ComponentSerializer import ComponentSerializer

class ConfigSerializer(serializers.ModelSerializer):
    # seasonality_components = ComponentSerializer(many = True)
    class Meta:
        model = DataConfig
        fields = "__all__"
