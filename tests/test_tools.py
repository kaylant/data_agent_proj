"""Tests for analysis tools"""

import pandas as pd
import pytest
from src.tools import set_dataframe
from src.tools.pandas_tool import execute_pandas_code
from src.tools.stats import get_column_stats, find_correlations
from src.tools.outliers import detect_outliers
from src.tools.patterns import find_patterns


@pytest.fixture(autouse=True)
def setup_dataframe(sample_df):
    """Set the dataframe before each test"""
    set_dataframe(sample_df)


class TestExecutePandasCode:
    def test_simple_count(self):
        result = execute_pandas_code.invoke({"code": "result = len(df)"})
        assert "5" in result

    def test_unique_count(self):
        result = execute_pandas_code.invoke({"code": "result = df['pipeline_name'].nunique()"})
        assert "3" in result

    def test_invalid_code_returns_error(self):
        result = execute_pandas_code.invoke({"code": "result = invalid_variable"})
        assert "Error" in result


class TestGetColumnStats:
    def test_numeric_column(self):
        result = get_column_stats.invoke({"column": "total_scheduled_quantity"})
        assert "total_scheduled_quantity" in result
        assert "Mean" in result
        assert "Null" in result

    def test_string_column(self):
        result = get_column_stats.invoke({"column": "pipeline_name"})
        assert "pipeline_name" in result
        assert "Unique" in result

    def test_invalid_column(self):
        result = get_column_stats.invoke({"column": "nonexistent"})
        assert "Error" in result


class TestFindCorrelations:
    def test_finds_correlations(self):
        result = find_correlations.invoke({"columns": ["design_capacity", "operating_capacity"]})
        assert "correlation" in result.lower()

    def test_default_all_numeric(self):
        result = find_correlations.invoke({})
        assert "correlation" in result.lower()


class TestDetectOutliers:
    def test_iqr_method(self):
        result = detect_outliers.invoke({"column": "total_scheduled_quantity", "method": "iqr"})
        assert "Outlier" in result
        assert "IQR" in result

    def test_zscore_method(self):
        result = detect_outliers.invoke({"column": "total_scheduled_quantity", "method": "zscore"})
        assert "Outlier" in result
        assert "ZSCORE" in result

    def test_invalid_column(self):
        result = detect_outliers.invoke({"column": "nonexistent"})
        assert "Error" in result


class TestFindPatterns:
    def test_group_by_single_column(self):
        result = find_patterns.invoke(
            {
                "group_by": ["pipeline_name"],
                "agg_column": "total_scheduled_quantity",
                "agg_func": "sum",
            }
        )
        assert "Pipeline" in result

    def test_group_by_multiple_columns(self):
        result = find_patterns.invoke(
            {
                "group_by": ["pipeline_name", "location_state_ab"],
                "agg_column": "total_scheduled_quantity",
                "agg_func": "mean",
            }
        )
        assert "Pattern" in result
