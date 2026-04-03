from ingest.clone_repo import clone_repository
from ingest.file_scanner import scan_repository
from ingest.parser import read_file


def ingest_repository(repo_url: str):
    repo_path = clone_repository(repo_url)

    print("[INFO] Scanning files...")
    files = scan_repository(repo_path)

    print(f"[INFO] Found {len(files)} files")

    documents = []

    for file_path in files:
        parsed = read_file(file_path)
        if parsed:
            documents.append(parsed)

    print(f"[INFO] Parsed {len(documents)} files")

    return documents