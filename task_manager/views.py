# from django.views.generic import TemplateView
from django.views.generic import View
from pathlib import Path
import os
from django.shortcuts import render

class HomeView(View):

    def get(self, request, *args, **kwargs):
        BASE_DIR = Path(__file__).resolve().parent.parent
        LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)

        return render(request, 'index.html',
                      context={'BASE_DIR': BASE_DIR,
                               'LOCALE_PATHS': LOCALE_PATHS,
                              },
                      ) 
#    template_name = 'index.html'
