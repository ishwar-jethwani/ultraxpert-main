from django.shortcuts import render
import subprocess
# Create your views here.
def meet(request):
    return render(request,"meet.html")
