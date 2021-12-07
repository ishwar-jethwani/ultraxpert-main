from django.shortcuts import render
import os
from UltraExperts.constants import VIDEOSDK_API_KEY
# Create your views here.
def meet(request):
    key = ""
    try:
        key = os.environ["API_KEY"]
    except KeyError:
        key = VIDEOSDK_API_KEY
       
    context = {"API_KEY":str(key)}
    return render(request,"meet.html",context)
