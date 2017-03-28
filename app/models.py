import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError

def dbSetUp():
    connection=r.connect(host='localhost',port=28015)
    try:
        r.db_create('hackjobs').run(connection)
        r.db('hackjobs').table_create('user').run(connection)
        r.db('hackjobs').table_create('post').run(connection)
        print("Database setup completed")
    except RqlRuntimeError:
        print("Database running Okay")
    finally:
        connection.close()
