from django.shortcuts import render
import os
from UltraExperts.constants import VIDEOSDK_API_KEY
# Create your views here.
def meet(request):
    key = ""
    if len(os.environ["API_KEY"]) == 0:
        key = VIDEOSDK_API_KEY
    else:
        key = os.environ["API_KEY"]
    context = {"API_KEY":key}
    return render(request,"meet.html",context)
