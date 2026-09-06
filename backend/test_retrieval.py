from retrieval.store import query_chunks

results = query_chunks("how does the library send an HTTP request")

for doc, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
    print(f"\n--- {meta['file_path']} :: {meta['name']} (lines {meta['start_line']}-{meta['end_line']}) ---")
    print(f"distance: {dist:.4f}")
    print(doc[:200], "...")