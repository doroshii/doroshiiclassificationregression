# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this
from apps.home import views  # add this

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("", include("apps.authentication.urls")), # Auth routes - login / register

    # ADD NEW Routes HERE
     # ADD NEW Routes HERE
    path("classify", views.classify_view, name="classify"),  # Add this line for the classify view

    # Leave `Home.Urls` as last the last line
    path("", include("apps.home.urls"))
]
