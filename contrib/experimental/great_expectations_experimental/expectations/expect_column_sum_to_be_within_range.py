"""
This is a template for creating custom ColumnExpectations.
For detailed instructions on how to use it, please see:
    https://docs.greatexpectations.io/docs/guides/expectations/creating_custom_expectations/how_to_create_custom_column_aggregate_expectations
"""

from typing import Dict, Optional

from great_expectations.core.expectation_configuration import ExpectationConfiguration
from great_expectations.execution_engine import ExecutionEngine
from great_expectations.expectations.expectation import ColumnExpectation


# This class defines the Expectation itself
class ExpectColumnSumToBeWithinRange(ColumnExpectation):
    """Expect the sum of a column to be within given range."""

    # These examples will be shown in the public gallery.
    # They will also be executed as unit tests for your Expectation.
    examples = [
        {
            "data": {"test": [1, 2, 3, 4, 5]},
            "tests": [
                {
                    "title": "basic_positive_test",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "test", "sum_total_range": (14,16)},
                    "out": {"success": True},
                },
                {
                    "title": "basic_negative_test",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "test", "sum_total_range": (10,14)},
                    "out": {"success": False},
                },
            ],
            "test_backends": [
                {
                    "backend": "pandas",
                    "dialects": None,
                },
                {
                    "backend": "sqlalchemy",
                    "dialects": ["sqlite", "postgresql"],
                },
                {
                    "backend": "spark",
                    "dialects": None,
                },
            ],
        }
    ]

    # This is a tuple consisting of all Metrics necessary to evaluate the Expectation.
    metric_dependencies = ("column.sum",)

    # This a tuple of parameter names that can affect whether the Expectation evaluates to True or False.
    success_keys = ("sum_total_range",)

    # This dictionary contains default values for any parameters that should have default values.
    default_kwarg_values = {}

    def validate_configuration(
        self, configuration: Optional[ExpectationConfiguration]
    ) -> None:
        """
        Validates that a configuration has been set, and sets a configuration if it has yet to be set. Ensures that
        necessary configuration arguments have been provided for the validation of the expectation.

        Args:
            configuration (OPTIONAL[ExpectationConfiguration]): \
                An optional Expectation Configuration entry that will be used to configure the expectation
        Returns:
            None. Raises InvalidExpectationConfigurationError if the config is not validated successfully
        """

        super().validate_configuration(configuration)
        if configuration is None:
            configuration = self.configuration

    # This method performs a validation of your metrics against your success keys, returning a dict indicating the success or failure of the Expectation.
    def _validate(
        self,
        configuration: ExpectationConfiguration,
        metrics: Dict,
        runtime_configuration: dict = None,
        execution_engine: ExecutionEngine = None,
    ):
        actual_value = metrics["column.sum"]
        range_of_total = self.get_success_kwargs(configuration).get("sum_total_range")
        if (actual_value >= range_of_total[0]) and (actual_value <= range_of_total[1]):
            success = True
        else:
            success = False
        return {"success": success, "result": {"observed_value": actual_value}}

    # This object contains metadata for display in the public Gallery
    library_metadata = {
        "tags": [
            "column aggregate expectation",
            "hackathon"
        ],  # Tags for this Expectation in the Gallery
        "contributors": [  # Github handles for all contributors to this Expectation.
            "@chetansurwade",  # Don't forget to add your github handle here!
        ],
    }


if __name__ == "__main__":
    ExpectColumnSumToBeWithinRange().print_diagnostic_checklist()
