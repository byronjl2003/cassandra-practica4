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
def cassandra_insert_patentes_masivos(path):
    cluster = Cluster(['master'],protocol_version = 3)
    session = cluster.connect()
    
    
    with open(path) as f:
        data = json.load(f)
        data = data['patents']
        
        #obtengo paises..
        paises = cassandra_get_paises()
        
        for patente in data:
                 
            #SE AGREGAN LOS Colaboradores... 
            colaboradores = patente['examiners']
            for colaborador in colaboradores:
                nombre_colaborador = colaborador['examiner_first_name'] + colaborador['examiner_last_name']
                id_colaborador = colaborador['examiner_id']
                ids_areas = patente['IPCs']
                nombres_area = cassandra_get_nombre_areas(ids_areas)
                #print("Conversion de areas..jiji::: ",nombres_area)
                #Sera que ya existe ese colaborador
                row_count_colaborador = cassandra_get_count_colaborador(id_colaborador)
                #print("@@@@@:: ",row_count_colaborador)
                for r in row_count_colaborador:
                    #print("------->::: ",r)
                    #print("------->::: ",r.count)
                    count = r.count
                if count == 0:
                    pass
                    ##SE CREA EL NUEVO REGISTRO
                    query_colaborador = SimpleStatement(
                        "INSERT INTO cpm.colaboradores(id_colaborador,area,comision,fec_inicio,nombre,salario)values(%s,%s,%s,%s,%s,%s)",consistency_level=ConsistencyLevel.QUORUM)
                    session.execute(query_colaborador, (id_colaborador,nombres_area,random.uniform(350, 1000),'2020-05-10',nombre_colaborador,random.uniform(3500, 25000.5)))
 
                else:
                    pass
                    ## SE AGREGA A LA LISTA
                    query_colaborador = SimpleStatement(
                        "UPDATE cpm.colaboradores SET area = area + %s where id_colaborador = %s",consistency_level=ConsistencyLevel.QUORUM)
                    session.execute(query_colaborador, (nombres_area,id_colaborador))
 


                



    return "OK"

def obtener_nombre_pais(id):
    cluster = Cluster(['master'],protocol_version = 3)
    session = cluster.connect()
    future = session.execute_async("select nombre from cpm.paises where alpha2=%s",[id])
    rows  = future.result()
    for row in rows:
        return row.nombre
    return "pais no encontrado alv!"

def cassandra_get_nombre_areas(ids):# va a devolver un diccionario..
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
def cassandra_get_areas():
    cluster = Cluster(['master'],protocol_version = 3)
    session = cluster.connect()
    future = session.execute("select id_area,descripcion from cpm.areas_investigacion")
    return future
def cassandra_get_colaboradores_por_area(areas):
    for area in areas:
        strquery = 'select id_colaborador, nombre'
        #from colaboradores where area['A'] = 'Human Necessitites'


def cassandra_get_count_colaborador(id):
    cluster = Cluster(['master'],protocol_version = 3)
    session = cluster.connect()
    future = session.execute("select count(*) from cpm.colaboradores where id_colaborador = %s",[id])
    return future

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