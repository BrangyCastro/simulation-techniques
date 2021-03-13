import random
import io


from flask import Flask, render_template, make_response
from metodoramdon import metodo_ramdon_api
from metodopronostico import metodo_pronostico_api
from metodoregresion import metodo_regresion_api
from metodosimulacion import metodo_simulacion_api
from modelosimulacion import modelo_simulacion_api
from vidareal import vida_real_api
from estadistico import estadistico_api

app = Flask(__name__)

app.register_blueprint(metodo_ramdon_api)
app.register_blueprint(metodo_pronostico_api)
app.register_blueprint(metodo_regresion_api)
app.register_blueprint(metodo_simulacion_api)
app.register_blueprint(modelo_simulacion_api)
app.register_blueprint(vida_real_api)
app.register_blueprint(estadistico_api)


@app.route('/')
def home():
    return render_template('random.html', page="index")


@app.route('/pronostico')
def pronostico():
    return render_template('pronostico.html', page="index2")


@app.route('/regresion')
def regresion():
    return render_template('regresion.html', page="index3")


@app.route('/simulacion')
def simulacion():
    return render_template('simulacion.html', page="index4")


@app.route('/index5')
def index5():
    return render_template('index5.html', page="index5")


if __name__ == '__main__':
    app.run(debug=True)
