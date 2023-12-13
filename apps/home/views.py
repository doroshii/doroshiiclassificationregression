# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import matplotlib.pyplot as plt
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
import joblib
from .models import DiabetesData
import numpy as np
from joblib import load  # for scikit-learn < 0.22
from .models import ProductData
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
# import seaborn as snsfrom io import BytesIO
from io import BytesIO
import base64

from django.views.decorators.csrf import csrf_exempt
import json


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
        diabetes_data = DiabetesData.objects.create(preg=preg, gluc=gluc, blood=blood, skin=skin, ins=ins, bmi=bmi, dbf=dbf, age=age, result=predicted_category)

    # Render the result in the diabetes.html template
    return render(request, 'home/diabetes.html', {'Category': predicted_category, 'input_data': sample_input, 'diabetes_data': diabetes_data})

# Diabetes Data Table
def diabetes_data_list(request):
    diabetes_data_list = DiabetesData.objects.all()
    return render(request, 'home/diabetesdata.html', {'diabetes_data_list': diabetes_data_list})


def diabetes_chart_view(request):
    # Retrieve data for the charts
    diabetic_count = DiabetesData.objects.filter(result='You are Diabetic!').count()
    non_diabetic_count = DiabetesData.objects.filter(result='You are Non-Diabetic!').count()

    # Assuming 'result' is a CharField in your model
    data_for_line_chart = json.dumps([['Diabetic', 'Non-Diabetic'], [diabetic_count, non_diabetic_count]])

    labels = ['Diabetic', 'Non-Diabetic']
    values = [diabetic_count, non_diabetic_count]

    # Assuming 'result' is a CharField in your model
    data_for_bar_chart = json.dumps({'labels': labels, 'values': values})

    # Assuming 'result' is a CharField in your model
    data_for_pie_chart = json.dumps({'labels': labels, 'values': values})

    context = {
        'data_for_line_chart': data_for_line_chart,
        'data_for_bar_chart': data_for_bar_chart,
        'data_for_pie_chart': data_for_pie_chart,
    }

    return render(request, 'home/diabeteschart.html', context)


def predict_sale_view(request):
    if request.method == 'POST':
        try:
            # Load the trained model
            model = load('C:/Users/djaba/ITD105/models/elasticnet_model.joblib')

            # Get input data from the form
            
            price = float(request.POST.get('price'))
            radio = float(request.POST.get('radio'))
            in_store_spending = float(request.POST.get('in_store_spending'))
            discount = float(request.POST.get('discount'))
            tv_spending = float(request.POST.get('tv_spending'))
            stock_rate = float(request.POST.get('stock_rate'))
            online_ads_spending = float(request.POST.get('online_ads_spending'))

            # Prepare the input data for prediction
            input_data = np.array([[price, radio, in_store_spending, discount, tv_spending, stock_rate, online_ads_spending]])

            # Make a prediction
            predicted_sale = model.predict(input_data)[0]
            
             # Save input data and prediction to the database
            product_data = ProductData.objects.create(
                price=price,
                radio=radio,
                in_store_spending=in_store_spending,
                discount=discount,
                tv_spending=tv_spending,
                stock_rate=stock_rate,
                online_ads_spending=online_ads_spending,
                predicted_sale=predicted_sale
            )

            # Pass the predicted price to the template
            return render(request, 'home/sales.html', {'predicted_sale': predicted_sale, 'product_data': product_data})

        except Exception as e:
            # Handle exceptions
            return render(request, 'home/sales.html', {'error': str(e)})

    else:
        # Handle non-POST requests
        return render(request, 'home/sales.html', {'error': 'Invalid request method'})
    
# Sales Data Table
def product_data_list(request):
    product_data_list = ProductData.objects.all()
    return render(request, 'home/salesdata.html', {'product_data_list': product_data_list})


def line_chart_view(request):
    # Retrieve data from the database
    product_data_list = ProductData.objects.all()

    # Extract relevant data for the line chart
    labels = [str(data.created_at) for data in product_data_list]
    predicted_sales = [data.predicted_sale for data in product_data_list]

    # Create a line chart
    fig = px.line(x=labels, y=predicted_sales, labels={'x': 'Date', 'y': 'Predicted Sale'},
                  title='Predicted Prices Over Time')

    line_chart_html = fig.to_html(full_html=False)

    return render(request, 'home/saleschart.html', {'chart_html': line_chart_html})

def pie_chart_view(request):
    # Retrieve data from the database
    product_data_list = ProductData.objects.all()

    # Extract relevant data for the pie chart
    labels = ['Price', 'Radio', 'In-store Spending', 'Discount', 'TV Spending', 'Stock Rate', 'Online Ads Spending']
    values = [
        sum([data.price for data in product_data_list]),
        sum([data.radio for data in product_data_list]),
        sum([data.in_store_spending for data in product_data_list]),
        sum([data.discount for data in product_data_list]),
        sum([data.tv_spending for data in product_data_list]),
        sum([data.stock_rate for data in product_data_list]),
        sum([data.online_ads_spending for data in product_data_list]),
    ]
    # Create a pie chart
    fig = px.pie(names=labels, values=values, title='Distribution of Predicted Sale')

    pie_chart_html = fig.to_html(full_html=False)

    return render(request, 'home/saleschart.html', {'chart_html': pie_chart_html})

def stacked_bar_chart(request):
     # Retrieve data from the database
    product_data_list = ProductData.objects.all()

    # Extract relevant data for the stacked bar chart
    predicted_sales = [data.predicted_sale for data in product_data_list]
    feature_labels = ['price', 'radio', 'in_store_spending', 'discount', 'tv_spending', 'stock_rate', 'online_ads_spending']
    features_data = {
        label: [getattr(data, label) for data in product_data_list] for label in feature_labels
    }

    # Create a DataFrame for the features data
    df = pd.DataFrame(features_data)
    df['predicted_sales'] = predicted_sales

    # Create a stacked bar chart
    fig = px.bar(df, x='predicted_sales', y=feature_labels, barmode='stack',
                 labels={'value', 'predicted_sales'},
                 title='Stacked Bar Chart: Feature Contributions to Predicted Sales')

    stacked_bar_chart_html = fig.to_html(full_html=False)

    return render(request, 'home/saleschart.html', {'chart_html': stacked_bar_chart_html})


