from airflow.providers.postgres.hooks.postgres import PostgresHook
from psycopg2.extras import RealDictCursor

table = "yt_api"

def get_conn_cursor():
    """
    Establishes a connection to the PostgreSQL database.
    
    Uses Airflow's PostgresHook to connect to the 'postgres_db_yt_elt' database.
    Creates a cursor that returns rows as dictionaries using RealDictCursor.
    
    Returns:
        tuple: A tuple containing:
            - conn (psycopg2.extensions.connection): Database connection object.
            - cur (psycopg2.extras.RealDictCursor): Dictionary-like cursor object.
    """
    hook = PostgresHook(postgres_conn_id="postgres_db_yt_elt")
    conn = hook.get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    return conn, cur

def close_conn_cursor(conn, cur):
    """
    Closes the given cursor and database connection.
    
    Args:
        conn (psycopg2.extensions.connection): Database connection object to be closed.
        cur (psycopg2.extensions.cursor): Database cursor object to be closed.
    """
    cur.close()
    conn.close()
    
def create_schema(schema):
    """
    Creates a database schema if it doesn't already exist.
    
    Args:
        schema (str): The name of the schema to create.
    """
    conn, cur = get_conn_cursor()
    schema_sql = f"CREATE SCHEMA IF NOT EXISTS {schema};"
    cur.execute(schema_sql)
    conn.commit()
    close_conn_cursor(conn, cur)


def create_table(schema):
    """
    Creates a table within the specified schema with a predefined structure.
    
    The table structure differs based on the schema. If the schema is 'staging', 
    the 'Duration' is stored as a VARCHAR and no 'Video_Type' is included. 
    For other schemas (like 'core'), 'Duration' is stored as a TIME type, 
    and a 'Video_Type' column is added.
    
    Args:
        schema (str): The name of the schema where the table will be created.
    """
    conn, cur = get_conn_cursor()
    if schema == "staging":
        table_sql = f"""
                CREATE TABLE IF NOT EXISTS {schema}.{table} (
                    "Video_ID" VARCHAR(11) PRIMARY KEY NOT NULL,
                    "Video_Title" TEXT NOT NULL,
                    "Upload_Date" TIMESTAMP NOT NULL,
                    "Duration" VARCHAR(20) NOT NULL,
                    "Video_Views" INT,
                    "Likes_Count" INT,
                    "Comments_Count" INT   
                );
            """
    else:
        table_sql = f"""
                  CREATE TABLE IF NOT EXISTS {schema}.{table} (
                      "Video_ID" VARCHAR(11) PRIMARY KEY NOT NULL,
                      "Video_Title" TEXT NOT NULL,
                      "Upload_Date" TIMESTAMP NOT NULL,
                      "Duration" TIME NOT NULL,
                      "Video_Type" VARCHAR(10) NOT NULL,
                      "Video_Views" INT,
                      "Likes_Count" INT,
                      "Comments_Count" INT    
                  ); 
              """
    cur.execute(table_sql)
    conn.commit()
    close_conn_cursor(conn, cur)


def get_video_ids(cur, schema):
    """
    Retrieves all Video IDs from the table in the given schema.
    
    Args:
        cur (psycopg2.extras.RealDictCursor): The dictionary-like database cursor.
        schema (str): The name of the schema to query.
        
    Returns:
        list: A list containing all 'Video_ID' strings found in the specified table.
    """
    cur.execute(f"""SELECT "Video_ID" FROM {schema}.{table};""")
    ids = cur.fetchall()
    video_ids = [row["Video_ID"] for row in ids]
    return video_ids