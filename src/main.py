#!/usr/bin/env python3
"""
Gemini MCP Server

An MCP server that provides Google search functionality using the gemini CLI.
"""

import argparse
import asyncio
import logging
import os
import sys

from mcp.server import FastMCP


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("gemini-mcp")

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Gemini MCP Server")
parser.add_argument(
  "--gemini-path", default="gemini", help="Path to gemini CLI (default: gemini)"
)
args, remaining = parser.parse_known_args()

# Store gemini CLI path
GEMINI_CLI_PATH: str = args.gemini_path
logger.info(f"Using gemini CLI path: {GEMINI_CLI_PATH}")

# Reset sys.argv to remaining args for MCP
sys.argv = [sys.argv[0]] + remaining

# Create FastMCP server instance with instructions for clients
mcp = FastMCP(
  "Gemini MCP Server",
  instructions="""
## Gemini Google Search MCP Server

This server provides AI-powered Google search using Gemini, delivering synthesized answers from current web content.

### Key Capabilities:
- Access to real-time web information beyond training data cutoffs
- Intelligent synthesis of multiple sources into comprehensive answers
- Automatic source attribution and citation when available

### Recommended Use Cases:
- Current events, news, and recent developments
- Up-to-date technical documentation and API references
- Comparative analysis requiring current data
- Fact-checking with recent sources
- Technical problem-solving with community knowledge

### Response Characteristics:
- Typical response time: 5-15 seconds depending on query complexity
- Responses include markdown formatting, code blocks, and structured lists
- Always display full responses to preserve context and formatting
""",
)


@mcp.tool()
async def google_search(query: str) -> str:
  """
  Execute a Google search with Gemini AI synthesis.

  Args:
      query: Search query string (question, topic, or keywords).
             Examples:
             - "latest React 19 features"
             - "how to implement OAuth 2.0 PKCE"
             - "compare Python vs Rust performance"
             - "current inflation rates US 2024"

  Returns:
      str: Gemini-generated response synthesizing web search results.
           Includes relevant information with source attribution when available.

  Raises:
      RuntimeError: If Gemini CLI is unavailable, times out, or returns an error.

  Note:
      Response time varies by query complexity (typically 5-15 seconds).
      Display complete response to preserve formatting and context.
  """
  try:
    # Check if gemini CLI is available
    await _check_gemini_availability()

    # Build gemini command with Google search prompt
    cmd: list[str] = [
      GEMINI_CLI_PATH,
      "--ide-mode-feature",
      "false",
      "--allowed-mcp-server-names",
      "-y",
      "-s",
      "-p",
      query + "\n Please always include source information and cite where the information comes from.",
    ]

    logger.info(f"Executing gemini search: {' '.join(cmd)}")

    # Execute gemini CLI command with environment variables
    env = os.environ.copy()
    process = await asyncio.create_subprocess_exec(
      *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, env=env
    )

    # Use wait_for to implement timeout
    stdout, stderr = await asyncio.wait_for(
      process.communicate(),
      timeout=300.0,  # 5 minute timeout
    )

    if process.returncode != 0:
      error_msg = stderr.decode("utf-8").strip() if stderr else "Unknown error"
      logger.error(
        f"Gemini CLI failed with return code {process.returncode}: {error_msg}"
      )
      raise RuntimeError(f"Gemini CLI failed: {error_msg}")

    # Return raw text output from gemini
    raw_output = stdout.decode("utf-8").strip()
    if not raw_output:
      logger.warning("Empty output from gemini CLI")
      return f"No results found for query: {query}"

    return raw_output

  except asyncio.TimeoutError:
    logger.error("Gemini CLI timed out")
    raise RuntimeError("Search request timed out")
  except FileNotFoundError:
    logger.error("Gemini CLI not found")
    raise RuntimeError("Gemini CLI is not installed or not found in PATH")
  except Exception as e:
    logger.error(f"Unexpected error during search: {str(e)}")
    raise RuntimeError(f"Search failed: {str(e)}")


async def _check_gemini_availability():
  """Check if gemini CLI is available."""
  # Check if GEMINI_API_KEY is set (optional)
  api_key = os.environ.get("GEMINI_API_KEY")
  if not api_key:
    logger.info(
      "GEMINI_API_KEY environment variable is not set - using default gemini configuration"
    )
  else:
    logger.debug("GEMINI_API_KEY is configured")

  import shutil

  if not shutil.which(GEMINI_CLI_PATH):
    raise RuntimeError("Gemini CLI is not installed or not accessible")

  logger.debug("Gemini CLI is available")


if __name__ == "__main__":
  mcp.run()
