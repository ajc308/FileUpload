import config
import pymssql

server = config.DB_SERVER
user = config.DB_USER
password = config.DB_PASSWORD


def get_connection(database):
    return pymssql.connect(server, user, password, database)


def get_table_columns(database, table):
    query = "SELECT c.name FROM sys.objects o INNER JOIN sys.columns c ON o.object_id = c.object_id WHERE o.name='{table}'".format(
        table=table
    )
    conn = get_connection(database)
    cursor = conn.cursor()

    cursor.execute(query)
    table_columns = [row[0] for row in cursor]

    cursor.close()
    conn.close()

    return table_columns


def truncate_table(database, table):
    conn = get_connection(database)
    cursor = conn.cursor()

    cursor.execute("TRUNCATE TABLE {table}".format(table=table))
    conn.commit()

    cursor.close()
    conn.close()
