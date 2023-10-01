from rest_framework import serializers
from simulator_api.models import *

class ConfigSerializer(serializers.ModelSerializer):
    # components = serializers.StringRelatedField(many = True)
    class Meta:
        model = DataConfig
        fields = "__all__"
