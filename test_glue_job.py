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


@mock('glue_job.DynamicFrame')
@mock('glue_job.createDataFrame')
@mock('glue_job.requests')
def test_captura_api(
        mock_requests,
        mock_createDataFrame,
        mock_DynamicFrame
):
    mock_response_api = MagicMock()
    atributos = {
        "get.return_value" : mock_response_api
    }
    mock_requests.configure_mock(**atributos)

    mock_df = MagicMock()
    atributos = {
        "createDataFrame.return_value" : mock_df
    }
    mock_createDataFrame.configure_mock(**atributos)

    mock_DynamicFrame = MagicMock()
    atributos = {
        "fromDF.return_value" : mock_DynamicFrame
    }
    mock_DynamicFrame.configure_mock(**atributos)

    glue_job.captura_api()

    call_mock_requests = mock_requests.mock_calls

    assert call_mock_requests == mock_response_api

    call_createDataFrame = mock_createDataFrame.mock_calls
    assert call_createDataFrame == mock_df

    call_DynamicFrame = mock_DynamicFrame.mock_calls
    assert call_DynamicFrame == mock_DynamicFrame
