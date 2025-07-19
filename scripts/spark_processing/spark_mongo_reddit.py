from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import col, from_unixtime, to_timestamp
import os
from dotenv import load_dotenv

load_dotenv()

def process_reddit_data():
    spark = SparkSession.builder \
        .appName("ProcessRedditData") \
        .config("spark.mongodb.input.uri", os.getenv('MONGO_URI') + "/bigdata_db.reddit") \
        .config("spark.mongodb.output.uri", os.getenv('MONGO_URI') + "/bigdata_db.reddit_processed") \
        .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.0.5") \
        .getOrCreate()

    try:
        # Definir esquema para los datos de Reddit
        schema = StructType([
            StructField("id", StringType(), True),
            StructField("title", StringType(), True),
            StructField("author", StringType(), True),
            StructField("score", IntegerType(), True),
            StructField("comments", IntegerType(), True),
            StructField("created_utc", TimestampType(), True),
            StructField("url", StringType(), True),
            StructField("selftext", StringType(), True),
            StructField("subreddit", StringType(), True),
            StructField("processed_at", TimestampType(), True)
        ])
        
        # Leer datos de MongoDB
        df = spark.read.format("mongo").load()
        
        # Procesar los datos
        processed_df = df.withColumn("created_ts", 
                              to_timestamp(from_unixtime(col("created_utc")))) \
                     .withColumn("processed_at", 
                              to_timestamp(from_unixtime(col("created_utc")))) \
                     .drop("created_utc")
        
        # Filtrar posts relevantes (score > 1000 o comments > 100)
        filtered_df = processed_df.filter((col("score") > 1000) | (col("comments") > 100))
        
        # Mostrar muestra de datos
        print("=== Muestra de datos procesados de Reddit ===")
        filtered_df.orderBy(col("created_ts").desc()).show(10, truncate=False)
        
        # Guardar en MongoDB
        filtered_df.write.format("mongo") \
            .mode("overwrite") \
            .save()
            
        print("Datos de Reddit procesados y guardados exitosamente")
        
    except Exception as e:
        print(f"Error al procesar datos de Reddit: {str(e)}")
    finally:
        spark.stop()

if __name__ == "__main__":
    process_reddit_data()