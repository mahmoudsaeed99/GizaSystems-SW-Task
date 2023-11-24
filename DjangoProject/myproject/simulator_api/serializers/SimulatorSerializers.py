
from rest_framework import serializers
from simulator_api.models import *
from rest_framework.response import Response
from ..views.ConfigController import *

from ..views.ConfigManager.SQLDB import *
from .ConfigSerializer import ConfigSerializer

class SimulateSerializer(serializers.ModelSerializer):
    dataset = ConfigSerializer(many=True, read_only=True)
    class Meta:
        model = Simulator
        fields = "__all__"
    # def __init__(self, *args, **kwargs):
    #     # Get the 'dataset' key from the incoming data
    #     datasets_data = kwargs.get('data', {}).get('dataset', [])
    #     # Call the parent class with the modified data
    #     super().__init__(data=kwargs.get('data', {}), *args, **kwargs)
    #     # Add the 'dataset' key back to the validated data
    #     self.initial_data['dataset'] = datasets_data
    def create(self, validated_data):
        """
        Create a new Simulator instance with related Datasets.

        Args:
            validated_data (dict): The validated data for creating the Simulator.

        Returns:
            Simulator: The created Simulator instance.
        """
        datasets_data = self.initial_data.get('dataset')
        simulator = Simulator.objects.create(**validated_data)

        for dataset_data in datasets_data:
            # Validate dataset_data before creating a Dataset instance
            dataset_data['simulater'] = simulator.id
            dataset_serializer = ConfigSerializer(data=dataset_data)
            if dataset_serializer.is_valid():
               dataset_serializer.save()
            else:
                # If validation fails, raise a ValidationError with the error messages
                raise serializers.ValidationError(dataset_serializer.errors)
        return simulator

    def to_representation(self, instance):
        """
        Convert the Simulator instance to a serialized representation.

        Args:
            instance (Simulator): The Simulator instance to serialize.

        Returns:
            dict: The serialized representation of the Simulator instance.
        """
        representation = super().to_representation(instance)
        # Include related datasets as JSON in the serialized representation
        datasets = DataConfig.objects.filter(simulater=instance.id)
        representation['data'] = ConfigSerializer(datasets, many=True).data

        return representation

