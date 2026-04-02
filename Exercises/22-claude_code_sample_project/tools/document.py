from pathlib import Path

from markitdown import MarkItDown, StreamInfo
from io import BytesIO
from pydantic import Field


def binary_document_to_markdown(binary_data: bytes, file_type: str) -> str:
    """Converts binary document data to markdown-formatted text."""
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content


def document_path_to_markdown(
    file_path: str = Field(description="Absolute or relative path to the document file (PDF, DOCX, etc.)"),
) -> str:
    """Convert a document file to markdown-formatted text.

    Reads the document at the given file path and converts its content to
    markdown. Supports PDF, DOCX, and any other format supported by markitdown.

    When to use:
    - When you have a file path to a document and need its text content
    - When you need to extract readable content from PDF or Word files

    When not to use:
    - When you already have the binary data — use binary_document_to_markdown instead

    Examples:
    >>> document_path_to_markdown("/tmp/report.pdf")
    "# Report Title\\n..."
    >>> document_path_to_markdown("docs/manual.docx")
    "# Manual\\n..."
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    extension = path.suffix.lstrip(".")
    binary_data = path.read_bytes()
    return binary_document_to_markdown(binary_data, extension)
