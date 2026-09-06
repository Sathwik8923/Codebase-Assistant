import os
import stat
import shutil
from git import Repo

SUPPORTED_EXTENSIONS = {".py", ".md", ".js", ".jsx"}

def _remove_readonly(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def clone_repo(repo_url: str, dest_path: str = "./cloned_repos/tmp_repo"):
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path, onerror=_remove_readonly)
    Repo.clone_from(repo_url, dest_path)
    return dest_path

def walk_repo(repo_path: str):
    """Yields (file_path, extension) for every relevant file, skipping junk dirs."""
    skip_dirs = {".git", "node_modules", "venv", "__pycache__", "dist", "build"}
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for f in files:
            ext = os.path.splitext(f)[1]
            if ext in SUPPORTED_EXTENSIONS:
                yield os.path.join(root, f), ext