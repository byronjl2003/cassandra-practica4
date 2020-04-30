#!/bin/python3
from flask import Flask, request, url_for, render_template
import urllib
import time
import csv
from prueba import get_tikets_por_fechas,get_tikets_por_usuario_rango_fechas,insert
app = Flask(__name__)
@app.route('/')
def index():
    return render_template("index.html",autor1 = {"nombre":"Byron","apellido":"Lopez"},mensaje=('','',''))
@app.route('/otroget')
def otroget():
    print("otroget")
    print("jiji")
    return render_template("index.html",autor1 = {"nombre":"Walter","apellido":"Mendoza"},autor2 = {"nombre":"Byron","apellido":"Lopez"},mensaje=('','',''))


@app.route('/ticket', methods=['POST'])
def ticket():
   #return render_template("index.html",autor1 = {"nombre":"Walter","apellido":"Mendoza"},autor2 = {"nombre":"Byron","apellido":"Lopez"},mensaje=('','',''))
    print('LLEGO a ticket!!!!!!!!!!!!!!!!!')
    params = request.form
    params2 = request.data
    print(request)
    print(params)
    print(params2)
    return insert(params['fec'],params['correo'],params['titulo'],params['descripcion'])

@app.route('/reporte1', methods=['POST'])
def reporte1():
   #return render_template("index.html",autor1 = {"nombre":"Walter","apellido":"Mendoza"},autor2 = {"nombre":"Byron","apellido":"Lopez"},mensaje=('','',''))
    print('LLEGO a ticket!!!!!!!!!!!!!!!!!')
    params = request.form
    params2 = request.data
    print(request)
    print(params)
    #print(params2)
    #print(str(params[0]))
    #print(params[1])
    #return "..."+params['fec1']+params['fec2']
    return get_tikets_por_fechas(params['fec1'],params['fec2'])

@app.route('/reporte2', methods=['POST'])
def reporte2():
    print('LLEGO a reporte2!!!!!!!!!!!!!!!!!')
    params = request.form
    return get_tikets_por_usuario_rango_fechas(params['correo'],params['fec1'],params['fec2'])
    

def filtrar(data):
    global _coeficientes
    inp = Signal()
    #inp.generate(300, 10, sinoidal=True)
    inp.addy(data)
    #inp.generate()
    inp.generate(300, 10, sinoidal=True)
    filtro = Filter(_coeficientes)
    filtrado = filtro.filter(inp)
    # end TODO

    # La funcion graficar recibe la entrada original y el resultado de filtrar
    print("--------*--------------------")
    print(inp.t)
    print(inp.y)
    print("--------*--------------------")
    print(filtrado.t)
    print(filtrado.y)
    
    print(filtrado)
    return graficar(inp, filtrado)

    # si index detecta que img no es nulo la coloca con un nuevo div
    # para mostrarla en la pagina



def readcsv(filename):
    resp = []
    with open('./temporales/'+filename) as csv_file:
        
        csv_reader = csv.reader(csv_file, delimiter=',')
        #line_count = 0
        for row in csv_reader:
            resp.append(float(row[0]))
        
    return resp

def create_html_table(inforepo):
    a = '''
    <div class="table-wrapper">
    <table class="table table-striped table-sm">
        <thead>
            <tr>
                <th>{}</th>
                <th>{}</th>
                <th>{}</th>
                <th>{}</th>
                <th>{}</th>
                <th>{}</th>
                <th>{}</th>
                <th>{}</th>
                <th>{}</th>
                <th>{}</th>
                <th>{}</th>
                <th>{}</th>
                <th>{}</th>
                <th>{}</th>
                <th>{}</th>
                <th>{}</th>
                <th>{}</th>
                <th>{}</th>
            </tr>
        </thead>
                                
    </table>
    </div>
    '''.format(indi[0],indi[1],indi[2],indi[3],indi[4],indi[5],indi[6],indi[7],indi[8],indi[9],indi[10],indi[11],indi[12],indi[13],indi[14],indi[15],indi[16],indi[17])
    return a


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
