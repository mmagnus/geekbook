#!/usr/bin/env python3
"""
RAG system for querying your geekbook notes using Claude.

Usage:
    python notes_rag.py index          # Build/rebuild the search index
    python notes_rag.py ask "question"  # Ask a question about your notes
    python notes_rag.py chat           # Interactive chat mode
    python notes_rag.py todos          # Summarize TODOs from org files
"""

import os
import sys
import glob
import pickle

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import anthropic

NOTES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notes")
INDEX_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".notes_index.pkl")
TOP_K = 15


def load_notes():
    """Load all notes (.md, .org, .txt) from the notes directory."""
    notes = []
    for ext in ("**/*.md", "**/*.org", "**/*.txt"):
        for filepath in glob.glob(os.path.join(NOTES_DIR, ext), recursive=True):
            try:
                with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read().strip()
                if content:
                    filename = os.path.relpath(filepath, NOTES_DIR)
                    title = filename.rsplit(".", 1)[0].replace("-", " ")
                    notes.append({
                        "filename": filename,
                        "text": f"Title: {title}\n\n{content}",
                    })
            except Exception as e:
                print(f"  Skipping {filepath}: {e}")
    return notes


def build_index():
    """Build the TF-IDF search index from notes."""
    print("Loading notes...")
    notes = load_notes()
    print(f"Found {len(notes)} notes")

    print("Building TF-IDF index...")
    texts = [n["text"] for n in notes]
    filenames = [n["filename"] for n in notes]

    vectorizer = TfidfVectorizer(
        max_features=50000,
        stop_words="english",
        ngram_range=(1, 2),
        sublinear_tf=True,
    )
    tfidf_matrix = vectorizer.fit_transform(texts)

    index = {
        "vectorizer": vectorizer,
        "tfidf_matrix": tfidf_matrix,
        "filenames": filenames,
        "texts": texts,
    }

    with open(INDEX_PATH, "wb") as f:
        pickle.dump(index, f)

    print(f"Done! Index saved to {INDEX_PATH} ({len(notes)} notes indexed)")


def load_index():
    """Load the search index from disk."""
    with open(INDEX_PATH, "rb") as f:
        return pickle.load(f)


def query_notes(question, top_k=TOP_K):
    """Query notes and return the most relevant ones."""
    index = load_index()
    query_vec = index["vectorizer"].transform([question])
    scores = (index["tfidf_matrix"] @ query_vec.T).toarray().flatten()

    # Boost scores for filename matches
    query_lower = question.lower()
    query_words = query_lower.split()
    for i, filename in enumerate(index["filenames"]):
        fname_lower = filename.lower()
        for word in query_words:
            if len(word) > 2 and word in fname_lower:
                scores[i] += 0.5

    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []
    sources = set()
    for i in top_indices:
        if scores[i] > 0:
            results.append({"text": index["texts"][i], "source": index["filenames"][i], "score": scores[i]})
            sources.add(index["filenames"][i])
    return results, sources


def ask(question):
    """Ask a question about your notes."""
    if not os.path.exists(INDEX_PATH):
        print("Index not found. Run 'python notes_rag.py index' first.")
        sys.exit(1)

    print("Searching notes...")
    results, sources = query_notes(question)

    if not results:
        print("No relevant notes found.")
        return

    # Build context — truncate each note to keep within token limits
    context_parts = []
    total_chars = 0
    max_chars = 30000  # ~7500 tokens, leaves room for the answer
    for r in results:
        snippet = r["text"][:3000]  # max 3k chars per note
        if total_chars + len(snippet) > max_chars:
            break
        context_parts.append(f"[From: {r['source']}]\n{snippet}")
        total_chars += len(snippet)

    context = "\n\n---\n\n".join(context_parts)

    client = anthropic.Anthropic()
    print("Thinking...\n")

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        system=(
            "You are a helpful assistant that answers questions based on the user's personal notes. "
            "Use ONLY the provided note excerpts to answer. If the notes don't contain enough "
            "information, say so. Always cite which note file(s) your answer comes from. "
            "Be concise but thorough."
        ),
        messages=[
            {
                "role": "user",
                "content": (
                    f"Here are relevant excerpts from my notes:\n\n{context}\n\n"
                    f"---\n\nQuestion: {question}"
                ),
            }
        ],
    )

    answer = response.content[0].text
    print(answer)
    print(f"\nSources: {', '.join(sorted(sources))}")
    return answer


def chat():
    """Interactive chat mode."""
    if not os.path.exists(INDEX_PATH):
        print("Index not found. Run 'python notes_rag.py index' first.")
        sys.exit(1)

    print("Notes Chat -- ask questions about your notes (type 'quit' to exit)\n")

    while True:
        try:
            question = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not question:
            continue
        if question.lower() in ("quit", "exit", "q"):
            print("Bye!")
            break

        print()
        ask(question)
        print()


def todos():
    """Extract and summarize TODO/action items from org files using Claude."""
    import re

    org_files = glob.glob(os.path.join(NOTES_DIR, "*.org"))
    all_items = []

    for filepath in org_files:
        try:
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except Exception:
            continue

        filename = os.path.basename(filepath)
        lines = content.split("\n")
        items = []
        for line in lines:
            stripped = line.strip()
            # Match org-mode TODOs, unchecked boxes, WAITING, NEXT, DEADLINE, SCHEDULED
            if re.match(r"^\*+\s+(TODO|NEXT|WAITING)\s+", stripped):
                items.append(stripped)
            elif re.match(r"^-\s+\[ \]", stripped):
                items.append(stripped)
            elif "DEADLINE:" in stripped or "SCHEDULED:" in stripped:
                items.append(stripped)

        if items:
            all_items.append(f"[From: {filename}]\n" + "\n".join(items))

    if not all_items:
        print("No TODO items found in org files.")
        return

    context = "\n\n---\n\n".join(all_items)
    print(f"Found action items across {len(all_items)} org files. Asking Claude to summarize...\n")

    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        system=(
            "You are a helpful assistant reviewing the user's org-mode TODO items. "
            "Organize them by priority/urgency. Highlight the most important actionable items. "
            "Group by file/project. Skip items that look completed or stale. Be concise."
        ),
        messages=[
            {
                "role": "user",
                "content": (
                    f"Here are all my open TODO items from my org-mode files:\n\n{context}\n\n"
                    "---\n\nSummarize what's important and what I should focus on."
                ),
            }
        ],
    )

    print(response.content[0].text)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "index":
        build_index()
    elif command == "ask":
        if len(sys.argv) < 3:
            print('Usage: python notes_rag.py ask "your question"')
            sys.exit(1)
        question = " ".join(sys.argv[2:])
        ask(question)
    elif command == "chat":
        chat()
    elif command == "todos":
        todos()
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
