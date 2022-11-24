from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .serializers import *

class TriningList(ListAPIView):
    """This Class Will Return List of Trinings"""
    serializer_class = TrainingSerializer
    queryset = Training.objects.all()
    

# Create your views here.
