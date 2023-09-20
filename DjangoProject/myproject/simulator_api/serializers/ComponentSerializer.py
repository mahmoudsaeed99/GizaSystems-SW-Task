from rest_framework import serializers
from simulator_api.models import *

class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = "__all__"

