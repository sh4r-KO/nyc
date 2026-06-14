DROP MATERIALIZED VIEW IF EXISTS agg_view;
CREATE MATERIALIZED VIEW agg_view AS
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
