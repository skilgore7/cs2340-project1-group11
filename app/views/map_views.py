from django.views import View
from django.shortcuts import render, redirect
import googlemaps
from django.conf import settings
from datetime import datetime

class ExploreMap(View):
    template_name = "app/explore.html"

    def get(self,request): 
        key = settings.GOOGLE_API_KEY
        context = {
            "key":key, 
        }

        return render(request, self.template_name, context)
