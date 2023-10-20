from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from user_agents import parse
import json

# Create your views here.
@csrf_exempt
def index(req):
    # if req.is_mobile:
    #     return render(req, "landing-mobile.html")
    ua = parse(req.META.get('HTTP_USER_AGENT'))
    if ua.is_mobile:
        return render(req, "landing-mobile.html")
    return render(req, "landing.html")