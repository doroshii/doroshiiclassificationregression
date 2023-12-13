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
    path('predict_sale_view', views.predict_sale_view, name='predict_sale_view'),
    path('product_data_list', views.product_data_list, name='product_data_list'),
    path('diabetes_data_list', views.diabetes_data_list, name='diabetes_data_list'),
    path('diabetes_chart_view', views.diabetes_chart_view, name='diabetes_chart_view'),
    # path('sales_chart_view', views.sales_chart_view, name='sales_chart_view'),
    path('line_chart', views.line_chart_view, name='line_chart_view'),  # Add this line
    path('pie_chart', views.pie_chart_view, name='pie_chart_view'),
    path('stacked_bar_chart', views.stacked_bar_chart, name='stacked_bar_chart'),
    # Leave `Home.Urls` as last the last line
    path("", include("apps.home.urls"))
    
]
