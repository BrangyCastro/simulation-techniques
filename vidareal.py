import matplotlib.pyplot as plt
from flask import Blueprint, Flask, render_template, make_response, request, send_file
from wtforms import Form, FloatField, validators, StringField, IntegerField
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
matplotlib.use('Agg')

vida_real_api = Blueprint('vida_real_api', __name__)

style = {'class': 'form-control', "rows": 3}


@vida_real_api.route('/vida-real', methods=("POST", "GET"))
def vida_real():
    page = "index6"

    class InputForm(Form):
        CH = IntegerField(
            label='Número de personas en espera', default=10,
            validators=[validators.InputRequired()],
            render_kw=style)
        D = FloatField(
            label='\( Landa \ \lambda \)', default=3.00,
            validators=[validators.InputRequired()],
            render_kw=style)
        CO = FloatField(
            label='\( Nu \ \mu \)', default=5.50,
            validators=[validators.InputRequired()],
            render_kw=style)

    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():

        D = float(form.D.data)
        Co = float(form.CO.data)
        Ch = int(form.CH.data)

        landa = D
        nu = Co
        # La probabilidad de hallar el sistema ocupado o utilización del sistema:
        𝑝 = landa/nu
        # La probabilidad de que no haya unidades en el sistema este vacía u ocioso :
        𝑃o = 1.0 - (landa/nu)
        # Longitud esperada en cola, promedio de unidades en la línea de espera:
        𝐿𝑞 = landa*landa / (nu * (nu - landa))
        # / (nu * (nu - landa))
        # Número esperado de clientes en el sistema(cola y servicio) :
        𝐿 = landa / (nu - landa)
        # El tiempo promedio que una unidad pasa en el sistema:
        𝑊 = 1 / (nu - landa)
        # Tiempo de espera en cola:
        𝑊𝑞 = W - (1.0 / nu)

        # La probabilidad de que haya n unidades en el sistema:
        n = 1
        𝑃𝑛 = (landa/nu)*𝑛*𝑃o

        dato1 = round(landa, 3)
        dato2 = round(p, 3)
        dato3 = round(Po, 3)
        dato4 = round(Lq, 3)
        dato5 = round(L, 1)
        dato6 = round(W, 3)
        dato7 = round(Wq, 3)
        dato8 = round(Pn, 3)

        i = 0
        # Landa y nu ya definidos
        # Atributos del DataFrame
        """
        ALL # ALEATORIO DE LLEGADA DE CLIENTES
        ASE # ALEATORIO DE SERVICIO
        TILL TIEMPO ENTRE LLEGADA
        TISE TIEMPO DE SERVICIO
        TIRLL TIEMPO REAL DE LLEGADA
        TIISE TIEMPO DE INICIO DE SERVICIO
        TIFSE TIEMPO FINAL DE SERVICIO
        TIESP TIEMPO DE ESPERA
        TIESA TIEMPO DE SALIDA
        numClientes NUMERO DE CLIENTES
        dfLE DATAFRAME DE LA LINEA DE ESPERA
        """
        numClientes = Ch
        i = 0
        indice = ['ALL', 'ASE', 'TILL', 'TISE',
                  'TIRLL', 'TIISE', 'TIFSE', 'TIESP', 'TIESA']
        Clientes = np.arange(numClientes)
        dfLE = pd.DataFrame(index=Clientes, columns=indice).fillna(0.000)
        np.random.seed(100)
        for i in Clientes:
            if i == 0:
                dfLE['ALL'][i] = random.random()
                dfLE['ASE'][i] = random.random()
                dfLE['TILL'][i] = -1/landa*np.log(dfLE['ALL'][i])
                dfLE['TISE'][i] = -1/nu*np.log(dfLE['ASE'][i])
                dfLE['TIRLL'][i] = dfLE['TILL'][i]
                dfLE['TIISE'][i] = dfLE['TIRLL'][i]
                dfLE['TIFSE'][i] = dfLE['TIISE'][i] + dfLE['TISE'][i]
                dfLE['TIESA'][i] = dfLE['TIESP'][i] + dfLE['TISE'][i]
            else:
                dfLE['ALL'][i] = random.random()
                dfLE['ASE'][i] = random.random()
                dfLE['TILL'][i] = -1/landa*np.log(dfLE['ALL'][i])
                dfLE['TISE'][i] = -1/nu*np.log(dfLE['ASE'][i])
                dfLE['TIRLL'][i] = dfLE['TILL'][i] + dfLE['TIRLL'][i-1]
                dfLE['TIISE'][i] = max(dfLE['TIRLL'][i], dfLE['TIFSE'][i-1])
                dfLE['TIFSE'][i] = dfLE['TIISE'][i] + dfLE['TISE'][i]
                dfLE['TIESP'][i] = dfLE['TIISE'][i] - dfLE['TIRLL'][i]
                dfLE['TIESA'][i] = dfLE['TIESP'][i] + dfLE['TISE'][i]
        nuevas_columnas = pd.core.indexes.base.Index(["A_LLEGADA", "A_SERVICIO", "TIE_LLEGADA", "TIE_SERVICIO",
                                                      "TIE_EXACTO_LLEGADA", "TIE_INI_SERVICIO", "TIE_FIN_SERVICIO",
                                                      "TIE_ESPERA", "TIE_EN_SISTEMA"])
        dfLE.columns = nuevas_columnas
        df = dfLE
        df2 = dfLE.describe()

        dfLE.plot()

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

        return render_template('/vida-real.html', form=form, tables=[df.to_html(classes='data')], tables2=[df2.to_html(classes='data')], grafica=plotfile, dato1=dato1,
                               dato2=dato2, dato3=dato3, dato4=dato4, dato5=dato5, dato6=dato6, dato7=dato7, dato8=dato8, page=page)
    else:
        D = None
        CO = None
        CH = None
    return render_template('/vida-real.html', form=form, D=D, CO=CO, CH=CH, page=page)
