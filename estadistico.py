import matplotlib.pyplot as plt
from flask import Blueprint, Flask, render_template, make_response, request, send_file
from wtforms import Form, FloatField, validators, StringField, IntegerField, TextAreaField
from numpy import exp, cos, linspace
from math import pi, sqrt
import io
import random
import os
import time
import glob
import numpy as np
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
import datetime
import statistics

matplotlib.use('Agg')

estadistico_api = Blueprint('estadistico_api', __name__)

style = {'class': 'form-control', "rows": 3}


@estadistico_api.route('/estadistico', methods=("POST", "GET"))
def estadistico():
    page = "index7"

    class InputForm(Form):
        N = TextAreaField(
            label='Ingresar una serie de números separados por comas (,)',
            default='5501.0, 6232.7, 8118.3, 10137.00, 10449.50, 12794.60, 9939.10, 13193.00, 16036.2, 18496.90, 18709.30, 19363.50, 16521.50, 15175.40, 16927.00',
            validators=[validators.InputRequired()],
            render_kw=style)
    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        prueba = str(form.N.data)
        ex = prueba.split(",")
        valX = list(map(float, ex))
        m = statistics.mean(valX)
        me = statistics.median(valX)
        moda = statistics.mode(valX)
        # plt.figure(figsize=(30, 5))
        plt.hist(valX, bins=10, color='blue')
        plt.axvline(m, color='red', label='Media')
        plt.axvline(me, color='yellow', label='Mediana')
        plt.axvline(moda, color='green', label='Moda')
        plt.xlabel('Eje X')
        plt.ylabel('Eje X')
        plt.legend()
        if not os.path.isdir('static'):
            os.mkdir('static')
        else:
            # Remove old plot files
            for filename in glob.glob(os.path.join('static', '*.png')):
                os.remove(filename)
        # Use time since Jan 1, 1970 in filename in order make
        # a unique filename that the browser has not chached
        plotfile = os.path.join('static', str(time.time()) + '.png')
        plt.savefig(plotfile)
        plt.clf()
        return render_template('/estadistico.html', form=form, page=page, grafica=plotfile, moda=moda, m=m, me=me)
    else:

        N = None

    return render_template('/estadistico.html', N=N, form=form, page=page)
