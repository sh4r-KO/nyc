structure of wht you will find here

      ┌───────────┐
      │           │           ┌─────────────┐
      │    API    │           │ cached file │
      │           │           │  20M rows   │
      └─────┬─────┘           └──────┬──────┘
            │                        │
   ┌────────┼────────────────────────┼──────────┐
   │        │                        │          │
   │        │                        │          │
   │        ▼                        │          │
   │   ┌──────────┐                  ▼          │
   │   │          │          ┌──────────────┐   │
   │   │  Python  ├────────► │  PostgresSQL │   │
   │   │  script  │          │   instance   │   │
   │   │          │          └──────────────┘   │
   │   └──────────┘                             │
   │             Docker-compose                 │
   │                                            │
   └────────────────────────────────────────────┘
#done at : https://asciiflow.com/#/

u need docker, docker compose, you can replace every podman by docker, its a wrapper for my current OS

this runs the docker compose file, contains 1 python app script and 1 pgsql instance.

how this should run :

    MONTH_PRIOR=0 podman compose -f docker-compose.yml up
    podman compose -f docker-compose.yml up

podman compose down && podman compose build --no-cache && MONTH_PRIOR=0 podman compose up -d


to check the python/db logs:
    podman logs python_app/postgres_db
to connect to the pgsql instance:
    psql -h localhost -U myuser -p 5432 -d mydb
    password : mypassword

to execute .sql script :
psql -h localhost -U myuser -p 5432 -d mydb -a -f Data_aggregations.sql

to run inside a container :
podman exec -it <CONTAINER_ID> sh
idk
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────





TODO LIST :
1. separate update and initialisation
    -initialisation :
        the pgsql instance should be created using the cached file (fhvhv_tripdata_2026-01.parquet)
        with a dedicated python script
    -update :
        when needed an optional argument passed, should download related file. Such as months from 01/2026
        so running this arg preceding_month would download the numbers (indicated) of month prior to the 01/2026 date
2. analytics
    when previous steps are achieved, something must be done to showcase this data properly, just doing some analytic work defining kpi and doing some nice graph
3. showcase:
    when the steps above are done, there should be a way to show this to the world.




────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────




analytics idea for later :

avg ride price / month

CREATE MATERIALIZED VIEW avg_price_daily AS

SELECT
  AVG(
      COALESCE(base_passenger_fare, 0)
    + COALESCE(tolls, 0)
    + COALESCE(bcf, 0)
    + COALESCE(sales_tax, 0)
    + COALESCE(congestion_surcharge, 0)
    + COALESCE(airport_fee, 0)
    + COALESCE(cbd_congestion_fee, 0)
    + COALESCE(tips, 0)
  ) AS avg_total_price, DATE_TRUNC('DAY', dropoff_datetime)
FROM fhvhv_tripdata
GROUP BY DATE_TRUNC('DAY', dropoff_datetime);
;



