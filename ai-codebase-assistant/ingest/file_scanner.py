import os

ALLOWED_EXTENSIONS = {
    ".py", ".java", ".js", ".ts", ".go", ".cpp", ".c", ".properties"
}

IGNORED_DIRS = {
    ".git", "node_modules", "build", "dist", "__pycache__"
}

MAX_FILE_SIZE = 200 * 1024  # 200KB


def is_valid_file(file_path):
    _, ext = os.path.splitext(file_path)
    return ext in ALLOWED_EXTENSIONS


def scan_repository(repo_path: str):
    code_files = []

    for root, dirs, files in os.walk(repo_path):
        # Remove ignored dirs
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        for file in files:
            file_path = os.path.join(root, file)

            if not is_valid_file(file_path):
                continue

            if os.path.getsize(file_path) > MAX_FILE_SIZE:
                continue

            code_files.append(file_path)

    return code_files