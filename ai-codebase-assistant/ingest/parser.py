import os

EXTENSION_LANGUAGE_MAP = {
    ".py": "python",
    ".java": "java",
    ".js": "javascript",
    ".ts": "typescript",
    ".go": "go",
    ".cpp": "cpp",
    ".c": "c"
}


def detect_language(file_path: str) -> str:
    _, ext = os.path.splitext(file_path)
    return EXTENSION_LANGUAGE_MAP.get(ext, "unknown")


def read_file(file_path: str) -> dict:
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        return {
            "file": file_path,
            "content": content,
            "language": detect_language(file_path)
        }

    except Exception as e:
        print(f"[ERROR] Failed reading {file_path}: {e}")
        return None