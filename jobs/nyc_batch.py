import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, hour, avg, count

# args: input_csv  output_dir
input_csv, output_dir = sys.argv[1], sys.argv[2]

spark = (
    SparkSession.builder
    .appName("nyc-batch")
    .config("spark.hadoop.fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
    .config("spark.hadoop.google.cloud.auth.service.account.enable", "true")
    #below would be set in airflow env
    .config("spark.hadoop.google.cloud.auth.service.account.json.keyfile", "/Users/koundesn/Projects/code/nyc_batch_pipeline/airflow_home/secret/gcp-big-self-009-8a0269bcd9a5.json")
    #.config("spark.bigquery.project", "gcp-big-self-009")  # Set your project ID here
    .getOrCreate()
)

# adjust the column names to your CSV if needed
df = (
    spark.read.option("header", "true")
    .option("inferSchema", "true")
    .csv(input_csv)
)

# example for NYC yellow taxi data style columns
# tpep_pickup_datetime, fare_amount
df = df.withColumn("pickup_ts", to_timestamp(col("tpep_pickup_datetime")))
agg = (
    df.filter(col("fare_amount") > 0)
      .withColumn("pickup_hour", hour("pickup_ts"))
      .groupBy("pickup_hour")
      .agg(
          count("*").alias("trips"),
          avg("fare_amount").alias("avg_fare")
      )
      .orderBy("pickup_hour")
)
agg.show()
# Write directly to BigQuery
agg.write \
    .format("bigquery") \
    .option("table", "gcp-big-self-009.nyc_cab.fare_aggregate") \
    .option("temporaryGcsBucket", "spark-bq-staging-1234") \
    .mode("append") \
    .save()

#agg.write.mode("overwrite").parquet(output_dir)
spark.stop()