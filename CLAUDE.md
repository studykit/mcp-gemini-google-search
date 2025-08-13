# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Commands

### Dependencies
```bash
# Install/sync dependencies
uv sync
```

### Running the Application
```bash
# Run the MCP server
uv run python src/main.py

# Run with custom gemini CLI path
uv run python src/main.py --gemini-path /path/to/gemini
```

### Testing
```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_main.py

# Run with verbose output
uv run pytest -v
```

### Code Quality
```bash
# Check code with ruff
uv run ruff check .

# Format code with ruff
uv run ruff format .

# Fix auto-fixable issues
uv run ruff check . --fix

# Type checking with pyright
uv run pyright
```

## Architecture Overview

### MCP Server Implementation
This is a FastMCP-based Model Context Protocol (MCP) server that provides Google search functionality through the gemini CLI. The architecture consists of:

1. **Main Server (`src/main.py`)**: FastMCP server that exposes a `google_search` tool. It spawns subprocess calls to the gemini CLI with specific parameters for web search functionality.

2. **Tool Design**: The server implements a single `google_search` tool that:
   - Accepts search queries as input
   - Executes gemini CLI with appropriate flags (`--ide-mode-feature false --allowed-mcp-server-names -y -s -p`)
   - Returns AI-synthesized results from web content
   - Includes timeout handling (5 minutes) and comprehensive error management

3. **Configuration**: 
   - Supports optional `GEMINI_API_KEY` environment variable
   - Allows custom gemini CLI path via `--gemini-path` argument
   - Falls back to default gemini configuration when API key not provided

### Key Technical Details

- **Async Architecture**: Uses asyncio for non-blocking subprocess execution
- **Error Handling**: Comprehensive error handling for CLI failures, timeouts, and missing dependencies
- **Logging**: Structured logging for debugging and monitoring
- **Process Management**: Careful subprocess handling with proper environment variable passing

### Testing Approach
The project uses pytest for testing. Tests should cover:
- MCP server initialization
- Tool registration and execution
- Subprocess handling and error cases
- Timeout scenarios

When adding new functionality, ensure tests are added in the `tests/` directory following the existing pattern.

## Coding Standards

### Type Hints
Always use specific and detailed type hints in all Python code:
- Use precise types instead of generic ones (e.g., `list[str]` instead of `list`)
- Include return types for all functions and methods
- Use `typing` module types when appropriate (`Optional`, `Union`, `Dict`, etc.)
- Annotate class attributes and instance variables
- Use `TypeVar` and generics for reusable type-safe code