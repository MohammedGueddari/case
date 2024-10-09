import sys
import boto3
import json
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrameCollection
from awsglue.dynamicframe import Dynamicframe


sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

glue_client = boto3.client("glue")

def captura_api():
    print()

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
        def
    except:
        invok lambda error 

if __name__ == "__main__":
    main()