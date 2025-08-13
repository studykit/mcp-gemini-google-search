# Gemini Google Search MCP Server

A Model Context Protocol (MCP) server that provides AI-powered Google search functionality using Gemini. This server allows you to perform web searches and get synthesized, intelligent responses from current web content.

## Features

- Real-time Google search through Gemini AI
- Intelligent synthesis of multiple web sources
- Automatic source attribution and citations
- Integration with Claude Desktop and other MCP clients

## Installation

### Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- [Gemini CLI](https://ai.google.dev/gemini-api/docs/cli) installed and configured

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/studykit/mcp-gemini-google-search.git
   cd mcp-gemini-google-search
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Configure Gemini CLI:**
   - Install the Gemini CLI following the [official guide](https://ai.google.dev/gemini-api/docs/cli)
   - Set up your API key or configure authentication as needed

4. **Test the installation:**
   ```bash
   uv run python src/main.py
   ```

## Claude Desktop Integration

To use this MCP server with Claude Desktop, add it to your MCP configuration:

### 1. Open Claude Desktop Settings

- Open Claude Desktop
- Go to Settings → Developer → Edit Config

### 2. Add MCP Server Configuration

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "gemini-google-search": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/mcp-gemini-google-search",
        "run",
        "python",
        "src/main.py"
      ]
    }
  }
}
```

### 3. Update Configuration Path

Replace `/path/to/mcp-gemini-google-search` with the actual path where you cloned this repository.

### 4. API Key Configuration (Optional)

The `GEMINI_API_KEY` environment variable is optional. When not provided:
- The server will use the default Gemini CLI configuration
- Gemini CLI will attempt to use its locally configured authentication
- This typically works if you've already run `gemini config` or have API keys configured through other Gemini CLI setup methods

If you need to provide a specific API key, add the `env` section:

```json
{
  "mcpServers": {
    "gemini-google-search": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/mcp-gemini-google-search",
        "run",
        "python",
        "src/main.py"
      ],
      "env": {
        "GEMINI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### 5. Custom Gemini CLI Path (Optional)

If your Gemini CLI is installed in a non-standard location, you can specify the path:

```json
{
  "mcpServers": {
    "gemini-google-search": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/mcp-gemini-google-search",
        "run",
        "python",
        "src/main.py",
        "--gemini-path",
        "/path/to/gemini"
      ]
    }
  }
}
```

### 6. Restart Claude Desktop

After saving the configuration, restart Claude Desktop for the changes to take effect.

## Usage

Once configured, you can use the Google search functionality in Claude Desktop by asking questions that require current web information:

- "What are the latest developments in AI?"
- "Find recent news about climate change"
- "Search for current Python best practices"

The server will automatically search the web using Gemini and provide synthesized, up-to-date answers with source attribution.

## Configuration

### Environment Variables

- `GEMINI_API_KEY`: Your Gemini API key (optional - falls back to Gemini CLI default configuration)

### Command Line Arguments

- `--gemini-path`: Path to the Gemini CLI executable (optional)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
