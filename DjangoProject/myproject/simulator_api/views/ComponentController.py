from rest_framework.response import Response
# Create your views here.
from rest_framework.generics import ListCreateAPIView
from ..serializers.ComponentSerializer import *
from ..models import Component
from rest_framework.filters import SearchFilter


class ComponentController(ListCreateAPIView ):
    """
        ComponentController Class inherit from ListCreateAPIView
        serializer class is componentSerializer
    """
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('=dataconfigID',)
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
        for i in data:
            i['dataconfig'] = item
            # create object of ComponentSerializer
            try:
                serielizer = ComponentSerializer(data=i)
            except Exception as e:
                print(e)
            # check if the data are validate or not
            if serielizer.is_valid():
                serielizer.save()
        return serielizer.data
    
    def get_data_component(self,data_id):
        """
            return components for specific data configs
        
        """
        data = Component.objects.all().filter(dataconfigID =data_id).values()
        data = {
                'components': data,
                }
        return data










