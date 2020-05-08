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
    query = SimpleStatement(
    
        "INSERT INTO cpm.inventores(id_inventor,nombre,alpha2,pais)values(%s,%s,%s,%s)",
        consistency_level=ConsistencyLevel.QUORUM)
    
    with open(path) as f:
        data = json.load(f)
        data = data['patents']
        for patente in data:
            print("##########")
            #return patente
            inventores = patente['inventors']
            for inventor in inventores:
                nombre = inventor['inventor_first_name']+ "" + inventor['inventor_last_name']
                pais = obtener_nombre_pais(inventor['inventor_country'])
                session.execute(query, (inventor['inventor_id'],nombre,inventor['inventor_country'],pais))
    return "OK"

def obtener_nombre_pais(id):
    cluster = Cluster(['master'],protocol_version = 3)
    session = cluster.connect()
    future = session.execute_async("select nombre from cpm.paises where alpha2=%s",[id])
    rows  = future.result()
    for row in rows:
        return row.nombre
    return "pais no encontrado alv!"


def cassandra_get_paises():
    cluster = Cluster(['master'],protocol_version = 3)
    session = cluster.connect()
    future = session.execute_async("select nombre,alpha2 from cpm.paises")
    return future.result()

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
    cluster = Cluster(['master'],protocol_version = 3)
    session = cluster.connect()

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

    future = session.execute_async("select * from soporte.tickets_por_rango_fechas")
    log.info("key\tcol1\tcol2")
    log.info("---\t----\t----")

    try:
        rows = future.result()
    except Exception:
        log.exeception()

    for row in rows:
        print(row.fec)

    #session.execute("DROP KEYSPACE " + KEYSPACE)

#if __name__ == "__main__":
#    main()