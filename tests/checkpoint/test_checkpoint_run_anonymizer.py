import pandas as pd
import pytest

from great_expectations import DataContext
from great_expectations.checkpoint import Checkpoint
from great_expectations.core.batch import RuntimeBatchRequest
from great_expectations.core.usage_statistics.anonymizers.checkpoint_anonymizer import (
    CheckpointAnonymizer,
)
from great_expectations.core.util import convert_to_json_serializable
from great_expectations.data_context.types.base import CheckpointConfig

DATA_CONTEXT_ID = "00000000-0000-0000-0000-000000000001"


@pytest.fixture
def checkpoint(
    titanic_pandas_data_context_with_v013_datasource_with_checkpoints_v1_with_empty_store_stats_enabled,
):
    context: DataContext = titanic_pandas_data_context_with_v013_datasource_with_checkpoints_v1_with_empty_store_stats_enabled
    return Checkpoint(
        data_context=context,
        **{
            "name": "my_checkpoint",
            "config_version": 1.0,
            "template_name": None,
            "run_name_template": None,
            "expectation_suite_name": None,
            "batch_request": None,
            "action_list": [
                {
                    "name": "store_validation_result",
                    "action": {"class_name": "StoreValidationResultAction"},
                },
                {
                    "name": "store_evaluation_params",
                    "action": {"class_name": "StoreEvaluationParametersAction"},
                },
                {
                    "name": "update_data_docs",
                    "action": {"class_name": "UpdateDataDocsAction", "site_names": []},
                },
            ],
            "evaluation_parameters": {},
            "runtime_configuration": {},
            "validations": [
                {
                    "batch_request": {
                        "datasource_name": "example_datasource",
                        "data_connector_name": "default_runtime_data_connector_name",
                        "data_asset_name": "my_data_asset",
                    },
                    "expectation_suite_name": "test_suite",
                }
            ],
            "profilers": [],
            "ge_cloud_id": None,
            "expectation_suite_ge_cloud_id": None,
        }
    )


def test_resolve_config_using_acceptable_arguments(checkpoint):
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})

    batch_request_param = {
        "runtime_parameters": {"batch_data": df},
        "batch_identifiers": {"default_identifier_name": "my_simple_df"},
    }

    result_format_param = {"result_format": "SUMMARY"}

    kwargs = {
        "batch_request": batch_request_param,
        "result_format": result_format_param,
    }

    # Matching how this is called in usage_statistics.py (parameter style)
    resolved_runtime_kwargs: dict = (
        CheckpointConfig.resolve_config_using_acceptable_arguments(
            *(checkpoint,), **kwargs
        )
    )

    # Assertions about important bits of the substituted_runtime_config

    expected_top_level_batch_request = {
        "runtime_parameters": {"batch_data": df},
        "batch_identifiers": {"default_identifier_name": "my_simple_df"},
    }
    expected_top_level_batch_request = convert_to_json_serializable(
        data=expected_top_level_batch_request
    )
    actual_top_level_batch_request = convert_to_json_serializable(
        data=resolved_runtime_kwargs["batch_request"]
    )
    assert actual_top_level_batch_request == expected_top_level_batch_request

    validation_level_batch_request = resolved_runtime_kwargs["validations"][0][
        "batch_request"
    ]

    assert validation_level_batch_request == RuntimeBatchRequest(
        **{
            "datasource_name": "example_datasource",
            "data_connector_name": "default_runtime_data_connector_name",
            "data_asset_name": "my_data_asset",
            "batch_identifiers": {"default_identifier_name": "my_simple_df"},
            "runtime_parameters": {"batch_data": df},
        }
    )
    assert (
        resolved_runtime_kwargs["validations"][0]["expectation_suite_name"]
        == "test_suite"
    )
