# Data Analysis Agent

A CLI chat agent that answers natural language questions about pipeline data using LangGraph and Anthropic/OpenAI LLMs.

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

   (The `data/` directory is gitignored and not included in this repo)

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

[Response time: 3.42s]
```

### Pattern Recognition (Correlations)
```
You: Find correlations between the capacity columns

Agent: ## Capacity Column Correlations

**Key Findings:**

1. **Very Strong Correlation (0.9990)**: `operating_capacity` ↔ `operationally_available_capacity`
2. **Moderate Correlations (~0.62-0.63)**: `design_capacity` ↔ `operating_capacity`

**Interpretation:**
- Operating capacity and operationally available capacity are essentially 
  measuring the same thing in this dataset
- Design capacity represents the theoretical maximum, while operating capacity 
  reflects real-world constraints

[Response time: 4.21s]
```

### Anomaly Detection
```
You: Are there outliers in total_scheduled_quantity?

Agent: **Comparison of Methods:**
- **IQR method**: 3.36M outliers (20.18%)
- **Z-score method**: 792 outliers (0.005%)

**Conclusion:**
The outliers appear to be legitimate extreme values rather than data errors.

[Response time: 5.67s]
```

### Data Quality Analysis
```
You: Run a data quality report

Agent: ## Data Quality Report Summary

### **Critical Issues (High Impact)**
- **7.6% of records** have operating capacity exceeding design capacity
- **11.9% missing coordinates** - affects any geographic analysis

### **Moderate Concerns**
- **44% of scheduled quantity values are zero**
- **5.5% of capacity values are zero or placeholder values** (999999999)

### **Recommendations**
1. For capacity analysis: Exclude rows where operating > design capacity
2. For volume analysis: Consider whether zero values should be included
3. For geographic analysis: Use only records with valid coordinates

[Response time: 28.63s]
```

### Pipeline Segmentation
```
You: Find segments of pipelines by total_scheduled_quantity

Agent: ## Pipeline Segments by Total Scheduled Quantity

**🔴 Top Tier (25% of pipelines - 41 pipelines)**
- **99.5% of total gas volume** (20.1 trillion units)
- Examples: Kern River, Transcontinental (Transco)

**🔵 Bottom Tier (25% of pipelines - 41 pipelines)**
- **<0.1% of total volume** (1 billion units)

### **Key Business Insight**
Just 41 pipelines (25%) handle virtually all gas transport. 
Scale disparity: Top tier pipelines move 18,800x more gas than bottom tier.

[Response time: 12.38s]
```

### Cluster Analysis
```
You: Cluster the data using design_capacity, operating_capacity, and total_scheduled_quantity

Agent: ## Cluster Analysis: Pipeline Capacity and Volume Patterns

### **Cluster 0: Standard Operations (99.9% of data)**
- Normal day-to-day pipeline operations with moderate capacities

### **Cluster 1: High-Capacity Placeholders (6 records)**
- Likely **data quality issues** - placeholder values (999,999,999)

### **Cluster 2: High-Volume Operations (26 records)**
- **Major transmission hubs** - high capacity, high utilization

**Recommendation**: Focus analysis on Clusters 0, 2, and 4 while excluding 
data quality issues in Clusters 1 and 3.

[Response time: 37.50s]
```

### Confounder Analysis
```
You: Check if the relationship between design_capacity and total_scheduled_quantity is confounded by region_nat_gas

Agent: ## Key Finding: Strong Regional Confounding Detected

**Evidence of Confounding:**
- Overall correlation is near zero (r = 0.0003)
- **Dramatic variation by region**:
  - Southeast: Strong positive (r = 0.73)
  - West: Virtually none (r = 0.003)

**Recommendation**: Always stratify capacity analyses by region, as the 
relationship varies dramatically across different natural gas regions.

[Response time: 29.76s]
```

### Robustness Checks
```
You: Run robustness checks on the top pipelines by total_scheduled_quantity

Agent: ## Robustness Check Results

### **✅ Passed 3/4 tests**
- Temporal Consistency: Rankings stable over time
- Sample Stability: Perfect 5/5 overlap across random samples

### **⚠️ Failed 1/4 tests**  
- Outlier Sensitivity: Rankings change when extreme values removed

**Conclusion**: The finding that a small number of pipelines dominate gas 
transport is **robust and reliable**, though exact rankings depend on 
whether you include peak volume events.

[Response time: 83.46s]
```

### Multi-turn Conversation
```
You: How many unique pipelines are there?
Agent: There are **163 unique pipelines** in the dataset.

You: Which one has the highest total scheduled quantity?
Agent: **Kern River** has the highest total scheduled quantity at 19.4 trillion units.

You: Tell me more about that pipeline
Agent: ## Kern River Pipeline - Comprehensive Analysis
- **73,177 records** spanning from April 2023 to December 2025
- **128 unique locations** across the pipeline system
- **Primary states:** California (62 locations), Utah (31), Wyoming (18)
```

## Testing
```bash
# Install dev dependencies
uv sync

# Run all tests
uv run pytest -v

# Run unit tests only (fast, no LLM calls)
uv run pytest tests/test_data_loader.py tests/test_tools.py tests/test_bonus_tools.py -v

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
│   │   ├── __init__.py       # Tool exports and shared state
│   │   ├── _shared.py        # Shared dataframe access
│   │   ├── pandas_tool.py    # General pandas code execution
│   │   ├── stats.py          # Column stats and correlations
│   │   ├── outliers.py       # Outlier detection
│   │   ├── time_series.py    # Time series analysis
│   │   ├── patterns.py       # Pattern finding
│   │   ├── clustering.py     # Clustering and segmentation
│   │   ├── data_quality.py   # Data quality checks
│   │   └── validation.py     # Robustness and confounder checks
│   ├── agent.py              # LangGraph agent with memory
│   ├── data_loader.py        # Dataset loading and schema
│   └── main.py               # CLI entry point
├── tests/
│   ├── conftest.py           # Pytest fixtures
│   ├── test_data_loader.py   # Data loader tests
│   ├── test_tools.py         # Core tool unit tests
│   └── test_agent.py         # Agent integration tests
├── data/                     # Dataset directory (gitignored)
├── .env                      # API keys (gitignored)
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
| `cluster_analysis` | K-means clustering for non-obvious segments |
| `find_segments` | Segment entities by metric (quartiles/kmeans) |
| `data_quality_report` | Comprehensive data quality assessment |
| `compare_with_without_issues` | Show how data issues affect conclusions |
| `check_confounders` | Analyze if relationships are confounded |
| `robustness_check` | Validate findings under different conditions |

## Features

- **Multi-turn conversation**: Agent remembers context within a session
- **Dual LLM support**: Works with Anthropic Claude or OpenAI GPT-4
- **LangSmith tracing**: Optional observability for debugging
- **Response timing**: Shows latency for each query
- **Comprehensive testing**: Unit and integration tests included
- **Analytics validation**: Clustering, segmentation, data quality, confounder analysis, robustness checks