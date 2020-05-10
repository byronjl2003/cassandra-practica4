#!/bin/python3
from flask import Flask, request, url_for, render_template,jsonify
#import urllib
import time
import json
import logging
from prueba import cassandra_insert_paises,cassandra_get_paises,cassandra_insert_patentes_masivos,cassandra_get_inventores,cassandra_get_areas,cassandra_get_colaboradores_por_area,cassandra_insert_pais,cassandra_insert_colaborador,cassandra_insert_patentes,cassandra_get_reporte1,cassandra_get_reporte2,cassandra_get_inventor_nombre,cassandra_get_reporte3
##########
listafronteras = []
#------------
###############
listaareascolaborador = []
#------------
listica = []
listainventores = []
listacolaboradores = []
#####
app = Flask(__name__)
@app.route('/')
def index():
    countryes = cassandra_get_paises()
    #print(countryes[0])
    inventors = cassandra_get_inventores()
    areass = cassandra_get_areas()
    global listica
    global listacolaboradores
    global listainventores
    listica = []
    listacolaboradores = []
    listainventores = []
    return render_template("index.html",autor1 = {"nombre":"Byron","apellido":"Lopez"},paises=countryes,inventores=inventors,areas=areass)
#################################################################
@app.route('/indexpaises')
def indexpaises():
    countryes = cassandra_get_paises()
    global listafronteras
    listafronteras = []
    return render_template("paises.html",autor1 = {"nombre":"Byron","apellido":"Lopez"},paises=countryes)

@app.route('/reporte1')
def reporte1():
    countryes = cassandra_get_paises()
    return render_template("reporte1.html",autor1 = {"nombre":"Byron","apellido":"Lopez"},paises=countryes)

@app.route('/reporte2')
def reporte2():
    inventors = cassandra_get_inventores()
    return render_template("reporte2.html",autor1 = {"nombre":"Byron","apellido":"Lopez"},inventores=inventors)

@app.route('/reporte3')
def reporte3():
    areass = cassandra_get_areas()
    return render_template("reporte3.html",autor1 = {"nombre":"Byron","apellido":"Lopez"},areas=areass)



@app.route('/setfrontera', methods=['POST'])
def setfrontera():
   #return render_template("index.html",autor1 = {"nombre":"Walter","apellido":"Mendoza"},autor2 = {"nombre":"Byron","apellido":"Lopez"},mensaje=('','',''))
    print('LLEGO a set_frontera!!!')
    global listafronteras
    params = request.form
    
    print(params)
    listafronteras.append(params['frontera'].encode('utf-8'))
    print(listafronteras)
    print('')
    return params['frontera']


@app.route('/postpais', methods=['POST'])
def postpais():
   #return render_template("index.html",autor1 = {"nombre":"Walter","apellido":"Mendoza"},autor2 = {"nombre":"Byron","apellido":"Lopez"},mensaje=('','',''))
    print('LLEGO a postpais!!!')
    global listafronteras
    params = request.form
    return cassandra_insert_pais(
        listafronteras,
        params['nombre'].encode('utf-8'),
        params['area'].encode('utf-8'),
        params['alpha2'].encode('utf-8'),
        params['alpha3'].encode('utf-8'),
        params['latitud'].encode('utf-8'),
        params['longitud'].encode('utf-8'),
        params['poblacion'].encode('utf-8')) 
    



######################TERMINA INGRESO DE PAIS##########################################################
#-------------EMPIEZA INGRESO DE COLABORADORES-------------------------------------------------
@app.route('/indexcolaboradores')
def indexcolaboradores():
    areass = cassandra_get_areas()
    global listaareascolaborador
    listaareascolaborador = []
    return render_template("colaboradores.html",autor1 = {"nombre":"Byron","apellido":"Lopez"},areas=areass)

@app.route('/setareacolaborador', methods=['POST'])
def setareacolaborador():
   #return render_template("index.html",autor1 = {"nombre":"Walter","apellido":"Mendoza"},autor2 = {"nombre":"Byron","apellido":"Lopez"},mensaje=('','',''))
    print('LLEGO a set_area_colaborador!!!')
    global listaareascolaborador
    params = request.form
    
    print(params)
    listaareascolaborador.append(params['area'].encode('utf-8'))
    print(listaareascolaborador)
    print('')
    return params['area']


@app.route('/postcolaborador', methods=['POST'])
def postcolaborador():
   #return render_template("index.html",autor1 = {"nombre":"Walter","apellido":"Mendoza"},autor2 = {"nombre":"Byron","apellido":"Lopez"},mensaje=('','',''))
    print('LLEGO a postcolaborador!!!')
    global listaareascolaborador
    params = request.form
    return cassandra_insert_colaborador(
        listaareascolaborador,
        params['comision'].encode('utf-8'),
        params['fec_inicio'].encode('utf-8'),
        params['nombre'].encode('utf-8'),
        params['salario'].encode('utf-8'))
    






##############################TERMINA INGRESO COLABORADORES
###############EMPIEZA LO DE LAS PATENTES####################
@app.route('/set_inventorespatente', methods=['POST'])
def set_inventorespatente():
    print('LLEGO a set_inventorespatente!!!')
    global listainventores
    params = request.form
    params2 = request.data
    #print(request)
    print(params)
    #print(params2)
    #print(str(params[0]))
    #print(params[1])
    listainventores.append(params['inventores'].encode('utf-8'))
    print(listainventores)
    
    #colaboradores = cassandra_get_colaboradores_por_area(listica)
    
    return params['inventores']



@app.route('/get_colaboradores', methods=['POST'])
def get_colaboradores():
   #return render_template("index.html",autor1 = {"nombre":"Walter","apellido":"Mendoza"},autor2 = {"nombre":"Byron","apellido":"Lopez"},mensaje=('','',''))
    print('LLEGO a get_colaboradores!!!')
    global listica
    params = request.form
    params2 = request.data
    #print(request)
    print(params)
    #print(params2)
    #print(str(params[0]))
    #print(params[1])
    listica.append(params['areas'].encode('utf-8'))
    print(listica)
    
    colaboradores = cassandra_get_colaboradores_por_area(listica)
    
    return html_colaboradores(colaboradores)

    
def html_colaboradores(colaboradores):
    resp = ''
    for colabs in colaboradores:
        resp += '<option value="'+ colabs.id_colaborador+'">'+colabs.nombre+'</option>'
    
    return resp

@app.route('/set_colaboradorespatente', methods=['POST'])
def set_colaboradorespatente():
    print('LLEGO a set_inventorespatente!!!')
    global listacolaboradores
    params = request.form
    params2 = request.data
    #print(request)
    print(params)
    #print(params2)
    #print(str(params[0]))
    #print(params[1])
    listacolaboradores.append(params['colaboradores'].encode('utf-8'))
    print(listainventores)
    
    #colaboradores = cassandra_get_colaboradores_por_area(listica)
    
    return params['colaboradores']


@app.route('/setpatente', methods=['POST'])
def setpatente():
    print('LLEGO a set_inventorespatente!!!')
    global listacolaboradores
    global listica
    global listainventores 

    params = request.form
    params2 = request.data
    
    print(params)
    
    #colaboradores = cassandra_get_colaboradores_por_area(listica)
    #el nombre del la patente
    nombre_patente = params['nombre']
    descripcion = params['descripcion']
    fec_presentacion = params['fec_presentacion']
    #el pais si lo recupero
    id_pais = params['id_pais']
    return cassandra_insert_patentes(nombre_patente,descripcion,fec_presentacion,id_pais,listica,listainventores,listacolaboradores)



@app.route('/getreporte1', methods=['POST'])
def getreporte1():
    params = request.form
    print(params)
    id_pais = params['id_pais']
    iterator = cassandra_get_reporte1(id_pais)
    return tabla_reporte1(iterator)

@app.route('/getreporte2', methods=['POST'])
def getreporte2():
    params = request.form
    print(params)
    id_inventor = params['id_inventor']
    nombre_inventor = cassandra_get_inventor_nombre(id_inventor)
    iterator = cassandra_get_reporte2(id_inventor,nombre_inventor)
    return tabla_reporte2(iterator)


@app.route('/getreporte3', methods=['POST'])
def getreporte3():
    params = request.form
    print(params)
    id_area = params['id_area']
    #nombre_inventor = cassandra_get_inventor_nombre(id_inventor)
    iterator = cassandra_get_reporte3(id_area)
    return tabla_reporte3(iterator)



def tabla_reporte3(iterator):
    a = '''
    <div class="table-wrapper">
    <table class="table table-striped table-sm">
        <thead>
            <tr>
                <th>id_invento</th>
                <th>nombre</th>
                <th>area</th>
                <th>nombre_area</th>
                <th>descripcion</th>
                <th>fec_presentacion</th>
                <th>id_pais</th>
                <th>pais</th>
               <th>colaboradores</th>
                <th>inventores</th>
                
            </tr>
        </thead>
        <tbody>
    '''
    for data in iterator:
        try:
            a += '''
            <tr>
             
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
               <td>{}</td>
                <td>{}</td>
                
            </tr>
        
        '''.format(data.id_invento,data.nombre,data.area,data.nombre_area,data.descripcion,data.fec_presentacion,data.id_pais,data.pais,data.colaboradores,data.inventores)
        except:
            print("Aalso sucedio...")
    a += '''
    </tbody>                            
    </table>
    </div>
    '''
            
        
    return a






def tabla_reporte2(iterator):
    a = '''
    <div class="table-wrapper">
    <table class="table table-striped table-sm">
        <thead>
            <tr>
                <th>id_inventor</th>
                <th>nombre_inventor</th>
                <th>id_invento</th>
                <th>nombre</th>
                <th>descripcion</th>
                <th>fec_presentacion</th>
                
                <th>id_pais</th>
                <th>pais</th>
                <th>nacionalidad</th>
                <th>sexo</th>
                <th>fec_nac</th>
                <th>colaboradores</th>
                <th>area</th>
                
            </tr>
        </thead>
        <tbody>
    '''
    for data in iterator:
        a += '''
            <tr>
             <th>{}</th>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
                <td></td>
                <td></td>
                
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
            </tr>
        
        '''.format(data.id_inventor,data.nombre_inventor,data.id_invento,data.nombre,data.descripcion,data.fec_presentacion,data.id_pais,data.pais,data.nacionalidad,data.sexo,data.fec_nac,data.colaboradores,data.area)
    
    a += '''
    </tbody>                            
    </table>
    </div>
    '''
    return a



def tabla_reporte1(iterator):
    a = '''
    <div class="table-wrapper">
    <table class="table table-striped table-sm">
        <thead>
            <tr>
                <th>id_pais</th>
                <th>nombre_pais</th>
                <th>id_invento</th>
                <th>nombre</th>
                <th>descripcion</th>
                <th>fec_presentacion</th>
                <th>area</th>
                               
                <th>colaboradores</th>
                <th>inventores</th>
                
            </tr>
        </thead>
        <tbody>
    '''
    for data in iterator:
        a += '''
            <tr>
             <th>{}</th>
                <th>{}</th>
                <th>{}</th>
                <th>{}</th>
                <th></th>
                <th>{}</th>
                <th>{}</th>
                               
                <th>{}</th>
                <th>{}</th>
            </tr>
        
        '''.format(data.id_pais,data.nombre_pais,data.id_invento,data.nombre,data.descripcion,data.fec_presentacion,data.area,data.colaboradores,data.inventores)
    
    a += '''
    </tbody>                            
    </table>
    </div>
    '''
    return a

@app.route('/cargas')
def cargas():
    return render_template("cargas.html",autor1 = {"nombre":"Byron","apellido":"Lopez"},mensaje=('','',''))


@app.route('/paises', methods=['POST'])
def post_paises():
   #return render_template("index.html",autor1 = {"nombre":"Walter","apellido":"Mendoza"},autor2 = {"nombre":"Byron","apellido":"Lopez"},mensaje=('','',''))
    print('LLEGO a cargar paises')
    files = request.files
    fl = files.listvalues()
    print(fl)

    for f  in fl:
        for f2 in f:
            rec = 'temporales/' + f2.filename
            f2.save(rec)
            return cassandra_insert_paises('temporales/' + f2.filename)


@app.route('/carga_patentes', methods=['POST'])
def post_patentes():
   #return render_template("index.html",autor1 = {"nombre":"Walter","apellido":"Mendoza"},autor2 = {"nombre":"Byron","apellido":"Lopez"},mensaje=('','',''))
    print('LLEGO a cargar patentes')
    files = request.files
    fl = files.listvalues()
    #print(fl)

    for f  in fl:
        for f2 in f:
            rec = 'temporales/' + f2.filename
            f2.save(rec)
            return cassandra_insert_patentes_masivos('temporales/' + f2.filename)



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
