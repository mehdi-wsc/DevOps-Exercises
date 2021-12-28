import sqlite3
import psycopg2
import psycopg2.extras
import os
from flask import g, current_app


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db()
    return db


def connect_db():
    db_type = os.environ.get("DB_TYPE", "sqlite")

    if db_type == "sqlite":
        return connect_sqlite()
    elif db_type == "postgres":
        return connect_postgres()
    return None


def connect_sqlite():
    database = os.environ.get("DB_NAME")

    db = sqlite3.connect(database)
    db.row_factory = dict_factory
    db.execute("PRAGMA foreign_keys = ON;")
    db.commit()

    return {
        "db": db,
        "query": query_sqlite
    }


def connect_postgres():
    user = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASSWORD")
    host = os.environ.get("DB_HOST")
    port = os.environ.get("DB_PORT")
    database = os.environ.get("DB_NAME")

    if not (user and password and host and port and database):
        raise Exception("DB Configuration")

    return {
        "db": psycopg2.connect(
            user = user,
            password = password,
            host = host,
            port = port,
            database = database
        ),
        "query": query_postgres
    }


def query_sqlite(query, args=(), one=False):
    parts = query.split(" ")
    insert = True if parts[0].upper() == "INSERT" else False
    try:
        cur = get_db()["db"].execute(query, args)
        if not insert:
            rv = cur.fetchall()
            cur.close()
            return (rv[0] if rv else None) if one else rv
        else:
            get_db().commit()
            return cur.lastrowid
    except Exception as e:
        print(str(e))
        get_db()["db"].rollback()
        return False


def query_postgres(query, args=(), one=False):
    parts = query.split(" ")
    insert = True if parts[0].upper() == "INSERT" else False
    if insert:
        query += " RETURNING id"
    try:
        cur = get_db()["db"].cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(query, args)
        if not insert:
            rv = [dict(record) for record in cur.fetchall()]
            return (rv[0] if rv else None) if one else rv
        else:
            # get_db()["db"].commit()
            return cur.fetchone()['id']
    except Exception as e:
        print(str(e))
        # get_db()["db"].rollback()
        return False


def query_db(query, args=(), one=False):
    db = get_db()
    if db is not None:
        return db["query"](query, args, one)
    return None