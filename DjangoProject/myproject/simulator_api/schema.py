import graphene
from graphene_django import DjangoObjectType
from .models import *

class SimulatorType(DjangoObjectType):
    class Meta:
        model = Simulator
        fields = "__all__"


class Query(graphene.ObjectType):
    all_simulators = graphene.List(SimulatorType)
    def resolve_all_simulators(root ,info):
        return Simulator.objects.all()

schema = graphene.Schema(query=Query)
