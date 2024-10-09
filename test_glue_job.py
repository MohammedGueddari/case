import sys
import boto3
import json
import requests
from awsglue.transforms import *
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.dynamicframe import Dynamicframe
from datetime import datetime


sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

glue_client = boto3.client("glue")
lambda_client = boto3.client("lambda") 

def captura_api():
    url = 'https://api.openbrewerydb.org/breweries'
    response = requests.get(url)

    df = spark.createDataFrame(response)
    dynamic_frame = DynamicFrame.fromDF(df, glueContext, "dynamic_frame")
    return dynamic_frame
    

def grava_resultado(glueContext, dynamicframe):
    sink = glueContext.getSink(
        path="s3://bucket/tabelaXX",
        connection_type="s3",
        updateBehavior="UPDATE_IN_DATABASE",
        partitionKeys=[],
        enableUpdateCatalog=True,
        transformation_ctx="sink"
    )
    sink.setFormat("json")
    sink.setCatalogInfo(catalogDatabase="target_db_name", catalogTableName="target_table_name")
    sink.writeFrame(dynamicframe)

def main():
    try:
        grava_resultado(captura_api())
        glueContext.commit()
    except:
        payload = {
            "job_name": "glue_job)",
            "key2": datetime.now()
        }
        json_payload = json.dumps(payload)
        response = lambda_client.invoke(
        FunctionName="function_error",
        InvocationType='RequestResponse',  # Use 'Event' for async invocation
        Payload=json_payload
)

if __name__ == "__main__":
    main()