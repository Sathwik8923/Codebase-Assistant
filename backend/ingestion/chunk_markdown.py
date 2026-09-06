import re

def chunk_markdown_file(file_path: str):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    chunks = []
    current = {"heading": "Introduction", "start_line": 1, "content": []}

    for i, line in enumerate(lines, start=1):
        heading_match = re.match(r"^(#{1,6})\s+(.*)", line)
        if heading_match:
            if current["content"]:
                chunks.append(_finalize(file_path, current, i - 1))
            current = {"heading": heading_match.group(2).strip(), "start_line": i, "content": []}
        current["content"].append(line)

    if current["content"]:
        chunks.append(_finalize(file_path, current, len(lines)))

    return chunks

def _finalize(file_path, current, end_line):
    return {
        "file_path": file_path,
        "type": "doc_section",
        "name": current["heading"],
        "start_line": current["start_line"],
        "end_line": end_line,
        "content": "".join(current["content"]).strip(),
    }