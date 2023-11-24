import graphene
from graphene_django import DjangoObjectType
from .models import *
from decimal import Decimal
class SimulatorType(DjangoObjectType):
    class Meta:
        model = Simulator
        fields = "__all__"
class ConfigsType(DjangoObjectType):
    class Meta:
        model = DataConfig
        fields = "__all__"
class ComponentsType(DjangoObjectType):
    class Meta:
        model = Component
        fields = "__all__"

class CreateDataConfigMutation(graphene.Mutation):
    class Arguments:
        frequency = graphene.String(required=True)
        noiseLevel = graphene.Int(required=True)
        trendCoef = graphene.String()
        missingPercent = graphene.String(required=True)
        outlierPercent = graphene.Int()
        cycle_amplitude = graphene.Int(required=True)
        cycle_frequency = graphene.Int(required=True)
        generator_id = graphene.Int(required=True)
        attribute_id = graphene.Int(required=True)
        simulator_id = graphene.Int(required=True)

    data_config = graphene.Field(ConfigsType)

    def mutate(self, info, frequency, noiseLevel, trendCoef, missingPercent, outlierPercent,
               cycle_amplitude, cycle_frequency, generator_id, attribute_id , simulator_id):
        missingPercent = Decimal(missingPercent)
        trendCoef = trendCoef or ''
        outlierPercent = outlierPercent or 0
        simulator = Simulator.objects.get(id=simulator_id)
        data_config = DataConfig(
            frequency=frequency,
            noiseLevel=noiseLevel,
            trendCoef=trendCoef,
            missingPercent=missingPercent,
            outlierPercent=outlierPercent,
            cycle_amplitude=cycle_amplitude,
            cycle_frequency=cycle_frequency,
            generator_id=generator_id,
            attribute_id=attribute_id,
            simulater = simulator
        )
        data_config.save()

        return CreateDataConfigMutation(data_config=data_config)
class CreateComponentMutation(graphene.Mutation):
    class Arguments:
        amplitude = graphene.Int(required=True)
        phase_shift = graphene.Int(required=True)
        frequency = graphene.String(required=True)
        multiplier = graphene.Int()
        dataconfig_id = graphene.Int(required=True)

    component = graphene.Field(ComponentsType)

    def mutate(self, info, amplitude, phase_shift, frequency, multiplier, dataconfig_id):
        data_config = DataConfig.objects.get(id=dataconfig_id)
        multiplier = multiplier or 0
        component = Component(
            amplitude=amplitude,
            phase_shift=phase_shift,
            frequency=frequency,
            multiplier=multiplier,
            dataconfig=data_config
        )
        component.save()

        return CreateComponentMutation(component=component)
class Query(graphene.ObjectType):
    all_simulators = graphene.List(SimulatorType)
    all_configs = graphene.List(ConfigsType)
    all_components = graphene.List(ComponentsType)
    def resolve_all_simulators(root ,info):
        return Simulator.objects.all()
    def resolve_all_configs(root ,info):
        return DataConfig.objects.all()
    def resolve_all_components(root ,info):
        return Component.objects.all()

class Mutation(graphene.ObjectType):
    create_data_config = CreateDataConfigMutation.Field()
    create_component = CreateComponentMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
