from django.shortcuts import render
import os
# Create your views here.
def meet(request):
    context = {"API_KEY":os.environ["API_KEY"]}
    return render(request,"meet.html",context)
