from django.urls import path
from .views.views import *
from .views.DataConfig import *
from .views.Component import *
urlpatterns = [
    path('simulate/', SimulateController.as_view(), name='simulate'),
    path('configs/',ConfigController.as_view() , name = 'configs'),
    path('Components/',ComponentController.as_view() , name = 'Components'),
]
