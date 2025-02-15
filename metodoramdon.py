import xlsxwriter
import matplotlib.pyplot as plt
from flask import Blueprint, Flask, render_template, make_response, request, send_file
from wtforms import Form, FloatField, validators, IntegerField
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


metodo_ramdon_api = Blueprint('metodo_ramdon_api', __name__)

style = {'class': 'form-control'}


@metodo_ramdon_api.route('/cuadmedio', methods=("POST", "GET"))
def cuadrado_medio():
    class InputForm(Form):
        N = IntegerField(
            label='Nº de iteraciones (N)',
            default=10,
            validators=[validators.InputRequired()],
            render_kw=style)
        R = IntegerField(
            label='Valor inicial o "semilla" (mínimo 3 dígitos) (R)',
            default=171,
            validators=[validators.InputRequired(
            ), validators.NumberRange(min=100)],
            render_kw=style)

    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        # Método de los cuadrados medios
        n = int(form.N.data)
        r = int(form.R.data)  # seleccionamos el valor inicial r
        reserva = int(form.R.data)
        l = len(str(r))  # determinamos el número de dígitos
        lista = []  # almacenamos en una lista
        lista2 = []
        i = 1
        # while len(lista) == len(set(lista)):
        while i <= n:
            x = str(r*r)  # Elevamos al cuadrado r
            if l % 2 == 0:
                x = x.zfill(l*2)
            else:
                x = x.zfill(l)
            y = (len(x)-l)/2
            y = int(y)
            r = int(x[y:y+l])
            lista.append(r)
            lista2.append(x)
            i = i+1

        df = pd.DataFrame({'Valores elevados': lista2, 'Valor medio': lista})
        dfres = df['Valores elevados']
        dfres2 = df['Valor medio']
        reserva2 = dfres[0]
        reserva3 = dfres2[0]
        dfrac = df["Valor medio"]/10**l
        df["Valor random"] = dfrac
        reserva4 = dfrac[0]
        x1 = df['Valor random']
        plt.plot(x1)
        plt.title('Generador de Numeros Aleatorios Cuadrados Medios')
        plt.xlabel('Serie')
        plt.ylabel('Aleatorios')
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
        return render_template('/metspages/metran/cuadmedio.html', form=form, tables=[df.to_html(classes='table table-hover')], grafica=plotfile, N=n, R=r,
                               res=reserva, res2=reserva2, res3=reserva3, res4=reserva4, res5=l)
    else:
        N = None
        R = None
        reserva = 0
        reserva2 = 0
        reserva3 = 0
        reserva4 = 0
        res5 = 0
    return render_template('/metspages/metran/cuadmedio.html', form=form, N=N, R=R, res=reserva, res2=reserva2, res3=reserva3, res4=reserva4, res5=res5)


@metodo_ramdon_api.route('/congaditivo', methods=("POST", "GET"))
def congruencial_aditivo():
    class InputForm(Form):
        X0 = IntegerField(
            label='Semilla (Xn)', default=4,
            validators=[validators.InputRequired()],
            render_kw=style)
        A = IntegerField(
            label='Multiplicador (a)', default=101,
            validators=[validators.InputRequired()],
            render_kw=style)
        C = IntegerField(
            label='Incremento (c)', default=457,
            validators=[validators.InputRequired()],
            render_kw=style)
        M = IntegerField(
            label='Módulo (m)', default=1000,
            validators=[validators.InputRequired()],
            render_kw=style)
        N = IntegerField(
            label='Nº de iteraciones (n)', default=20,
            validators=[validators.InputRequired()],
            render_kw=style)
    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        # Generador de números aleatorios Congruencia lineal
        n = int(form.N.data)
        m = int(form.M.data)
        a = int(form.A.data)
        x0 = int(form.X0.data)
        c = int(form.C.data)
        resv1 = n
        resv2 = m
        resv3 = a
        resv4 = x0
        resv5 = c
        x = [1] * n
        r = [0.1] * n
        for i in range(0, n):
            x[i] = ((a*x0)+c) % m
            x0 = x[i]
            r[i] = x0 / m
        # llenamos nuestro DataFrame
        d = {'Número generado': x, 'Valor random': r}
        dftemp1 = d['Número generado']
        dftemp2 = d['Valor random']
        resv6 = dftemp1[0]
        resv7 = dftemp2[0]
        resv8 = ((resv6*a)+c)
        resv9 = dftemp1[1]
        resv10 = dftemp2[1]
        df = pd.DataFrame(data=d)
        plt.plot(r, marker='o')
        plt.title('Generador de Numeros Aleatorios ')
        plt.xlabel('Serie')
        plt.ylabel('Aleatorios')
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
        return render_template('/metspages/metran/congaditivo.html', form=form, tables=[df.to_html(classes='table table-hover')], grafica=plotfile,
                               N=resv1, M=resv2, A=resv3, X0=resv4, C=resv5, res1=resv6, res2=resv7, res3=resv8, res4=resv9, res5=resv10)
    else:
        N = None
        M = None
        A = None
        X0 = None
        C = None
        resv6 = None
        resv7 = None
        resv8 = None
        resv9 = None
        resv10 = None
    return render_template('/metspages/metran/congaditivo.html', form=form, N=N, M=M, A=A, X0=X0, C=C, res1=resv6, res2=resv7, res3=resv8, res4=resv9, res5=resv10)


@metodo_ramdon_api.route('/congmultiplicativo', methods=("POST", "GET"))
def congruencial_multiplicativo_autogenerado():
    page = "congmultiplicativo"

    class InputForm(Form):
        X0 = IntegerField(
            label='Semilla (Xn)', default=123,
            validators=[validators.InputRequired()],
            render_kw=style)
        A = IntegerField(
            label='Multiplicador (a)', default=747,
            validators=[validators.InputRequired()],
            render_kw=style)
        M = IntegerField(
            label='Módulo (m)', default=1000,
            validators=[validators.InputRequired()],
            render_kw=style)
        N = IntegerField(
            label='Nº de iteraciones (n)', default=20,
            validators=[validators.InputRequired()],
            render_kw=style)

    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        # Generador de números aleatorios Congruencia lineal
        n = int(form.N.data)
        m = int(form.M.data)
        a = int(form.A.data)
        x0 = int(form.X0.data)

        resv1 = n
        resv2 = m
        resv3 = a
        resv4 = x0
        # generador excel-03
        # - Xn+1 = (171Xn ) (mod 30264)
        x = [1] * n
        r = [0.1] * n
        for i in range(0, n):
            x[i] = (a*x0) % m
            x0 = x[i]
            r[i] = x0 / m
        d = {'Número generado': x, 'Valor random': r}

        dftemp1 = d['Número generado']
        dftemp2 = d['Valor random']
        resv6 = dftemp1[0]
        resv7 = dftemp2[0]
        resv8 = (resv6*a)
        resv9 = dftemp1[1]
        resv10 = dftemp2[1]

        df = pd.DataFrame(data=d)
        plt.plot(r, 'g-', marker='o',)
        plt.title('Generador de Numeros Aleatorios ')
        plt.xlabel('Serie')
        plt.ylabel('Aleatorios')
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

        return render_template('/metspages/metran/congmultiplicativo.html', form=form, tables=[df.to_html(classes='table table-hover')],
                               grafica=plotfile, N=resv1, M=resv2, A=resv3, X0=resv4, res1=resv6, res2=resv7, res3=resv8, res4=resv9, res5=resv10, page=page)
    else:
        N = None
        M = None
        A = None
        X0 = None
        resv6 = None
        resv7 = None
        resv8 = None
        resv9 = None
        resv10 = None
    return render_template('/metspages/metran/congmultiplicativo.html', form=form, N=N, M=M, A=A, X0=X0, res1=resv6, res2=resv7, res3=resv8, res4=resv9, res5=resv10, page=page)


@metodo_ramdon_api.route('/congmultiplicativo30264', methods=("POST", "GET"))
def congruencial_multiplicativo_30264():
    page = "congmultiplicativo30264"

    class InputForm(Form):
        X0 = IntegerField(
            label='Semilla (Xn)', default=123,
            validators=[validators.InputRequired()],
            render_kw=style)
        N = IntegerField(
            label='Nº de iteraciones (n)', default=20,
            validators=[validators.InputRequired()],
            render_kw=style)

    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        # Generador de números aleatorios Congruencia lineal
        n = int(form.N.data)
        x0 = int(form.X0.data)
        m, a = 1000, 171

        resv1 = n
        resv2 = m
        resv3 = a
        resv4 = x0
        # generador excel-03
        # - Xn+1 = (171Xn ) (mod 30264)
        x = [1] * n
        r = [0.1] * n
        for i in range(0, n):
            x[i] = (a*x0) % m
            x0 = x[i]
            r[i] = x0 / m
        d = {'Número generado': x, 'Valor random': r}

        dftemp1 = d['Número generado']
        dftemp2 = d['Valor random']
        resv6 = dftemp1[0]
        resv7 = dftemp2[0]
        resv8 = (resv6*a)
        resv9 = dftemp1[1]
        resv10 = dftemp2[1]

        df = pd.DataFrame(data=d)
        plt.plot(r, 'g-', marker='o',)
        plt.title('Generador de Numeros Aleatorios ')
        plt.xlabel('Serie')
        plt.ylabel('Aleatorios')
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

        return render_template('/metspages/metran/congmultiplicativo.html', form=form, tables=[df.to_html(classes='table table-hover')],
                               grafica=plotfile, N=resv1, M=resv2, A=resv3, X0=resv4, res1=resv6, res2=resv7, res3=resv8, res4=resv9, res5=resv10, page=page)
    else:
        N = None
        M = None
        A = None
        X0 = None
        resv6 = None
        resv7 = None
        resv8 = None
        resv9 = None
        resv10 = None
    return render_template('/metspages/metran/congmultiplicativo.html', form=form, N=N, M=M, A=A, X0=X0, res1=resv6, res2=resv7, res3=resv8, res4=resv9, res5=resv10, page=page)


@metodo_ramdon_api.route('/congmultiplicativo30307', methods=("POST", "GET"))
def congruencial_multiplicativo_30307():
    page = "congmultiplicativo30307"

    class InputForm(Form):
        X0 = IntegerField(
            label='Semilla (Xn)', default=123,
            validators=[validators.InputRequired()],
            render_kw=style)
        N = IntegerField(
            label='Nº de iteraciones (n)', default=20,
            validators=[validators.InputRequired()],
            render_kw=style)

    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        # Generador de números aleatorios Congruencia lineal
        n = int(form.N.data)
        x0 = int(form.X0.data)
        m, a = 30307, 172

        resv1 = n
        resv2 = m
        resv3 = a
        resv4 = x0

        x = [1] * n
        r = [0.1] * n
        for i in range(0, n):
            x[i] = (a*x0) % m
            x0 = x[i]
            r[i] = x0 / m
        d = {'Número generado': x, 'Valor random': r}

        dftemp1 = d['Número generado']
        dftemp2 = d['Valor random']
        resv6 = dftemp1[0]
        resv7 = dftemp2[0]
        resv8 = (resv6*a)
        resv9 = dftemp1[1]
        resv10 = dftemp2[1]

        df = pd.DataFrame(data=d)
        plt.plot(r, 'g-', marker='o',)
        plt.title('Generador de Numeros Aleatorios ')
        plt.xlabel('Serie')
        plt.ylabel('Aleatorios')
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

        return render_template('/metspages/metran/congmultiplicativo.html', form=form, tables=[df.to_html(classes='table table-hover')],
                               grafica=plotfile, N=resv1, M=resv2, A=resv3, X0=resv4, res1=resv6, res2=resv7, res3=resv8, res4=resv9, res5=resv10, page=page)
    else:
        N = None
        M = None
        A = None
        X0 = None
        resv6 = None
        resv7 = None
        resv8 = None
        resv9 = None
        resv10 = None
    return render_template('/metspages/metran/congmultiplicativo.html', form=form, N=N, M=M, A=A, X0=X0, res1=resv6, res2=resv7, res3=resv8, res4=resv9, res5=resv10, page=page)


@metodo_ramdon_api.route('/congmultiplicativo30323', methods=("POST", "GET"))
def congruencial_multiplicativo_30323():
    page = "congmultiplicativo30323"

    class InputForm(Form):
        X0 = IntegerField(
            label='Semilla (Xn)', default=123,
            validators=[validators.InputRequired()],
            render_kw=style)
        N = IntegerField(
            label='Nº de iteraciones (n)', default=20,
            validators=[validators.InputRequired()],
            render_kw=style)

    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        # Generador de números aleatorios Congruencia lineal
        n = int(form.N.data)
        x0 = int(form.X0.data)
        m, a = 30323, 170

        resv1 = n
        resv2 = m
        resv3 = a
        resv4 = x0

        x = [1] * n
        r = [0.1] * n
        for i in range(0, n):
            x[i] = (a*x0) % m
            x0 = x[i]
            r[i] = x0 / m
        d = {'Número generado': x, 'Valor random': r}

        dftemp1 = d['Número generado']
        dftemp2 = d['Valor random']
        resv6 = dftemp1[0]
        resv7 = dftemp2[0]
        resv8 = (resv6*a)
        resv9 = dftemp1[1]
        resv10 = dftemp2[1]

        df = pd.DataFrame(data=d)
        plt.plot(r, 'g-', marker='o',)
        plt.title('Generador de Numeros Aleatorios ')
        plt.xlabel('Serie')
        plt.ylabel('Aleatorios')
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

        return render_template('/metspages/metran/congmultiplicativo.html', form=form, tables=[df.to_html(classes='table table-hover')],
                               grafica=plotfile, N=resv1, M=resv2, A=resv3, X0=resv4, res1=resv6, res2=resv7, res3=resv8, res4=resv9, res5=resv10, page=page)
    else:
        N = None
        M = None
        A = None
        X0 = None
        resv6 = None
        resv7 = None
        resv8 = None
        resv9 = None
        resv10 = None
    return render_template('/metspages/metran/congmultiplicativo.html', form=form, N=N, M=M, A=A, X0=X0, res1=resv6, res2=resv7, res3=resv8, res4=resv9, res5=resv10, page=page)
