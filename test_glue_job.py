import sys
import os
import mock
import pytest
import json
from unittest.mock import MagicMock
from pyspark.sql import SparkSession
from pyspark.context import SparkContext
from unittest.mock import call
from datetime import datetime
import calendar

sys.path.append(os.path.abspath('./'))
import glue_job

spark = SparkSession.builder.getOrCreate()

sc = SparkContext.getOrCreate()
sc.addPyFile('./glue_job')

@pytest.fixture(autouse=True)
def append_sys_args():
    sys.argv.append('--JOB_NAME')
    yield
    sys.argv.remove('--JOB_NAME')