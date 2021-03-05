import random
import io


from flask import Flask, render_template, make_response
from metsim import metsim_api
from metran import metran_api
from modsim import modsim_api
from metprob import metprob_api
from metreg import metreg_api


app = Flask(__name__)

app.register_blueprint(metsim_api)
app.register_blueprint(metran_api)
app.register_blueprint(modsim_api)
app.register_blueprint(metprob_api)
app.register_blueprint(metreg_api)

@app.route('/')
def home():
    return render_template('index.html', page="index")

@app.route('/index2')
def index2():
    return render_template('index2.html', page="index2")
    
@app.route('/index3')
def index3():
    return render_template('index3.html', page="index3")
    
@app.route('/index4')
def index4():
    return render_template('index4.html', page="index4")
    
@app.route('/index5')
def index5():
    return render_template('index5.html', page="index5")


if __name__ == '__main__':
    app.run()