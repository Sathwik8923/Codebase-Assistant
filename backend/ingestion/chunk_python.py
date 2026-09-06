import ast

def chunk_python_file(file_path: str):
    """Splits a Python file into function/class-level chunks with line ranges."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []  # skip unparseable files

    lines = source.splitlines()
    chunks = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            start = node.lineno
            end = getattr(node, "end_lineno", start)
            content = "\n".join(lines[start - 1:end])

            chunks.append({
                "file_path": file_path,
                "type": "class" if isinstance(node, ast.ClassDef) else "function",
                "name": node.name,
                "start_line": start,
                "end_line": end,
                "content": content,
            })

    # Fallback: if a file has no functions/classes (e.g. plain scripts), chunk the whole file
    if not chunks:
        chunks.append({
            "file_path": file_path,
            "type": "module",
            "name": file_path,
            "start_line": 1,
            "end_line": len(lines),
            "content": source,
        })

    return chunks