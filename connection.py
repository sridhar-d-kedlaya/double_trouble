import psycopg

def connect():
    global conn
    conn = psycopg.connect("dbname=iitb_ctf user=parzival")
    return conn

def transt():
    conn = connect()
