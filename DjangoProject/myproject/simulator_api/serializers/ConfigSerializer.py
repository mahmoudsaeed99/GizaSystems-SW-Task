from rest_framework import serializers
from simulator_api.models import *
from .ComponentSerializer import ComponentSerializer

class ConfigSerializer(serializers.ModelSerializer):
    # seasonality_components = ComponentSerializer(many = True)
    seasonality_components = ComponentSerializer(many=True, read_only=True)
    class Meta:
        model = DataConfig
        fields = "__all__"


    def create(self, validated_data):
        """
        Create a new Dataset instance with related Seasonality components.

        Args:
            validated_data (dict): The validated data for creating the Dataset.

        Returns:
            Dataset: The created Dataset instance.
        """

        seasonality_components = self.initial_data.get('seasonality_components')
        dataset = DataConfig.objects.create(**validated_data)
        for seasonality_component in seasonality_components:
            # Validate seasonality_component before creating a Seasonality instance
            seasonality_component['dataconfig'] = dataset.id
            seasonality_serializer = ComponentSerializer(data=seasonality_component)
            if seasonality_serializer.is_valid():
                seasonality_serializer.save()
            else:
                # If validation fails, raise a ValidationError with the error messages
                raise serializers.ValidationError(seasonality_serializer.errors)
        return dataset

    def to_representation(self, instance):
        """
        Convert the Dataset instance to a serialized representation.

        Args:
            instance (Dataset): The Dataset instance to serialize.

        Returns:
            dict: The serialized representation of the Dataset instance.
        """
        representation = super().to_representation(instance)

        # Include related seasonality components as JSON in the serialized representation
        seasonality_components = Component.objects.filter(dataconfig=instance.id)
        representation['seasonality_components'] = ComponentSerializer(seasonality_components, many=True).data
        return representation
