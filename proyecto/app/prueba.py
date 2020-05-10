#!/usr/bin/env python

#import logging

#log = logging.getLogger()
#log.setLevel('DEBUG')
#handler = logging.StreamHandler()
#handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
#log.addHandler(handler)
import time
from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from cassandra.util import uuid_from_time
import json
import random
KEYSPACE = "cpm"
'''
REATE TABLE cpm.paises (
    alpha2 text,
    alpha3 text,
    area float,
    fronteras list<text>,
    latlng list<float>,
    nombre text,
    poblacion int,
    PRIMARY KEY (alpha2, alpha3)
) WITH CLUSTERING ORDER BY (alpha3 ASC)
'''
def cassandra_insert_paises(path):
    cluster = Cluster(['master'],protocol_version = 3)
    session = cluster.connect()
    query = SimpleStatement(
    
        "INSERT INTO cpm.paises(nombre,area,alpha2,alpha3,latlng,poblacion,fronteras)values(%s,%s,%s,%s,%s,%s,%s)",
        consistency_level=ConsistencyLevel.QUORUM)
    
    with open(path) as f:
        data = json.load(f)
        for pais in data:
            session.execute(query, (pais['name'],pais['area'],pais['alpha2Code'],pais['alpha3Code'],pais['latlng'],pais['population'],pais['borders']))
    return "OK"

def crear_mapa_colaboradores(ids_colaboradores):
    resp = []
    cluster = Cluster(['master'],protocol_version = 3)
    session = cluster.connect()
    for id_colaborador in  ids_colaboradores:
        dic = {}
        future = session.execute("select  * from cpm.colaboradores where id_colaborador=%s",[id_colaborador])
        for row in future:
            dic['id_colaborador'] = id_colaborador
            dic['nombre'] = row.nombre
            dic['fec_inicio'] = str(row.fec_inicio)
            dic['salario'] = str(row.salario)
            dic['comision'] = str(row.comision)
            break
        resp.append(dic)
    return resp

def crear_mapa_inventores(ids_inventores):
    resp = []
    cluster = Cluster(['master'],protocol_version = 3)
    session = cluster.connect()
    for id_inventor in  ids_inventores:
        dic = {}
        future = session.execute("select  * from cpm.inventores where id_inventor=%s",[id_inventor])
        for row in future:
            dic['id_inventor'] = id_inventor
            dic['nombre'] = row.nombre
            dic['alpha2'] = row.alpha2
            dic['pais'] = row.pais
            break
        resp.append(dic)
    return resp


def cassandra_insert_patentes(nombre_patente,descripcion,fec_presentacion,id_pais,listaareas,listainventores,listacolaboradores,idmasivo=None):
    #FIJO EN TODAS VAN LA LISTA DE MAPAS DE LOS COLABORADORES..ARMEMOLA
    colaboradores = crear_mapa_colaboradores(listacolaboradores)
    print("##############--->:: ",colaboradores)
    inventores = crear_mapa_inventores(listainventores)
    print("##############--->:: ",inventores)
    areas = cassandra_get_nombre_areasv2(listaareas)
    print("##############--->:: ",areas)
    myuuid = None
    if idmasivo == None:
        myuuid = uuid_from_time(time.time())
    else:
        myuuid = idmasivo
    #print('')
    print("------->MYUUID:::",myuuid)
    id_invento = str(myuuid)   
    #VOY A INGRESAR POR PAIS...
    #NOMBRE DEL PAIS>>
    nombre_pais = obtener_nombre_pais(id_pais)
    querypais = SimpleStatement(
    
        "INSERT INTO cpm.inventos_por_pais(id_invento,id_pais,nombre_pais,nombre,fec_presentacion,inventores,colaboradores,descripcion,area)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        consistency_level=ConsistencyLevel.QUORUM)
    cluster = Cluster(['master'],protocol_version = 3)
    session = cluster.connect()
    session.execute(querypais, (id_invento,id_pais,nombre_pais,nombre_patente,fec_presentacion,inventores,colaboradores,descripcion,areas))
    

    #VOY A INGRESAR POR inventor
    
    for idinv in listainventores:
        infoinventor = cassandra_get_inventor_por_id(idinv)
        for info in infoinventor:
            querypais = SimpleStatement(
    
            "INSERT INTO cpm.inventos_por_inventor(nombre_inventor,id_invento,id_inventor,nacionalidad,sexo,fec_nac,nombre,fec_presentacion,descripcion,area,colaboradores,pais,id_pais)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            consistency_level=ConsistencyLevel.QUORUM)
            cluster = Cluster(['master'],protocol_version = 3)
            session = cluster.connect()
            session.execute(querypais, (info.nombre,id_invento,idinv,info.pais,"F","1996-01-01",nombre_patente,fec_presentacion,descripcion,areas,colaboradores,nombre_pais,id_pais))
            break
    
    #VOY A INGRESAR POR AREA
    for idarea in listaareas:
        nombre_area = cassandra_get_area_por_id(idarea)
        querypais = SimpleStatement(
    
            "INSERT INTO cpm.inventos_por_area(area,nombre_area,id_invento,inventores,colaboradores,nombre,fec_presentacion,descripcion,pais,id_pais)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            consistency_level=ConsistencyLevel.QUORUM)
        cluster = Cluster(['master'],protocol_version = 3)
        session = cluster.connect()
        session.execute(querypais, (idarea,nombre_area,id_invento,inventores,colaboradores,nombre_patente,fec_presentacion,descripcion,nombre_pais,id_pais))

    
    
    return "Patente ingresada con exito!!!"

def cassandra_get_inventor_por_id(idi):
    cluster = Cluster(['master'],protocol_version = 3)
    session = cluster.connect()
    future = session.execute("select * from cpm.inventores  where id_inventor = %s",[idi])
    return future

def cassandra_get_area_por_id(id):
    cluster = Cluster(['master'],protocol_version = 3)
    session = cluster.connect()
    future = session.execute("select descripcion from cpm.areas_investigacion  where id_area = %s",[id])
    for row in future:
        return row.descripcion.encode('utf-8')


def cassandra_insert_patentes_masivos(path):
    cluster = Cluster(['master'],protocol_version = 3)
    session = cluster.connect()
    
    
    with open(path) as f:
        data = json.load(f)
        data = data['patents']
        
        #obtengo paises..
        paises = cassandra_get_paises()
        
        for patente in data:
            id_patente = patente['patent_number']
            nombre_patente = patente['patent_title']
            descripcion = nombre_patente
            fec_presentacion = patente['patent_date']
            id_pais = patente['assignees'][0]['assignee_lastknown_country']
            areas = patente['IPCs']
            listaareas = []
            for area in areas:
                listaareas.append(area['ipc_section'])
            inventores = patente['inventors']
            listainventores = []
            for invent in inventores:
                listainventores.append(invent['inventor_id'])
            colaboradores = patente['examiners']
            listacolaboradores = []
            for colab in colaboradores:
                listacolaboradores.append(colab['examiner_id'])


            cassandra_insert_patentes(nombre_patente,descripcion,fec_presentacion,id_pais,listaareas,listainventores,listacolaboradores,id_patente)
         
    return "OK"

def obtener_nombre_pais(id):
    cluster = Cluster(['master'],protocol_version = 3)
    session = cluster.connect()
    future = session.execute_async("select nombre from cpm.paises where alpha2=%s",[id])
    rows  = future.result()
    for row in rows:
        return row.nombre
    return "pais no encontrado alv!"

def cassandra_get_nombre_areas(ids):# va a devolver un diccionario.. lo que recive es la lista de areas del archivo..
    resp = {}
    cluster = Cluster(['master'],protocol_version = 3)
    session = cluster.connect()
    for idd in ids:
        valid = idd['ipc_section']
        #print("#######::",valid)
        row = session.execute("select descripcion from cpm.areas_investigacion where id_area= %s",[valid])
        lista = list(row)
        if len(lista)==0 :
            #NO EXISTE ESA CATEGORIA??
            print("Se detecto que no existe la categoria:: ",valid)
        else:
            #SI EXISTE YEIIII
            resp[valid] = lista[0].descripcion
    return resp

def cassandra_get_nombre_areasv2(ids):# va a devolver un diccionario.. lo que recive es la lista de areas del archivo..
    resp = {}
    cluster = Cluster(['master'],protocol_version = 3)
    session = cluster.connect()
    for idd in ids:
        valid = idd
        #print("#######::",valid)
        row = session.execute("select descripcion from cpm.areas_investigacion where id_area= %s",[valid])
        lista = list(row)
        if len(lista)==0 :
            #NO EXISTE ESA CATEGORIA??
            print("Se detecto que no existe la categoria:: ",valid)
        else:
            #SI EXISTE YEIIII
            resp[valid] = lista[0].descripcion
    return resp

def cassandra_get_paises():
    cluster = Cluster(['master'],protocol_version = 3)
    session = cluster.connect()
    future = session.execute("select nombre,alpha2 from cpm.paises")
    return future
def cassandra_get_inventores():
    cluster = Cluster(['master'],protocol_version = 3)
    session = cluster.connect()
    future = session.execute("select id_inventor,nombre from cpm.inventores")
    return future

def cassandra_get_inventor_nombre(id_inventor):
    cluster = Cluster(['master'],protocol_version = 3)
    session = cluster.connect()
    future = session.execute("select nombre from cpm.inventores where id_inventor = %s",[id_inventor])
    for r in future:
        return r.nombre.encode('utf-8')
     

def cassandra_get_areas():
    cluster = Cluster(['master'],protocol_version = 3)
    session = cluster.connect()
    future = session.execute("select id_area,descripcion from cpm.areas_investigacion")
    return future
def cassandra_get_colaboradores_por_area(areas):
    print("$$$$$$$$ AREAS:: ",areas)
    cluster = Cluster(['master'],protocol_version = 3)
    session = cluster.connect()
    future = session.execute("select id_area,descripcion from cpm.areas_investigacion")
    listica = {}
    for now in future:
        listica[now.id_area] = now.descripcion
    print("########:::",listica)
    strquery = 'select id_colaborador, nombre from cpm.colaboradores where'
    parametros = []
    for i in range(len(areas)):
        area = areas[i]
        if i == len(areas) - 1 :
            #es el ultimo
            strquery += " area['"+area+"'] = %s ALLOW FILTERING"
            parametros.append(listica[area])
        else:
            strquery += " area['"+area+"'] = %s AND "
            parametros.append(listica[area])
        #print('')
        print("@@@@@@@@@@@@@@@@@@@@@::",strquery)
        print("########:::",parametros)
    return session.execute(strquery,parametros)

     #from colaboradores where area['A'] = 'Human Necessitites'
       
def cassandra_get_reporte1(id_pais):
    cluster = Cluster(['master'],protocol_version = 3)
    session = cluster.connect()
    future = session.execute("select * from cpm.inventos_por_pais where id_pais = %s ",[id_pais])
    return future
    
def cassandra_get_reporte2(id_inventor,nombre_inventor):
    cluster = Cluster(['master'],protocol_version = 3)
    session = cluster.connect()
    future = session.execute("select * from cpm.inventos_por_inventor where id_inventor =  %s and nombre_inventor = %s",[id_inventor,nombre_inventor])
    return future

def cassandra_get_reporte3(id_area):
    cluster = Cluster(['master'],protocol_version = 3)
    session = cluster.connect()
    future = session.execute("select * from cpm.inventos_por_area where area =  %s",[id_area])
    return future

def cassandra_get_count_colaborador(id):
    cluster = Cluster(['master'],protocol_version = 3)
    session = cluster.connect()
    future = session.execute("select count(*) from cpm.colaboradores where id_colaborador = %s",[id])
    return future


#######################################################
def cassandra_insert_pais(fronteras,nombre,area,alpha2,alpha3,lat,lng,poblacion):
    cluster = Cluster(['master'],protocol_version = 3)
    session = cluster.connect()
    query = SimpleStatement(
    
        "INSERT INTO cpm.paises(nombre,area,alpha2,alpha3,latlng,poblacion,fronteras)values(%s,%s,%s,%s,%s,%s,%s)",
        consistency_level=ConsistencyLevel.QUORUM)
    session.execute(query, (nombre,int(area),alpha2,alpha3,[float(lat),float(lng)],int(poblacion),fronteras))
    return "Pais ingresado correctamente"

#------------------------------------------------------------
####################################################
def cassandra_insert_colaborador(lids,comision,fec_inicio,nombre,salario):
    myuuid = uuid_from_time(time.time())
    print('')
    print("------->MYUUID:::",myuuid)
    id_colaborador = str(myuuid)
    print("------->IDCOLABORADOR:::",id_colaborador)
    print("--->LIDS: ",lids)
    area = get_areas_for_colaborador(lids)
    print("----> AREA::",area)
    cluster = Cluster(['master'],protocol_version = 3)
    session = cluster.connect()
    query = SimpleStatement(
    
        "INSERT INTO cpm.colaboradores(id_colaborador,area,comision,fec_inicio,nombre,salario)values(%s,%s,%s,%s,%s,%s)",
        consistency_level=ConsistencyLevel.QUORUM)
    session.execute(query, (id_colaborador,area,float(comision),fec_inicio,nombre,float(salario)))
    return "Colaborador ingresado correctamente"

def get_areas_for_colaborador(ids):
    resp = {}
    cluster = Cluster(['master'],protocol_version = 3)
    session = cluster.connect()
    for idd in ids:
        valid = idd
        #print("#######::",valid)
        row = session.execute("select descripcion from cpm.areas_investigacion where id_area= %s",[valid])
        lista = list(row)
        resp[valid] = lista[0].descripcion
    return resp

















def insert(fec,correo,titulo,descripcion):
    
    cluster = Cluster(['master'],protocol_version = 3)
    session = cluster.connect()
    myuuid = uuid_from_time(time.time())
    #query = session.prepare("select * from soporte.tickets_por_rango_fechas where fec >= '2014-01-01' and fec <= '2015-12-31' ALLOW FILTERING")
    query = SimpleStatement(
    
        "INSERT INTO soporte.tickets_por_usuario_rango_fechas(fec,correo,idticket,titulo,descripcion)values(%s,%s,%s,%s,%s)",
        consistency_level=ConsistencyLevel.QUORUM)
    session.execute(query, (fec,correo,myuuid,titulo,descripcion))
    query2 = SimpleStatement(
    
        "INSERT INTO soporte.tickets_por_rango_fechas(fec,correo,idticket,titulo,descripcion)values(%s,%s,%s,%s,%s)",
        consistency_level=ConsistencyLevel.QUORUM)
    session.execute(query2, (fec,correo,myuuid,titulo,descripcion))
    return "<p>Ticket creado satisfactoriamente </p>"


def get_tikets_por_fechas(fecha1,fecha2):
    cluster = Cluster(['master'],protocol_version = 3)
    session = cluster.connect()
    #query = session.prepare("select * from soporte.tickets_por_rango_fechas where fec >= '2014-01-01' and fec <= '2015-12-31' ALLOW FILTERING")
    future = session.execute_async("select nombre,alpha2 from cpm.paises")
    try:
        rows = future.result()
        return rows
    except Exception:
        print(Exception)
    return "error al traer paises!!"

def get_tikets_por_usuario_rango_fechas(correo,fecha1,fecha2):
    cluster = Cluster(['master'],protocol_version = 3)
    session = cluster.connect()
    #query = session.prepare("select * from soporte.tickets_por_rango_fechas where fec >= '2014-01-01' and fec <= '2015-12-31' ALLOW FILTERING")
    future = session.execute_async("select * from soporte.tickets_por_usuario_rango_fechas where correo=%s and fec >= %s and fec <= %s",[correo,fecha1,fecha2])
    #log.info("key\tcol1\tcol2")
    #log.info("---\t----\t----")
    resp='posible error'+fecha1+fecha2
    try:
        rows = future.result()
        resp = '''
        <div class="table-wrapper">
        <table class="table table-striped table-sm">
            <thead>
                <tr>
                    <th>Fecha</th>
                    <th>Correo</th>
                    <th>Titulo</th>
                    <th>Descripcion</th>
                </tr>
            </thead>
            <tbody>

            
        '''
        for row in rows:
            resp += '''
        <tr>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
        </tr>
            '''.format(row.fec,row.correo,row.titulo,row.descripcion)
        #print(row.fec)
        #resp.append(str(row.fec))
        resp += '''
            </tbody>
                                    
            </table>
            </div>'''
    except Exception:
        print(Exception)
    
    
    return resp


def main():
    
    
    print("ijoles!")
    cassandra_insert_patentes_masivos('temporales/patents-original.json')
    #cassandra_insert_paises('temporales/countries.json')
    #cluster = Cluster(['master'],protocol_version = 3)
    #session = cluster.connect()

    #rows = session.execute("SELECT keyspace_name FROM system.schema_keyspaces")
    #if KEYSPACE in [row[0] for row in rows]:
    #    log.info("dropping existing keyspace...")
    #    session.execute("DROP KEYSPACE " + KEYSPACE)

    #log.info("creating keyspace...")
    #session.execute("""
    #    CREATE KEYSPACE %s
    #    WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
    #    """ % KEYSPACE)

    #log.info("setting keyspace...")
    #session.set_keyspace(KEYSPACE)

    #log.info("creating table...")
    #session.execute("""
    #    CREATE TABLE mytable (
    #        thekey text,
    #        col1 text,
    #        col2 text,
    #        PRIMARY KEY (thekey, col1)
    #    )
    #    """)

    #query = SimpleStatement("""
    #    INSERT INTO mytable (thekey, col1, col2)
    #    VALUES (%(key)s, %(a)s, %(b)s)
    #    """, consistency_level=ConsistencyLevel.ONE)

    #prepared = session.prepare("""
    #    INSERT INTO mytable (thekey, col1, col2)
    #    VALUES (?, ?, ?)
    #    """)

    #for i in range(10):
    #    log.info("inserting row %d" % i)
    #    session.execute(query, dict(key="key%d" % i, a='a', b='b'))
    #    session.execute(prepared.bind(("key%d" % i, 'b', 'b')))

    #future = session.execute_async("select * from soporte.tickets_por_rango_fechas")
    #log.info("key\tcol1\tcol2")
    #log.info("---\t----\t----")

    #try:
    #    rows = future.result()
    #except Exception:
    #    log.exeception()

    #for row in rows:
    #    print(row.fec)

    #session.execute("DROP KEYSPACE " + KEYSPACE)

if __name__ == "__main__":
    main()