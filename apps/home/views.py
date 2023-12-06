# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect
import joblib
from .models import DiabetesData

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
    
# other imports...

def classify_view(request):
    if request.method == 'GET':
        # Get the input data from the request
        preg = float(request.GET.get('preg', 0))
        gluc = float(request.GET.get('gluc', 0))
        blood = float(request.GET.get('blood', 0))
        skin = float(request.GET.get('skin', 0))
        ins = float(request.GET.get('ins', 0))
        bmi = float(request.GET.get('bmi', 0))
        dbf = float(request.GET.get('dbf', 0))
        age = float(request.GET.get('age', 0))

        # Load the saved machine learning model
        model_filename = "C:/Users/djaba/mydjangosite/logistic_regression_model.pkl"
        loaded_model = joblib.load(model_filename)

        # Define sample input data
        sample_input = [[preg, gluc, blood, skin, ins, bmi, dbf, age]]

        # Make predictions using the loaded model
        predicted = loaded_model.predict(sample_input)
        predicted_category = "You are Diabetic!" if predicted[0] == 1 else "You are Non-Diabetic!"
        
        # Save input data and result to the database
        DiabetesData.objects.create(preg=preg, gluc=gluc, blood=blood, skin=skin, ins=ins, bmi=bmi, dbf=dbf, age=age, result=predicted_category)

        # Fetch all data from the database
        all_data = DiabetesData.objects.all()

        # Render the result in the diabetes.html and classification.html templates
        return render(request, 'home/diabetes.html', {'Category': predicted_category, 'input_data': sample_input, 'all_data': all_data})
    
    # Handle the case where the request method is not 'GET'
    return HttpResponse("Invalid request method")
 
        # return render(request, 'home/diabetes.html', {'Category': predicted_category})
