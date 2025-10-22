# scripts/inspect_vs.py
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from agent_core.rag.vector_store import VectorStore


def main():
    print("🔍 ChromaDB Inspection\n")
    print("=" * 60)

    vs = VectorStore()

    # Total count
    total = vs.count()
    print(f"\n📊 Total chunks: {total}")

    if total == 0:
        print("\n⚠️  Vector store is empty!")
        return

    # List sources
    sources = vs.list_sources()
    print(f"\n📁 Source files ({len(sources)}):")
    for source in sources:
        print(f"  - {source}")

    # Get all data
    results = vs.collection.get()

    # Show samples from each source
    print("\n📄 Sample chunks per file:\n")
    for source in sources:
        print(f"--- {source} ---")

        # Find chunks from this source
        source_chunks = []
        for i, meta in enumerate(results['metadatas']):
            if meta.get('source') == source:
                source_chunks.append({
                    'text': results['documents'][i],
                    'meta': meta
                })

        print(f"Total chunks: {len(source_chunks)}")

        # Show first chunk preview
        if source_chunks:
            first = source_chunks[0]
            preview = first['text'][:200] + "..." if len(first['text']) > 200 else first['text']
            print(f"First chunk preview:\n{preview}")
            print(f"Metadata: {first['meta']}")

        print()

    print("=" * 60)


if __name__ == "__main__":
    main()