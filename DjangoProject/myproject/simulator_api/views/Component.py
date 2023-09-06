from django.shortcuts import render
from django.urls import reverse
from rest_framework.response import Response
# Create your views here.
from rest_framework.generics import ListAPIView , ListCreateAPIView 
from ..models import *
from ..serializers import *
from rest_framework import status
import datetime
class ComponentController(ListCreateAPIView ):
    """
        ComponentController Class inherit from ListCreateAPIView
        serializer class is componentSerializer
    """
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
    def get(self, request, *args, **kwargs):
        data = self.list(request,*args, **kwargs).data
        return Response(data = data)
    
    def add(self,data , item, **kwargs ):
        """
            add function take 2 arguments
            data-> list : list of component dict that needs to add to database
            item-> integer : data config ID
        """
        componentList = []
        components = {}
        print(data)
        for i in data:
            components = {'frequency':i['frequency'],
                            'multiplier':i['multiplier'],
                            'phase_shift':i['phase_shift'],
                            'amplitude':i['amplitude'],
                            'dataconfigID':item,
                            }
            # create object of ComponentSerializer
            serielizer = ComponentSerializer(data=components)

            print(serielizer.is_valid())
            # check if the data are validate or not
            if serielizer.is_valid():
                serielizer.save()
            # componentList.append([serielizer.data])
            # DataConfig.save()
            # configs =  self.create(dataConfig , 'custom', **kwargs )
        return serielizer.data
    











