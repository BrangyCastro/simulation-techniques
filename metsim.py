import matplotlib.pyplot as plt
from flask import Blueprint, Flask, render_template, make_response, request, send_file
from wtforms import Form, FloatField, validators, StringField, IntegerField, TextAreaField
from numpy import exp, cos, linspace
import math
import itertools
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


metsim_api = Blueprint('metsim_api', __name__)

style = {'class': 'form-control', "rows": 3}


@metsim_api.route('/montecarloaditivo', methods=("POST", "GET"))
def montecarlo_aditivo():
    page = "montecarloaditivo"

    class InputForm(Form):
        L = TextAreaField(
            label='Escriba los valores de ingreso separados por comas (,)',
            default='5501.0, 6232.7, 8118.3, 10137.00, 10449.50, 12794.60, 9939.10,  13193.00, 16036.2, 18496.90, 18709.30, 19363.50, 16521.50, 15175.40,  16927.00',
            validators=[validators.InputRequired()],
            render_kw=style)
        N = IntegerField(
            label='Número de eventos que desea (n)', default=20,
            validators=[validators.InputRequired()],
            render_kw=style)
        M = IntegerField(
            label='Módulo (m)', default=1000,
            validators=[validators.InputRequired()],
            render_kw=style)
        A = IntegerField(
            label='Multiplicador (a)', default=747,
            validators=[validators.InputRequired()],
            render_kw=style)
        X0 = IntegerField(
            label='Semilla (Xn)', default=123,
            validators=[validators.InputRequired()],
            render_kw=style)
        C = IntegerField(
            label='Incremento (c)', default=457,
            validators=[validators.InputRequired()],
            render_kw=style)

    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        # datos experimentales
        # el DataFrame se llama movil
        prueba = str(form.L.data)
        ex = prueba.split(",")
        ex2 = list(map(float, ex))
        exporta = {'Año': ex2,
                   'Valores': ex2}
        a = pd.DataFrame(exporta)
        cant = len(a['Valores'])
        cantidad = list(range(cant + 1))
        cantidad[1:]
        a['Año'] = cantidad[1:]

        dfval = exporta['Valores']

        # Ordenamos por Día
        suma = a['Valores'].sum()
        # cant=len(exporta)
        suma
        x1 = a.assign(Probabilidad=lambda x: x['Valores'] / suma)
        x2 = x1.sort_values('Año')

        salvando = x2['Año']
        del x2['Año']
        a = x2['Probabilidad']
        a1 = np.cumsum(a)  # Cálculo la suma acumulativa de las probabilidades
        x2['FPA'] = a1
        x2['Min'] = x2['FPA']
        x2['Max'] = x2['FPA']
        lis = x2["Min"].values
        lis2 = x2['Max'].values
        lis[0] = 0
        for i in range(1, len(x2['Valores'])):
            lis[i] = lis2[i-1]
        x2['Min'] = lis

        dfprob = x2['Probabilidad']

        n = int(form.N.data)
        m = int(form.M.data)
        a = int(form.A.data)
        x0 = int(form.X0.data)
        c = int(form.C.data)
        x = [1] * n
        r = [0.1] * n
        for i in range(0, n):
            x[i] = ((a*x0)+c) % m
            x0 = x[i]
            r[i] = x0 / m
        # llenamos nuestro DataFrame
        d = {'ri': r}
        dfMCL = pd.DataFrame(data=d)
        dfMCL
        max = x2['Max'].values
        min = x2['Min'].values

        def busqueda(arrmin, arrmax, valor):
            # print(valor)
            for i in range(len(arrmin)):
                # print(arrmin[i],arrmax[i])
                if valor >= arrmin[i] and valor <= arrmax[i]:
                    return i
                    # print(i)
            return -1
        xpos = dfMCL['ri']
        posi = [0] * n
        #print (n)
        for j in range(n):
            val = xpos[j]
            pos = busqueda(min, max, val)
            posi[j] = pos
        df1 = x2

        simula = []
        for j in range(n):
            for i in range(n):
                sim = x2.loc[salvando == posi[i]+1]
                simu = sim.filter(['Valores']).values
                iterator = itertools.chain(*simu)
                for item in iterator:
                    a = item
                simula.append(round(a, 2))
        dfMCL["Simulación"] = pd.DataFrame(simula)
        df2 = dfMCL
        return render_template('/metspages/metsim/montecarlo.html', form=form, tables=[df1.to_html(classes='data')], tables2=[df2.to_html(classes='data')], suma=suma, vald1=dfval[0],
                               cant=cant, dfprob=dfprob[0], page=page)
    else:
        N = None
        M = None
        A = None
        X0 = None
        C = None
        L = None
        grafica = None
        vald1 = None
        cant = None
        suma = None
        dfprob = None
    return render_template('/metspages/metsim/montecarlo.html', form=form, L=L, N=N, M=M, A=A, X0=X0, C=C, grafica=grafica, suma=suma, vald1=vald1, cant=cant, dfprob=dfprob, page=page)


@metsim_api.route('/montecarlomultiplicativo', methods=("POST", "GET"))
def montecarlo_multiplicativo():
    page = "montecarlomultiplicativo"

    class InputForm(Form):
        L = TextAreaField(
            label='Escriba los valores de ingreso separados por comas (,)',
            default='5501.0, 6232.7, 8118.3, 10137.00, 10449.50, 12794.60, 9939.10,  13193.00, 16036.2, 18496.90, 18709.30, 19363.50, 16521.50, 15175.40,  16927.00',
            validators=[validators.InputRequired()],
            render_kw=style)
        N = FloatField(
            label='Número de eventos que desea (n)', default=20,
            validators=[validators.InputRequired()],
            render_kw=style)
        M = FloatField(
            label='Módulo (m)', default=1000,
            validators=[validators.InputRequired()],
            render_kw=style)
        A = FloatField(
            label='Multiplicador (a)', default=747,
            validators=[validators.InputRequired()],
            render_kw=style)
        X0 = FloatField(
            label='Semilla (Xn)', default=123,
            validators=[validators.InputRequired()],
            render_kw=style)

    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        # datos experimentales
        # el DataFrame se llama movil
        prueba = str(form.L.data)
        ex = prueba.split(",")
        ex2 = list(map(float, ex))
        exporta = {'Año': ex2,
                   'Valores': ex2}
        a = pd.DataFrame(exporta)
        cant = len(a['Valores'])
        cantidad = list(range(cant + 1))
        cantidad[1:]
        a['Año'] = cantidad[1:]

        dfval = exporta['Valores']

        # Ordenamos por Día
        suma = a['Valores'].sum()
        n = len(exporta)
        suma
        x1 = a.assign(Probabilidad=lambda x: x['Valores'] / suma)
        x2 = x1.sort_values('Año')

        salvando = x2['Año']
        del x2['Año']
        a = x2['Probabilidad']
        a1 = np.cumsum(a)  # Cálculo la suma acumulativa de las probabilidades
        x2['FPA'] = a1
        x2['Min'] = x2['FPA']
        x2['Max'] = x2['FPA']
        lis = x2["Min"].values
        lis2 = x2['Max'].values
        lis[0] = 0
        for i in range(1, len(x2['Valores'])):
            lis[i] = lis2[i-1]
        x2['Min'] = lis

        dfprob = x2['Probabilidad']

        n = int(form.N.data)
        m = int(form.M.data)
        a = int(form.A.data)
        x0 = int(form.X0.data)
        # generador excel-03
        # - Xn+1 = (171Xn ) (mod 30264)
        x = [1] * n
        r = [0.1] * n
        for i in range(0, n):
            x[i] = (a*x0) % m
            x0 = x[i]
            r[i] = x0 / m
        # llenamos nuestro DataFrame
        d = {'ri': r}
        dfMCL = pd.DataFrame(data=d)
        dfMCL
        max = x2['Max'].values
        min = x2['Min'].values

        def busqueda(arrmin, arrmax, valor):
            # print(valor)
            for i in range(len(arrmin)):
                # print(arrmin[i],arrmax[i])
                if valor >= arrmin[i] and valor <= arrmax[i]:
                    return i
                    # print(i)
            return -1
        xpos = dfMCL['ri']
        posi = [0] * n
        #print (n)
        for j in range(n):
            val = xpos[j]
            pos = busqueda(min, max, val)
            posi[j] = pos
        df1 = x2

        simula = []
        for j in range(n):
            for i in range(n):
                sim = x2.loc[salvando == posi[i]+1]
                simu = sim.filter(['Valores']).values
                iterator = itertools.chain(*simu)
                for item in iterator:
                    a = item
                simula.append(round(a, 2))
        dfMCL["Simulación"] = pd.DataFrame(simula)
        df2 = dfMCL
        return render_template('/metspages/metsim/montecarlo.html', form=form, tables=[df1.to_html(classes='data')], tables2=[df2.to_html(classes='data')], suma=suma, vald1=dfval[0],
                               cant=cant, dfprob=dfprob[0], page=page)
    else:
        N = None
        M = None
        A = None
        X0 = None
        C = None
        L = None
        grafica = None
        vald1 = None
        cant = None
        suma = None
        dfprob = None
    return render_template('/metspages/metsim/montecarlo.html', form=form, L=L, N=N, M=M, A=A, X0=X0, C=C, grafica=grafica, suma=suma, vald1=vald1, cant=cant, dfprob=dfprob, page=page)


@metsim_api.route('/transinversaditivo', methods=("POST", "GET"))
def transformada_inversa_aditivo():
    page = "transinversaditivo"

    class InputForm(Form):
        L = FloatField(
            label='Ingrese el valor de landa', default=0.2,
            validators=[validators.InputRequired()])
        N = FloatField(
            label='Número de eventos que desea', default=20,
            validators=[validators.InputRequired()])
        M = FloatField(
            label='Módulo', default=1000,
            validators=[validators.InputRequired()])
        A = FloatField(
            label='Multiplicador', default=747,
            validators=[validators.InputRequired()])
        X0 = FloatField(
            label='Semilla', default=123,
            validators=[validators.InputRequired()])
        C = FloatField(
            label='Incremento', default=457,
            validators=[validators.InputRequired()])

    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        n = int(form.N.data)
        m = int(form.M.data)
        a = int(form.A.data)
        x0 = int(form.X0.data)
        c = int(form.C.data)
        x = [1] * n
        r = [0.1] * n
        for i in range(0, n):
            x[i] = ((a*x0)+c) % m
            x0 = x[i]
            r[i] = x0 / m
        # llenamos nuestro DataFrame
        d = {'Xn': x, 'ri': r}
        dfMCL = pd.DataFrame(data=d)
        landa = form.L.data
        dfexp = dfMCL['ri']
        # calculamos a todos los elementos la inversa
        exp_x = dfexp.values*(-1/landa)*np.log(dfexp)
        # anexamos al Datafram dfMCL
        dfMCL["Inversa"] = exp_x
        df = dfMCL

        dfgrafico = dfMCL.filter(items=['ri', 'Inversa'])
        dfgrafico.plot()
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

        return render_template('/metspages/metsim/transinversa.html', form=form, tables=[df.to_html(classes='data')], grafica=plotfile, page=page)
    else:
        N = None
        M = None
        A = None
        X0 = None
        C = None
        L = None
        grafica = None
    return render_template('/metspages/metsim/transinversa.html', form=form, L=L, N=N, M=M, A=A, X0=X0, C=C, grafica=grafica, page=page)


@metsim_api.route('/transinversamultiplicativo', methods=("POST", "GET"))
def transformada_inversa_multiplicativo():
    page = "transinversamultiplicativo"

    class InputForm(Form):
        L = FloatField(
            label='Ingrese el valor de landa', default=0.2,
            validators=[validators.InputRequired()])
        N = FloatField(
            label='Número de eventos que desea', default=20,
            validators=[validators.InputRequired()])
        M = FloatField(
            label='Módulo', default=1000,
            validators=[validators.InputRequired()])
        A = FloatField(
            label='Multiplicador', default=747,
            validators=[validators.InputRequired()])
        X0 = FloatField(
            label='Semilla', default=123,
            validators=[validators.InputRequired()])

    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        n = int(form.N.data)
        m = int(form.M.data)
        a = int(form.A.data)
        x0 = int(form.X0.data)
        x = [1] * n
        r = [0.1] * n
        for i in range(0, n):
            x[i] = (a*x0) % m
            x0 = x[i]
            r[i] = x0 / m
        d = {'Xn': x, 'ri': r}
        dfMCL = pd.DataFrame(data=d)
        landa = form.L.data
        dfexp = dfMCL['ri']
        # calculamos a todos los elementos la inversa
        exp_x = dfexp.values*(-1/landa)*np.log(dfexp)
        # anexamos al Datafram dfMCL
        dfMCL["Inversa"] = exp_x
        df = dfMCL

        dfgrafico = dfMCL.filter(items=['ri', 'Inversa'])
        dfgrafico.plot()
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

        return render_template('/metspages/metsim/transinversa.html', form=form, tables=[df.to_html(classes='data')], grafica=plotfile, page=page)
    else:
        N = None
        M = None
        A = None
        X0 = None
        L = None
        grafica = None
    return render_template('/metspages/metsim/transinversa.html', form=form, L=L, N=N, M=M, A=A, X0=X0, grafica=grafica, page=page)
