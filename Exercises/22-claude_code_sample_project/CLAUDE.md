# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Setup
uv venv && source .venv/bin/activate
uv pip install -e .

# Run the MCP server
uv run main.py

# Run all tests
uv run pytest

# Run a single test
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_pdf
```

No linter is configured in this project.

## Architecture

This is an **MCP (Model Context Protocol) server** that exposes tools for AI assistants (like Claude).

**Flow:** `main.py` creates a `FastMCP` server instance, registers tool functions via `mcp.tool()`, and runs the server. Tools receive structured calls from AI assistants over the MCP protocol.

**Tool modules** (`tools/`):
- `math.py` — arithmetic tools (currently `add`)
- `document.py` — converts binary document data (PDF, DOCX) to markdown via `markitdown`

**Note:** `document.py` defines `binary_document_to_markdown` but it is not currently registered in `main.py`. To expose it, add `mcp.tool()(binary_document_to_markdown)` after importing it.

## Tool Definition Convention

Tools are plain Python functions registered with `mcp.tool()`. Follow the pattern in `tools/math.py`:

- Use `pydantic.Field` for parameter descriptions (this becomes the schema the AI sees)
- Docstring should include: one-line summary, detailed explanation, when to use, and examples
- Return type annotation is required

```python
from pydantic import Field

def my_tool(
    param: str = Field(description="What this parameter does"),
) -> str:
    """One-line summary.

    Detailed explanation...

    When to use:
    - ...

    Examples:
    >>> my_tool("input")
    "output"
    """
    ...
```

Register in `main.py`:
```python
mcp.tool()(my_tool)
```

## Tests

Tests live in `tests/` and use pytest. Fixture files (`.docx`, `.pdf`) are in `tests/fixtures/`. When adding new document formats, add corresponding fixture files there.
