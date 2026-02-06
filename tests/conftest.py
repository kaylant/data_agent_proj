"""Pytest fixtures for tests"""

import pandas as pd
import pytest


@pytest.fixture
def sample_df():
    """Create a small sample dataframe for testing"""
    return pd.DataFrame(
        {
            "pipeline_name": ["Pipeline A", "Pipeline A", "Pipeline B", "Pipeline B", "Pipeline C"],
            "location_state_ab": ["TX", "TX", "CA", "CA", "OK"],
            "total_scheduled_quantity": [100.0, 200.0, 150.0, None, 300.0],
            "design_capacity": [500.0, 500.0, 400.0, 400.0, 600.0],
            "operating_capacity": [450.0, 450.0, 380.0, 380.0, 550.0],
            "gas_day": pd.to_datetime(
                ["2024-01-01", "2024-01-02", "2024-01-01", "2024-01-02", "2024-01-01"]
            ),
        }
    )
