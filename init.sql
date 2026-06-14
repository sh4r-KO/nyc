

GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;

CREATE TABLE IF NOT EXISTS fhvhv_tripdata (
            hvfhs_license_num TEXT,
            dispatching_base_num TEXT,
            originating_base_num TEXT,
            request_datetime TIMESTAMP,
            on_scene_datetime TIMESTAMP,
            pickup_datetime TIMESTAMP,
            dropoff_datetime TIMESTAMP,
            PULocationID INTEGER,
            DOLocationID INTEGER,
            trip_miles FLOAT,
            trip_time INTEGER,
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
        );