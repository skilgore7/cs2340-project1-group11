from django.conf import settings
from django.shortcuts import render
from django.views import View


class ExploreMap(View):
    template_name = "app/explore.html"

    def get(self,request): 
        key = settings.GOOGLE_API_KEY
        context = {
            "key":key, 
        }

        return render(request, self.template_name, context)
