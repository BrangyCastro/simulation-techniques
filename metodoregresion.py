import matplotlib.pyplot as plt
from flask import Blueprint, Flask, render_template, make_response, request, send_file
from wtforms import Form, FloatField, validators, StringField, IntegerField, TextAreaField
from numpy import exp, cos, linspace
from math import pi
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
matplotlib.use('Agg')

metodo_regresion_api = Blueprint('metodo_regresion_api', __name__)

style = {'class': 'form-control', "rows": 3}


@metodo_regresion_api.route('/lineal', methods=("POST", "GET"))
def regresion_lineal():
    class InputForm(Form):
        N = TextAreaField(
            label='Ingresar los valores de X separados por comas (,)',
            default='1,2,3,4,5,6,7,8,9,10,11,12,13,14,15',
            validators=[validators.InputRequired()],
            render_kw=style)
        M = TextAreaField(
            label='Ingresar los valores de Y separados por comas (,)',
            default='5501.0, 6232.7, 8118.3, 10137.00, 10449.50, 12794.60, 9939.10, 13193.00, 16036.2, 18496.90, 18709.30, 19363.50, 16521.50, 15175.40, 16927.00',
            validators=[validators.InputRequired()],
            render_kw=style)

    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        # datos experimentales
        # el DataFrame se llama movil
        prueba = str(form.N.data)
        prueba2 = str(form.M.data)
        ex = prueba.split(",")
        ex2 = prueba2.split(",")
        valX = list(map(float, ex))
        valY = list(map(float, ex2))
        exporta = {'X': valX,
                   'Y': valY}

        a = pd.DataFrame(exporta)
        x = a['X']
        y = a['Y']
        df = pd.DataFrame({'X': x, 'Y': y})
        x2 = df["X"]**2
        xy = df["X"] * df["Y"]
        df["X^2"] = x2
        df["XY"] = xy

        # ajuste de la recta (polinomio de grado 1 f(x) = ax + b)
        p = np.polyfit(x, y, 1)  # 1 para lineal, 2 para polinomio ...
        p0, p1 = p
        P0 = p0
        P1 = p1
        pfinal = -(p1/p0)
        y_ajuste = p[0]*x + p[1]
        df['Ajuste'] = y_ajuste

        cant = len(df['Y'])

        cant1 = df['X']
        cant2 = df['Y']
        cant3 = df['X^2']
        cant4 = df['XY']

        sum1 = cant1.values.sum()
        sum2 = cant2.values.sum()
        sum3 = cant3.values.sum()
        sum4 = cant4.values.sum()
        # dibujamos los datos experimentales de la recta
        p_datos = plt.plot(x, y, 'b.')
        # Dibujamos la recta de ajuste
        p_ajuste = plt.plot(x, y_ajuste, 'r-')
        plt.title('Ajuste lineal por mínimos cuadrados')
        plt.xlabel('Eje x')
        plt.ylabel('Eje y')
        plt.legend(('Datos experimentales', 'Ajuste lineal',),
                   loc="upper right")
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

        return render_template('/metspages/metreg/reglineal.html', form=form, tables=[df.to_html(classes='table table-hover')], grafica=plotfile, cant=cant, sum1=sum1,
                               sum2=sum2, sum3=sum3, sum4=sum4, P0=P0, P1=P1, fin=pfinal)
    else:
        N = None
        M = None
        cant = None
        sum1 = None
        sum2 = None
        sum3 = None
        sum4 = None
        P0 = None
        P1 = None
        fin = None
    return render_template('/metspages/metreg/reglineal.html', form=form, N=N, M=M, cant=cant, sum1=sum1, sum2=sum2, sum3=sum3, sum4=sum4, P0=P0, P1=P1, fin=fin)


@metodo_regresion_api.route('/nolineal', methods=("POST", "GET"))
def regresion_no_lineal():
    class InputForm(Form):
        N = TextAreaField(
            label='Ingresar los valores de X separados por comas (,)',
            default='1,2,3,4,5,6,7,8,9,10,11,12,13,14,15',
            validators=[validators.InputRequired()],
            render_kw=style)
        M = TextAreaField(
            label='Ingresar los valores de Y separados por comas (,)',
            default='5501.0, 6232.7, 8118.3, 10137.00, 10449.50, 12794.60, 9939.10, 13193.00, 16036.2, 18496.90, 18709.30, 19363.50, 16521.50, 15175.40, 16927.00',
            validators=[validators.InputRequired()],
            render_kw=style)
        C = IntegerField(
            label='Dato a predecir', default=1,
            validators=[validators.InputRequired()],
            render_kw=style)

    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        # Importar libreria numpy
        # datos experimentales
        # el DataFrame se llama movil
        prueba = str(form.N.data)
        prueba2 = str(form.M.data)
        PRED = int(form.C.data)

        ex = prueba.split(",")
        ex2 = prueba2.split(",")
        valX = list(map(float, ex))
        valY = list(map(float, ex2))
        exporta = {'ValTiempo': valX,
                   'Y': valY}
        a = pd.DataFrame(exporta)
        cantidad = len(a['ValTiempo'])
        c = 2
        x = [0]
        ini = 1
        fin = -1
        while c <= cantidad:
            if c % 2 == 0:
                x.append(ini)
                ini = ini+1
                c = c+1
            else:
                x.insert(0, fin)
                fin = fin-1
                c = c+1
        a['X'] = x
        x = a['X']
        y = a['Y']
        ValTiempo = a["ValTiempo"]
        df = pd.DataFrame({'ValTiempo': ValTiempo, 'X': x, 'Y': y})
        x2 = df["X"]**2
        x3 = df["X"]**3
        x4 = df["X"]**4
        xy = df["X"] * df["Y"]
        x2y = x2 * df["Y"]
        df["X^2"] = x2
        df["X^3"] = x3
        df['X^4'] = x4
        df["XY"] = xy
        df["X^2Y"] = x2y

        cant1 = df['X']
        cant2 = df['Y']
        cant3 = df['X^2']
        cant4 = df['X^3']
        cant5 = df['X^4']
        cant6 = df['XY']
        cant7 = df['X^2Y']

        sum1 = cant1.values.sum()
        sum2 = cant2.values.sum()
        sum3 = cant3.values.sum()
        sum4 = cant4.values.sum()
        sum5 = cant5.values.sum()
        sum6 = cant6.values.sum()
        sum7 = cant7.values.sum()

        p = np.polyfit(x, y, 2)
        p0, p1, p2 = p
        P0 = p0
        P1 = p1
        P2 = p2
        #print ("El valor de p0 = ", p0, "Valor de p1 = ", p1, " el valor de p2 = ",p2)
        y_ajuste = p[0]*x*x + p[1]*x + p[2]
        n = x.size
        x1 = []
        x2 = []
        for i in [PRED]:
            y1_ajuste = p[0]*i*i + p[1]*i + p[2]
            x1.append(i)
            x2.append(y1_ajuste)
        df["Ajuste"] = y_ajuste
        dp = pd.DataFrame({'ValTiempo': 'Dato buscado',
                           'X': PRED, 'Y': [0], 'Ajuste': x2})
        res = x2[-1]
        df = df.append(dp, ignore_index=True)

        p_datos = plt.plot(x, y, 'b.')
        # Dibujamos la curva de ajuste
        p_ajuste = plt.plot(x, y_ajuste, 'r-')
        plt.title('Ajuste Polinomial por mínimos cuadrados')
        plt.xlabel('Eje x')
        plt.ylabel('Eje y')
        plt.legend(('Datos experimentales', 'Ajuste Polinomial',),
                   loc="upper left")
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

        return render_template('/metspages/metreg/regnolineal.html', form=form, tables=[df.to_html(classes='table table-hover')], grafica=plotfile, sum1=sum1,
                               sum2=sum2, sum3=sum3, sum4=sum4, sum5=sum5, sum6=sum6, sum7=sum7, P0=P0, P1=P1, P2=P2, cant=cantidad, pron=PRED, res=res)
    else:
        N = None
        M = None
        C = None
        sum1 = None
        sum2 = None
        sum3 = None
        sum4 = None
        sum5 = None
        sum6 = None
        sum7 = None
        P0 = None
        P1 = None
        P2 = None
        cantidad = None
        PRED = None
        res = None
    return render_template('/metspages/metreg/regnolineal.html', form=form, N=N, M=M, C=C, sum1=sum1,
                           sum2=sum2, sum3=sum3, sum4=sum4, sum5=sum5, sum6=sum6, sum7=sum7, P0=P0, P1=P1, P2=P2, cant=cantidad, pron=PRED, res=res)
