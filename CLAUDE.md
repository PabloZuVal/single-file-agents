# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands
- **Run agents**: `uv run <agent_filename.py> [options]`
- **Install uv**: `curl -LsSf https://astral.sh/uv/install.sh | sh`

## Environment Setup
Set API keys before running agents:
```bash
export GEMINI_API_KEY='your-api-key-here'
export OPENAI_API_KEY='your-api-key-here'
export ANTHROPIC_API_KEY='your-api-key-here'
export FIRECRAWL_API_KEY='your-api-key-here'  # Get from https://www.firecrawl.dev/
```

## Code Architecture
This repository demonstrates Single File Agents (SFA) - powerful, self-contained AI agents that pack all functionality into a single Python file using `uv` for dependency management.

### Key Design Patterns
1. **Single File Architecture**: Each agent is completely self-contained with embedded dependencies via `/// script` comments
2. **Tool-based Design**: Agents use function calling/tool use patterns from OpenAI, Anthropic, and Gemini
3. **Iterative Compute Loops**: Most agents support `-c` flag for multiple compute iterations
4. **Consistent CLI Interface**: All agents use argparse with similar patterns for database paths, prompts, and output

### Agent Categories
- **Database Agents** (DuckDB, SQLite): Generate and execute SQL queries with schema discovery
- **Data Processing** (JQ, Polars CSV): Transform and analyze JSON/CSV data
- **File Manipulation** (Bash Editor): Edit files and execute commands with AI assistance
- **Web Scraping** (Scrapper Agent): Extract content from websites using Firecrawl API
- **Meta Tools** (Meta Prompt Generator): Generate structured prompts for other AI systems

## Development Guidelines
- File naming: `sfa_<capability>_<provider>_v<version>.py`
- Dependencies: Specified at file top in `/// script` comments
- Error handling: User-friendly messages with rich console output
- Testing: Use provided test data in `data/` directory (analytics.db, analytics.json, etc.)

## Quick Examples
```bash
# DuckDB query
uv run sfa_duckdb_openai_v2.py -d ./data/analytics.db -p "Show users with score > 80"

# JQ command generation
uv run sfa_jq_gemini_v1.py --exe "Filter scores above 80 from data/analytics.json"

# File editing with AI
uv run sfa_bash_editor_agent_anthropic_v2.py --prompt "Create hello.txt with 'Hello World!'"

# CSV analysis
uv run sfa_polars_csv_agent_openai_v2.py -i "data/analytics.csv" -p "Average age of users?"
```