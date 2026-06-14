import pandas as pd
import pyarrow.parquet as pq
import psycopg2
from dotenv import load_dotenv
from io import StringIO
import os, time

import json

if __name__ == "__main__":
    load_dotenv()

    CHUNK_SIZE = 100_000  # lower = less RAM, more commits

    def connect_with_retry(retries=10, delay=3):
        for i in range(retries):
            try:
                conn = psycopg2.connect(
                    host=os.getenv("DB_HOST"),
                    port=os.getenv("DB_PORT"),
                    dbname=os.getenv("DB_NAME"),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASSWORD")
                )
                print("Connected to DB!")
                return conn
            except psycopg2.OperationalError as e:
                print(f"Attempt {i+1}/{retries} failed: {e}")
                time.sleep(delay)
        raise Exception("Could not connect to DB after retries")

    #todo use file not this : https://stackoverflow.com/questions/19472922/reading-external-sql-script-in-python
    def create_table(conn):
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS fhvhv_tripdata (
                    hvfhs_license_num TEXT,
                    dispatching_base_num TEXT,
                    originating_base_num TEXT,
                    request_datetime TIMESTAMP,
                    on_scene_datetime TIMESTAMP,
                    pickup_datetime TIMESTAMP,
                    dropoff_datetime TIMESTAMP,
                    pulocationid INTEGER,
                    dolocationid INTEGER,
                    trip_miles FLOAT,
                    trip_time BIGINT,
                    base_passenger_fare FLOAT,
                    tolls FLOAT,
                    bcf FLOAT,
                    sales_tax FLOAT,
                    congestion_surcharge FLOAT,
                    airport_fee FLOAT,
                    tips FLOAT,
                    driver_pay FLOAT,
                    shared_request_flag TEXT,
                    shared_match_flag TEXT,
                    access_a_ride_flag TEXT,
                    wav_request_flag TEXT,
                    wav_match_flag TEXT,
                    cbd_congestion_fee FLOAT
                )
            ''')
            conn.commit()
        print("Table ready.")

    def copy_chunk(df, conn):
        buffer = StringIO()
        df.to_csv(buffer, index=False, header=False, sep='\t', na_rep='\\N')
        buffer.seek(0)
        with conn.cursor() as cur:
            try:
                cur.copy_from(buffer, 'fhvhv_tripdata', sep='\t', null='\\N',
                              columns=df.columns.tolist())  # back to normal
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e


    def stream_parquet_to_db(filepath, conn):
        pf = pq.ParquetFile(filepath)
        total_rows = pf.metadata.num_rows
        inserted = 0

        print(f"File has {total_rows:,} rows — streaming in chunks of {CHUNK_SIZE:,}")

        for batch in pf.iter_batches(batch_size=CHUNK_SIZE):
            df = batch.to_pandas()
            df = df.rename(columns={'PULocationID': 'pulocationid', 'DOLocationID': 'dolocationid'})
            df = df.where(pd.notnull(df), None)
            copy_chunk(df, conn)
            inserted += len(df)
            pct = 100 * inserted // total_rows
            print(f"  {inserted:,}/{total_rows:,} rows ({pct}%)", flush=True)

        print(f"Done! Inserted {inserted:,} rows.")


    MONTH_PRIOR = int(os.environ['MONTH_PRIOR'])

    print("MONTH_PRIOR value : ",MONTH_PRIOR)
    if MONTH_PRIOR == 0:

        print("this is an update !launch the initialisation process! not coded yet though :(")

        fd = open('Data_aggregations.sql', 'r')
        sqlFile = fd.read()
        fd.close()
        conn = connect_with_retry()

        sqlCommands = sqlFile.split(';')

        conn.autocommit = True  # or commit explicitly after the loop
        with conn.cursor() as cur:
            for command in sqlCommands:
                if not command.strip():
                    continue
                cur.execute(command)


        with conn.cursor() as cur:
            cur.execute("SELECT json_agg(agg_view) FROM agg_view")#eecuted here to preventcross-container permission
            result = cur.fetchone()[0]
        with open('/tmp/export.json', 'w') as f:
            json.dump(result, f)
    elif MONTH_PRIOR > 0:

        print("Starting...")
        conn = connect_with_retry()
        create_table(conn)
        stream_parquet_to_db('/app/fhvhv_tripdata_2026-01.parquet', conn)
        conn.close()
        print("JOB DONE #################################")
