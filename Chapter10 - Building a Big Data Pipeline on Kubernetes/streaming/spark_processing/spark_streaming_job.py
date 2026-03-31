from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.sql.types import *

if __name__ == "__main__":

    spark = (
        SparkSession.builder
        .appName("ConsumeFromKafka")
        .getOrCreate()
    ) 

    spark.sparkContext.setLogLevel('ERROR') 

    df = ( 
        spark.readStream 
        .format('kafka') 
        .option("kafka.bootstrap.servers", "kafka-cluster-kafka-bootstrap:9092") 
        .option("subscribe", "src-customers")
        .option("startingOffsets", "earliest") 
        .load() 
    )

    schema1 = StructType([
        StructField("schema", StringType(), False),
        StructField("payload", StringType(), False)
    ])

    schema2 = StructType([
        StructField("name", StringType(), False),
        StructField("gender", StringType(), False),
        StructField("phone", StringType(), False),
        StructField("email", StringType(), False),
        StructField("photo", StringType(), False),
        StructField("birthdate", StringType(), False),
        StructField("profession", StringType(), False),
        StructField("dt_update", LongType(), False)
    ])

    o = df.selectExpr("CAST(value AS STRING)")

    o2 = o.select(f.from_json(f.col("value"), schema1).alias("data")).selectExpr("data.payload")
    o2 = o2.selectExpr("CAST(payload AS STRING)")
    newdf = o2.select(f.from_json(f.col("payload"), schema2).alias("data")).selectExpr("data.*")

    query = (
        newdf
        .withColumn("dt_birthdate", f.col("birthdate"))
        .withColumn("today", f.to_date(f.current_timestamp() ) )
        .withColumn("age", f.round(
            f.datediff(f.col("today"), f.col("dt_birthdate"))/365.25, 0)
        )
        .select("name", "gender", "birthdate", "profession", "age", "dt_update")
    )
    write_schema = '{"schema":{"type":"struct","fields":[{"type":"string","optional":true,"field":"name"},{"type":"string","optional":true,"field":"gender"},{"type":"string","optional":true,"field":"birthdate"},{"type":"string","optional":true,"field":"profession"},{"type":"int64","optional":true,"field":"age"},{"type":"int64","optional":true,"name":"org.apache.kafka.connect.data.Timestamp","version":1,"field":"dt_update"}],"optional":false},"payload":'

    json_query = (
        query
        .select(
            f.to_json(f.struct(f.col("*")))
        )
        .toDF("value")
    )

    (
        json_query
        .withColumn("value", f.concat(f.lit(write_schema), f.col("value"), f.lit('}')))
        .selectExpr("CAST(value AS STRING)")
        .writeStream
        .format("kafka")
        .option("kafka.bootstrap.servers", "kafka-cluster-kafka-bootstrap:9092")
        .option("topic", "customers-transformed")
        .option("checkpointLocation", "s3a://bdok-<ACCOUNT-NUMBER>/spark-checkpoint/customers-processing/")
        .start()
        .awaitTermination()
    )
