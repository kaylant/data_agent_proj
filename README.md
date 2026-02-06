# Data Analysis Agent

A CLI chat agent that answers natural language questions about pipeline data using LangGraph and Anthropic/OpenAPI LLMs.

## Setup

### Prerequisites
- Python 3.10+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

### Installation
```bash
git clone https://github.com/yourusername/data-analysis-agent.git
cd data-analysis-agent
uv sync
```

### Configuration

1. Create a `.env` file in the project root:
```env
ANTHROPIC_API_KEY=your-key-here
# or
OPENAI_API_KEY=your-key-here

# Optional: LangSmith tracing
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-key
LANGCHAIN_PROJECT=data-analysis-agent
```

2. Place the dataset file at `data/pipeline_dataset.parquet`

   (The `data/` directory is gitignored and not included in the repo)

## Usage
```bash
uv run python -m src.main
```

### Commands

| Command | Description |
|---------|-------------|
| `/schema` | Show dataset schema |
| `/clear` | Clear conversation history |
| `/quit` | Exit the agent |

## Example Queries & Outputs

### Deterministic Query
```
You: How many unique pipelines are in the dataset?

Agent: There are **163 unique pipelines** in the dataset.

This count is based on the `pipeline_name` column, which contains the names 
of all the different natural gas pipeline systems represented in the data.

[Response time: 3.42s]
```

### Pattern Recognition (Correlations)
```
You: Find correlations between the capacity columns

Agent: ## Capacity Column Correlations

**Key Findings:**

1. **Very Strong Correlation (0.9990)**: `operating_capacity` ↔ `operationally_available_capacity`
   - Nearly perfect positive correlation
   - These two measures are almost identical in most cases

2. **Moderate Correlations (~0.62-0.63)**:
   - `design_capacity` ↔ `operating_capacity`: 0.6259
   - `design_capacity` ↔ `operationally_available_capacity`: 0.6226

**Interpretation:**
- Operating capacity and operationally available capacity are essentially 
  measuring the same thing in this dataset
- Design capacity represents the theoretical maximum, while operating/operationally 
  available capacity reflects real-world constraints

[Response time: 4.21s]
```

### Anomaly Detection
```
You: Are there outliers in total_scheduled_quantity?

Agent: **Comparison of Methods:**
- **IQR method**: 3.36M outliers (20.18%) - more sensitive to the distribution's shape
- **Z-score method**: 792 outliers (0.005%) - only catches the most extreme values

**Conclusion:**
The outliers appear to be legitimate extreme values rather than data errors. 
The z-score method identifies only the most extreme cases (like the 389 billion maximum), 
while the IQR method captures the broader range of unusually high/low scheduled 
quantities that are still operationally valid but outside typical ranges.

[Response time: 5.67s]
```

### Time Series Analysis
```
You: Analyze the time series trend of total_scheduled_quantity by gas_day

Agent: ## Time Series Analysis: Total Scheduled Quantity Trends

**Key Findings:**

### Overall Trend: **Dramatic Increasing Pattern**
- **Time Period**: April 1, 2023 to December 31, 2025 (1,006 days)
- **Growth**: 152x increase from first day to last day (15,197% growth)

### Temporal Patterns:
- **2023 (Baseline Period)**: Started with relatively low volumes
- **2024 (Growth Phase)**: Significant jump in Q2 2024
- **2025 (Acceleration Phase)**: Massive volume increases across all quarters

**Note**: The extreme growth pattern suggests either significant expansion in 
pipeline capacity/usage, changes in data collection methodology, or addition 
of new pipeline systems to the dataset.

[Response time: 8.34s]
```

### Data Quality Analysis
```
You: What data quality issues exist in this dataset?

Agent: ## Data Quality Issues Identified

### 1. Missing Data (Systematic Gaps)
- **Location coordinates**: 11.92% missing (1.99M records)
- **Design capacity**: 2.57% missing (429K records)
- **Total scheduled quantity**: 1.73% missing (288K records)

### 2. Coordinate Data Problems
- **Invalid latitude values**: 1,418 records outside valid range
- **Suspicious longitude values**: 3,423 records with positive longitude

### 3. Capacity Data Inconsistencies
- **Placeholder values**: 999,999,999 appears as likely missing data indicator
- **Negative capacities**: 4,732 records with negative operationally_available_capacity
- **Logical inconsistencies**: 1.71M records where operating > design capacity

**Recommendation**: Implement data validation rules, coordinate system verification, 
and capacity relationship constraints before analysis.

[Response time: 12.45s]
```

### Multi-turn Conversation
```
You: How many unique pipelines are there?
Agent: There are **163 unique pipelines** in the dataset.

You: Which one has the highest total scheduled quantity?
Agent: **Kern River** has the highest total scheduled quantity at 19.4 trillion units.

You: Tell me more about that pipeline
Agent: ## Kern River Pipeline - Comprehensive Analysis

**Overview:**
- **73,177 records** spanning from April 2023 to December 2025
- **128 unique locations** across the pipeline system
- **Primary states:** California (62 locations), Utah (31), Wyoming (18), Nevada (16)
...
```

## Testing
```bash
# Install dev dependencies
uv sync

# Run all tests
uv run pytest -v

# Run unit tests only (fast, no LLM calls)
uv run pytest tests/test_data_loader.py tests/test_tools.py -v

# Run integration tests only (slower, uses LLM)
uv run pytest tests/test_agent.py -v

# Skip integration tests
uv run pytest -v -m "not integration"
```

## Project Structure
```
data-analysis-agent/
├── src/
│   ├── tools/
│   │   ├── __init__.py      # Tool exports and shared state
│   │   ├── _shared.py       # Shared dataframe access
│   │   ├── pandas_tool.py   # General pandas code execution
│   │   ├── stats.py         # Column stats and correlations
│   │   ├── outliers.py      # Outlier detection
│   │   ├── time_series.py   # Time series analysis
│   │   └── patterns.py      # Pattern finding
│   ├── agent.py             # LangGraph agent with memory
│   ├── data_loader.py       # Dataset loading and schema
│   └── main.py              # CLI entry point
├── tests/
│   ├── conftest.py          # Pytest fixtures
│   ├── test_data_loader.py  # Data loader tests
│   ├── test_tools.py        # Tool unit tests
│   └── test_agent.py        # Agent integration tests
├── data/                    # Dataset directory (gitignored)
├── .env                     # API keys (gitignored)
├── .gitignore
├── pyproject.toml
└── README.md
```

## Available Tools

| Tool | Description |
|------|-------------|
| `execute_pandas_code` | Run arbitrary pandas code against the dataset |
| `get_column_stats` | Detailed statistics for a column |
| `find_correlations` | Correlation analysis between numeric columns |
| `detect_outliers` | IQR or z-score outlier detection |
| `analyze_time_series` | Trend analysis over time |
| `find_patterns` | Group-by aggregation patterns |

## Features

- **Multi-turn conversation**: Agent remembers context within a session
- **Dual LLM support**: Works with Anthropic Claude or OpenAI GPT-4
- **LangSmith tracing**: Optional observability for debugging
- **Response timing**: Shows latency for each query
- **Comprehensive testing**: Unit and integration tests included