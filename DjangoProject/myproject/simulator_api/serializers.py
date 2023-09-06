
from rest_framework import serializers
from .models import *

class SimulateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Simulator
        fields = "__all__"



class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataConfig
        fields = "__all__"


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = "__all__"

        


