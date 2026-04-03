import os
from langchain.tools import tool


# 🔹 CORE FUNCTION (used by LangGraph)
def read_file_raw(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()[:5000]
    except Exception as e:
        return f"Error reading file: {str(e)}"


# 🔹 TOOL WRAPPER (used by LangChain — optional now)
@tool
def read_file(file_path: str) -> str:
    """Read full file content"""
    return read_file_raw(file_path)