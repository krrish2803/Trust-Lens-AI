#!/usr/bin/env python3
"""Generate embeddings for scam phrases using sentence transformers."""
import json
import os
import sys
import argparse
import pickle
import numpy as np
from typing import List, Dict


DATASETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'datasets')
MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend', 'models', 'embeddings')


def load_phrases() -> List[dict]:
    """Load phrases from dataset."""
    filepath = os.path.join(DATASETS_DIR, "hinglish_phrases.json")
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get("phrases", [])


def generate_embeddings(phrases: List[dict], model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> tuple:
    """Generate embeddings for phrases using sentence transformers."""
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(model_name)
    except ImportError:
        print("sentence-transformers not installed. Using fallback...")
        # Fallback: simple TF-IDF-like embedding
        return generate_fallback_embeddings(phrases)
    
    texts = [p.get("phrase", "") for p in phrases]
    # Also include variations
    all_texts = []
    text_to_phrase_idx = []
    for i, p in enumerate(phrases):
        all_texts.append(p.get("phrase", ""))
        text_to_phrase_idx.append(i)
        for v in p.get("variations", []):
            all_texts.append(v)
            text_to_phrase_idx.append(i)
    
    embeddings = model.encode(all_texts, show_progress_bar=True)
    
    return embeddings, all_texts, text_to_phrase_idx


def generate_fallback_embeddings(phrases: List[dict]) -> tuple:
    """Generate simple embeddings without sentence-transformers."""
    from collections import Counter
    
    all_texts = []
    text_to_phrase_idx = []
    for i, p in enumerate(phrases):
        all_texts.append(p.get("phrase", ""))
        text_to_phrase_idx.append(i)
        for v in p.get("variations", []):
            all_texts.append(v)
            text_to_phrase_idx.append(i)
    
    # Create vocabulary
    vocab = set()
    for text in all_texts:
        vocab.update(text.lower().split())
    vocab = sorted(vocab)
    word_to_idx = {w: i for i, w in enumerate(vocab)}
    
    # Create simple TF embeddings
    embeddings = np.zeros((len(all_texts), len(vocab)))
    for i, text in enumerate(all_texts):
        words = text.lower().split()
        word_counts = Counter(words)
        for word, count in word_counts.items():
            if word in word_to_idx:
                embeddings[i][word_to_idx[word]] = count
    
    return embeddings, all_texts, text_to_phrase_idx


def save_embeddings(embeddings, all_texts, text_to_phrase_idx, output_dir: str):
    """Save embeddings to disk."""
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, "hinglish_phrases.pkl")
    with open(output_path, 'wb') as f:
        pickle.dump({
            "embeddings": embeddings,
            "texts": all_texts,
            "text_to_phrase_idx": text_to_phrase_idx,
            "shape": embeddings.shape if hasattr(embeddings, 'shape') else None
        }, f)
    
    print(f"✓ Embeddings saved to {output_path}")
    print(f"  Shape: {embeddings.shape if hasattr(embeddings, 'shape') else (len(embeddings), len(embeddings[0]) if embeddings else 0)}")
    print(f"  Total texts: {len(all_texts)}")


def test_similarity(embeddings, all_texts, text_to_phrase_idx, test_pairs: List[tuple]):
    """Test semantic similarity between phrase pairs."""
    try:
        from sklearn.metrics.pairwise import cosine_similarity
    except ImportError:
        print("sklearn not installed, skipping similarity test")
        return
    
    print("\nSimilarity Tests:")
    print("-" * 60)
    for text1, text2 in test_pairs:
        idx1 = all_texts.index(text1) if text1 in all_texts else -1
        idx2 = all_texts.index(text2) if text2 in all_texts else -1
        
        if idx1 >= 0 and idx2 >= 0:
            sim = cosine_similarity(
                embeddings[idx1].reshape(1, -1),
                embeddings[idx2].reshape(1, -1)
            )[0][0]
            print(f"  '{text1}' <-> '{text2}'")
            print(f"  Similarity: {sim:.4f}")
        else:
            print(f"  '{text1}' or '{text2}' not found in embeddings")


def main():
    parser = argparse.ArgumentParser(description="Generate embeddings for TrustLens AI phrases")
    parser.add_argument("--model", type=str, default="sentence-transformers/all-MiniLM-L6-v2",
                       help="Sentence transformer model name")
    parser.add_argument("--output", type=str, default=MODELS_DIR,
                       help="Output directory for embeddings")
    parser.add_argument("--test-similarity", action="store_true",
                       help="Run similarity tests after generation")
    args = parser.parse_args()
    
    print("Loading phrases...")
    phrases = load_phrases()
    print(f"Loaded {len(phrases)} phrases")
    
    print(f"\nGenerating embeddings with model: {args.model}")
    embeddings, all_texts, text_to_phrase_idx = generate_embeddings(phrases, args.model)
    
    print(f"\nSaving embeddings...")
    save_embeddings(embeddings, all_texts, text_to_phrase_idx, args.output)
    
    if args.test_similarity:
        test_pairs = [
            ("aapka account band hoga", "account will be suspended"),
            ("OTP share karein", "share the OTP"),
            ("prize mila hai", "you have won a prize"),
            ("bank se call hai", "calling from bank"),
            ("turant paisa bhejein", "send money immediately"),
        ]
        test_similarity(embeddings, all_texts, text_to_phrase_idx, test_pairs)
    
    print("\n✓ Done!")


if __name__ == "__main__":
    main()
