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


metodo_pronostico_api = Blueprint('metodo_pronostico_api', __name__)

style = {'class': 'form-control'}


@metodo_pronostico_api.route('/pronostico/prommovil', methods=("POST", "GET"))
def promedio_movil():
    class InputForm(Form):
        N = TextAreaField(
            label='Ingrese una serie de números separados por comas (,)',
            default='5501.0, 6232.7, 8118.3, 10137.00, 10449.50, 12794.60, 9939.10, 13193.00, 16036.2, 18496.90, 18709.30, 19363.50, 16521.50, 15175.40, 16927.00',
            validators=[validators.InputRequired()],
            render_kw={'class': 'form-control', "rows": 3})

    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        # Promedio Móvil
        # Vamos a crear un DataFrame con los datos y luego procederemos a calcular el promedio movil MMO_3 = 3 y MMO_4 = 4
        # el DataFrame se llama movil
        prueba = str(form.N.data)
        ex = prueba.split(",")
        ex2 = list(map(float, ex))
        exporta = {'Año': ex2,
                   'Valores': ex2}
        movil = pd.DataFrame(exporta)

        prediccion = len(ex2)
        predfinal = prediccion - 3
        # mostramos los 5 primeros registros
        # calculamos para la primera media móvil MMO_3
        for i in range(0, movil.shape[0]-2):
            movil.loc[movil.index[i+2], 'Promedio a 3'] = np.round(
                ((movil.iloc[i, 1]+movil.iloc[i+1, 1]+movil.iloc[i+2, 1])/3), 1)
        # calculamos para la segunda media móvil MMO_4
        for i in range(0, movil.shape[0]-3):
            movil.loc[movil.index[i+3], 'Promedio a 4'] = np.round(((movil.iloc[i, 1]+movil.iloc[i+1, 1]+movil.iloc[i+2, 1]+movil.iloc[i +
                                                                                                                                       3, 1])/4), 1)
        # calculamos la proyeción final
        proyeccion = movil.iloc[predfinal:, [1, 2, 3]]
        p1, p2, p3 = proyeccion.mean()
        # incorporamos al DataFrame
        a = movil.append({'Año': 2018, 'Valores': p1,
                          'Promedio a 3': p2, 'Promedio a 4': p3}, ignore_index=True)
        # mostramos los resultados
        a['Error promedio 3'] = a['Valores']-a['Promedio a 3']
        a['Error promedio 4'] = a['Valores']-a['Promedio a 4']
        df = a

        dftemp1 = df['Valores']
        dftemp2 = df['Promedio a 3']
        dftemp3 = df['Promedio a 4']
        dftemp4 = df['Error promedio 3']
        dftemp5 = df['Error promedio 4']
        resv1 = dftemp1[0]
        resv2 = dftemp1[1]
        resv3 = dftemp1[2]
        resv4 = dftemp1[3]

        resv5 = dftemp2[2]
        resv6 = dftemp3[3]
        resv7 = dftemp4[2]
        resv8 = dftemp5[3]

        plt.figure(figsize=[8, 8])
        plt.grid(True)
        plt.plot(a['Valores'], label='Valores', marker='o')
        plt.plot(a['Promedio a 3'], label='Media Móvil 3 años')
        plt.plot(a['Promedio a 4'], label='Media Móvil 4 años')
        plt.legend(loc=2)
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

        del df['Año']
        return render_template('/metspages/metprob/prommovil.html', form=form, tables=[df.to_html(classes='data')], grafica=plotfile, res1=resv1,
                               res2=resv2, res3=resv3, res4=resv4, res5=resv5, res6=resv6, res7=resv7, res8=resv8)
    else:
        N = None
        resv1 = None
        resv2 = None
        resv3 = None
        resv4 = None
        resv5 = None
        resv6 = None
        resv7 = None
        resv8 = None
    return render_template('/metspages/metprob/prommovil.html', form=form, N=N, res1=resv1,
                           res2=resv2, res3=resv3, res4=resv4, res5=resv5, res6=resv6, res7=resv7, res8=resv8)


@metodo_pronostico_api.route('/pronostico/alisexponencial', methods=("POST", "GET"))
def alisamiento_exponencial():
    class InputForm(Form):
        N = TextAreaField(
            label='Ingrese una serie de números separados por comas (,)',
            default='5501.0, 6232.7, 8118.3, 10137.00, 10449.50, 12794.60, 9939.10, 13193.00, 16036.2, 18496.90, 18709.30, 19363.50, 16521.50, 15175.40, 16927.00',
            validators=[validators.InputRequired()],
            render_kw={'class': 'form-control', "rows": 3})
        M = FloatField(
            label='Valor de alfa \( \ \propto \ \) (entre 0 y 1)', default=0.1,
            validators=[validators.InputRequired(), validators.NumberRange(
                min=0.1, max=1, message='Solo valores entre 0 y 1')],
            render_kw=style)

    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        # el DataFrame se llama movil
        M = (form.M.data)
        prueba = str(form.N.data)
        ex = prueba.split(",")
        ex2 = list(map(float, ex))
        exporta = {'Año': ex2,
                   'Valores': ex2}
        movil = pd.DataFrame(exporta)
        # mostramos los 5 primeros registros
        movil.head()
        alfa = M
        unoalfa = 1. - alfa
        for i in range(0, movil.shape[0]-1):
            movil.loc[movil.index[i+1], 'SN'] = np.round(movil.iloc[i, 1], 1)
        for i in range(2, movil.shape[0]):
            movil.loc[movil.index[i], 'SN'] = np.round(
                movil.iloc[i-1, 1], 1)*alfa + np.round(movil.iloc[i-1, 2], 1)*unoalfa
        i = i+1
        p2 = np.round(movil.iloc[i-1, 1], 1)*alfa + \
            np.round(movil.iloc[i-1, 2], 1)*unoalfa
        movil['Error pronóstico'] = movil['Valores']-movil['SN']

        plt.figure(figsize=[8, 8])
        plt.grid(True)
        plt.plot(movil['Valores'], label='Valores originales')
        plt.plot(movil['SN'], label='Suavización Exponencial')
        plt.legend(loc=2)
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

        a = movil.append(
            {'Año': 2018, 'Valores': "Pronóstico", 'SN': p2}, ignore_index=True)
        df = a
        del df['Año']

        deftemp1 = df['Valores']
        deftemp2 = df['SN']
        deftemp3 = df['Error pronóstico']
        resv1 = deftemp1[1]
        resv2 = deftemp2[1]
        resv3 = deftemp2[2]
        resv4 = deftemp3[2]
        resv5 = deftemp1[2]
        # movil
        # %matplotlib inline

        return render_template('/metspages/metprob/alisexponencial.html', form=form, tables=[df.to_html(classes='data')], grafica=plotfile, M=alfa, res1=resv1, res2=resv2, res3=resv3, res4=resv4, res5=resv5)
    else:
        N = None
        M = None
        resv1 = None
        resv2 = None
        resv3 = None
        resv4 = None
        resv5 = None
    return render_template('/metspages/metprob/alisexponencial.html', form=form, N=N, M=M, res1=resv1, res2=resv2, res3=resv3, res4=resv4, res5=resv5)
