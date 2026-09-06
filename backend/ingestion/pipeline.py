import json
from .walker import clone_repo, walk_repo
from .chunk_python import chunk_python_file
from .chunk_markdown import chunk_markdown_file

def run_ingestion(repo_url: str, output_path: str = "chunks.json"):
    repo_path = clone_repo(repo_url)
    all_chunks = []

    for file_path, ext in walk_repo(repo_path):
        if ext == ".py":
            all_chunks.extend(chunk_python_file(file_path))
        elif ext == ".md":
            all_chunks.extend(chunk_markdown_file(file_path))
        # .js/.jsx: we'll add tree-sitter for this once Python path works

    with open(output_path, "w") as f:
        json.dump(all_chunks, f, indent=2)

    print(f"Indexed {len(all_chunks)} chunks from {repo_path}")
    return all_chunks

if __name__ == "__main__":
    run_ingestion("https://github.com/psf/requests.git")