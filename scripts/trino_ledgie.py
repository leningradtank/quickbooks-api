import trino
import pandas as pd

def read_ledgie_data():
    conn = trino.dbapi.connect(
        host='your_trino_host',
        port=8080,
        user='your_trino_user',
        catalog='your_catalog',
        schema='your_schema',
        http_scheme='https'
    )
    
    query = """
    SELECT *
    FROM my_table
    WHERE column_a = 'value_a'
    AND column_b = 'value_b'
    """

    df_ledgie = pd.read_sql_query(query, conn)

    return df_ledgie