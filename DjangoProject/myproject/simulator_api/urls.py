from django.urls import path
from .views.SimulateController import *
from .views.ConfigController import *
from .views.ComponentController import *
from graphene_django.views import GraphQLView
from .schema import schema

from .views.BuildSimulator import *
urlpatterns = [
    path('', SimulateController.as_view(), name='simulate'),
    path('configs/', ConfigController.as_view(), name='configs'),
    path('Components/', ComponentController.as_view(), name='Components'),
    path('run/', SimulateController.runSimulator),
    path('stop/', SimulateController.stopSimulator),
    path('graphql',GraphQLView.as_view(graphiql = True , schema = schema))

]
