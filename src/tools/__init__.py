"""Tools for data analysis agent"""

import pandas as pd

# Shared dataframe reference
_df: pd.DataFrame = None


def set_dataframe(df: pd.DataFrame):
    """Set the dataframe for all tools to use."""
    global _df
    _df = df


# Import tools AFTER _df is defined
from src.tools.outliers import detect_outliers
from src.tools.pandas_tool import execute_pandas_code
from src.tools.patterns import find_patterns
from src.tools.stats import find_correlations, get_column_stats
from src.tools.time_series import analyze_time_series

ALL_TOOLS = [
    execute_pandas_code,
    find_correlations,
    detect_outliers,
    analyze_time_series,
    get_column_stats,
    find_patterns,
]
