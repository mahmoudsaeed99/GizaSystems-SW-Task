from django.urls import path
from .views.SimulateController import *
from .views.ConfigController import *
from .views.ComponentController import *
from .views.RunSimulator import *
urlpatterns = [
    path('', SimulateController.as_view(), name='simulate'),
    path('configs/',ConfigController.as_view() , name = 'configs'),
    path('Components/',ComponentController.as_view() , name = 'Components'),
    path('run/' , RunSimulator.runSimulator)
    

]
