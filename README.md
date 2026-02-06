# Data Analysis Agent

A CLI chat agent that answers natural language questions about pipeline data using LangGraph and  Anthropic/OpenAPI LLMs.

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
| `/quit` | Exit the agent |

### Example Queries
```
You: How many unique pipelines are in the dataset?
Agent: There are 163 unique pipelines in the dataset.

You: What states have the most pipeline locations?
Agent: The top 5 states by number of pipeline locations are...

You: Are any of the counties Tarrant County??
Agent: No, there are no counties named "Tarrant County" in this dataset.

My analysis shows that:
- Neither the `location_county` nor `location_county_composite` columns contain "Tarrant County"
- There are no entries containing "Tarrant" in any form in either county column
- The count of records with "Tarrant" is 0 in both county-related columns
```

## Project Structure
```
data-analysis-agent/
├── src/
│   ├── agent.py       # LangGraph agent
│   ├── data_loader.py # Dataset loading and schema
│   ├── tools.py       # Pandas execution tool
│   └── main.py        # CLI entry point
├── data/              # Dataset directory (gitignored)
├── .env               # API keys (gitignored)
├── .gitignore
├── pyproject.toml
└── README.md
```

## Requirements

- langchain
- langchain-anthropic
- langchain-openai
- langgraph
- pandas
- pyarrow
- python-dotenv