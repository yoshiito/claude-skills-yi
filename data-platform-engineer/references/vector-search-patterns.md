# Vector Search Patterns

Patterns for implementing effective vector search and RAG systems.

## Vector Database Selection

| Database | Type | Best For | Trade-offs |
|----------|------|----------|------------|
| **Qdrant** | Dedicated | Production RAG, filtering | Separate service |
| **Pinecone** | Managed | Serverless, quick start | Cost, vendor lock-in |
| **pgvector** | Extension | Unified stack, SQL | Performance at scale |
| **Weaviate** | Dedicated | Hybrid search, GraphQL | Complexity |
| **Milvus** | Dedicated | Large scale, GPU | Operational overhead |
| **Chroma** | Embedded | Development, prototyping | Not for production |

## Embedding Models

| Model | Dimensions | Speed | Quality | Use Case |
|-------|------------|-------|---------|----------|
| `all-MiniLM-L6-v2` | 384 | Fast | Good | General purpose |
| `all-mpnet-base-v2` | 768 | Medium | Better | Higher quality needs |
| `text-embedding-3-small` | 1536 | API | Good | OpenAI ecosystem |
| `text-embedding-3-large` | 3072 | API | Best | Maximum quality |
| `voyage-2` | 1024 | API | Excellent | RAG-optimized |

---

## Chunking Strategies

### Fixed-Size Chunking

```python
def chunk_fixed(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Simple fixed-size chunking with overlap."""
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    
    return chunks
```

**Pros**: Simple, predictable chunk sizes
**Cons**: May split mid-sentence, loses context

### Sentence-Based Chunking

```python
import nltk
nltk.download('punkt')

def chunk_sentences(text: str, sentences_per_chunk: int = 5) -> list[str]:
    """Chunk by sentence boundaries."""
    sentences = nltk.sent_tokenize(text)
    chunks = []
    
    for i in range(0, len(sentences), sentences_per_chunk):
        chunk = ' '.join(sentences[i:i + sentences_per_chunk])
        chunks.append(chunk)
    
    return chunks
```

**Pros**: Preserves sentence integrity
**Cons**: Variable chunk sizes

### Semantic Chunking

```python
from sentence_transformers import SentenceTransformer
import numpy as np

def chunk_semantic(
    text: str, 
    model: SentenceTransformer,
    similarity_threshold: float = 0.8,
    max_chunk_size: int = 1000
) -> list[str]:
    """Chunk based on semantic similarity between sentences."""
    sentences = nltk.sent_tokenize(text)
    embeddings = model.encode(sentences)
    
    chunks = []
    current_chunk = [sentences[0]]
    current_embedding = embeddings[0]
    
    for i in range(1, len(sentences)):
        similarity = np.dot(current_embedding, embeddings[i]) / (
            np.linalg.norm(current_embedding) * np.linalg.norm(embeddings[i])
        )
        
        chunk_text = ' '.join(current_chunk + [sentences[i]])
        
        if similarity >= similarity_threshold and len(chunk_text) <= max_chunk_size:
            current_chunk.append(sentences[i])
            # Update running average embedding
            current_embedding = np.mean(embeddings[i-len(current_chunk)+1:i+1], axis=0)
        else:
            chunks.append(' '.join(current_chunk))
            current_chunk = [sentences[i]]
            current_embedding = embeddings[i]
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks
```

**Pros**: Keeps related content together
**Cons**: More complex, variable sizes

### Document-Aware Chunking

```python
import re

def chunk_markdown(text: str, max_chunk_size: int = 1000) -> list[dict]:
    """Chunk markdown preserving structure."""
    # Split by headers
    sections = re.split(r'(^#{1,6}\s+.+$)', text, flags=re.MULTILINE)
    
    chunks = []
    current_header = None
    
    for section in sections:
        if re.match(r'^#{1,6}\s+', section):
            current_header = section.strip()
        elif section.strip():
            # Further chunk if too large
            if len(section) > max_chunk_size:
                for sub_chunk in chunk_fixed(section, max_chunk_size):
                    chunks.append({
                        'content': sub_chunk,
                        'header': current_header
                    })
            else:
                chunks.append({
                    'content': section.strip(),
                    'header': current_header
                })
    
    return chunks
```

---

## Indexing Strategies

### Qdrant Collection Setup

```python
from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams, Distance, 
    OptimizersConfigDiff, HnswConfigDiff
)

client = QdrantClient(host="localhost", port=6333)

# Create optimized collection
client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    ),
    # Optimize for search speed
    hnsw_config=HnswConfigDiff(
        m=16,                    # Connections per node
        ef_construct=100,        # Build-time search width
        full_scan_threshold=10000  # Use brute force below this
    ),
    optimizers_config=OptimizersConfigDiff(
        indexing_threshold=20000  # Index after this many points
    )
)

# Create payload indexes for filtering
client.create_payload_index(
    collection_name="documents",
    field_name="source",
    field_schema="keyword"
)
client.create_payload_index(
    collection_name="documents",
    field_name="created_at",
    field_schema="datetime"
)
```

### pgvector Index Selection

```sql
-- IVFFlat: Faster to build, good for frequently changing data
CREATE INDEX idx_docs_ivfflat ON documents 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);  -- sqrt(n) to n/1000 lists

-- HNSW: Slower to build, faster queries, better recall
CREATE INDEX idx_docs_hnsw ON documents 
USING hnsw (embedding vector_cosine_ops)
WITH (
    m = 16,              -- Connections per node
    ef_construction = 64  -- Build-time search width
);

-- Set search parameters
SET ivfflat.probes = 10;  -- More probes = better recall, slower
SET hnsw.ef_search = 40;   -- Higher = better recall, slower
```

---

## Retrieval Strategies

### Basic Vector Search

```python
def search_basic(query: str, top_k: int = 5) -> list[dict]:
    """Simple vector similarity search."""
    query_embedding = embed_model.encode(query)
    
    results = qdrant.search(
        collection_name="documents",
        query_vector=query_embedding.tolist(),
        limit=top_k
    )
    
    return [
        {
            'content': hit.payload['content'],
            'score': hit.score,
            'source': hit.payload.get('source')
        }
        for hit in results
    ]
```

### Hybrid Search (Vector + Keyword)

```python
def search_hybrid(
    query: str, 
    top_k: int = 5,
    alpha: float = 0.5  # Balance: 0=keyword, 1=semantic
) -> list[dict]:
    """Combine vector and keyword search."""
    
    # Semantic search
    query_embedding = embed_model.encode(query)
    semantic_results = qdrant.search(
        collection_name="documents",
        query_vector=query_embedding.tolist(),
        limit=top_k * 2
    )
    
    # Keyword search (BM25 or full-text)
    keyword_results = keyword_search(query, limit=top_k * 2)
    
    # Combine scores using Reciprocal Rank Fusion
    combined = {}
    
    for rank, hit in enumerate(semantic_results):
        doc_id = hit.id
        combined[doc_id] = combined.get(doc_id, 0) + alpha / (rank + 60)
    
    for rank, hit in enumerate(keyword_results):
        doc_id = hit['id']
        combined[doc_id] = combined.get(doc_id, 0) + (1 - alpha) / (rank + 60)
    
    # Sort by combined score
    sorted_ids = sorted(combined.keys(), key=lambda x: combined[x], reverse=True)
    
    return fetch_documents(sorted_ids[:top_k])
```

### Filtered Search

```python
from qdrant_client.models import Filter, FieldCondition, MatchValue, Range

def search_filtered(
    query: str,
    source: str = None,
    min_date: str = None,
    top_k: int = 5
) -> list[dict]:
    """Search with metadata filters."""
    
    conditions = []
    
    if source:
        conditions.append(
            FieldCondition(
                key="source",
                match=MatchValue(value=source)
            )
        )
    
    if min_date:
        conditions.append(
            FieldCondition(
                key="created_at",
                range=Range(gte=min_date)
            )
        )
    
    query_embedding = embed_model.encode(query)
    
    results = qdrant.search(
        collection_name="documents",
        query_vector=query_embedding.tolist(),
        query_filter=Filter(must=conditions) if conditions else None,
        limit=top_k
    )
    
    return [hit.payload for hit in results]
```

### Multi-Query Retrieval

```python
def search_multi_query(query: str, top_k: int = 5) -> list[dict]:
    """Generate multiple query variations for better recall."""
    
    # Generate query variations using LLM
    variations_prompt = f"""Generate 3 different ways to ask this question:
    
Original: {query}

Variations (one per line):"""
    
    variations_response = llm.complete(variations_prompt)
    queries = [query] + variations_response.strip().split('\n')
    
    # Search with each query
    all_results = {}
    
    for q in queries:
        embedding = embed_model.encode(q)
        results = qdrant.search(
            collection_name="documents",
            query_vector=embedding.tolist(),
            limit=top_k
        )
        
        for hit in results:
            if hit.id not in all_results:
                all_results[hit.id] = {
                    'payload': hit.payload,
                    'max_score': hit.score
                }
            else:
                all_results[hit.id]['max_score'] = max(
                    all_results[hit.id]['max_score'],
                    hit.score
                )
    
    # Sort by max score across queries
    sorted_results = sorted(
        all_results.values(),
        key=lambda x: x['max_score'],
        reverse=True
    )
    
    return [r['payload'] for r in sorted_results[:top_k]]
```

---

## Reranking

### Cross-Encoder Reranking

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def search_with_rerank(
    query: str,
    initial_k: int = 20,
    final_k: int = 5
) -> list[dict]:
    """Retrieve then rerank with cross-encoder."""
    
    # Initial retrieval (fast, approximate)
    query_embedding = embed_model.encode(query)
    initial_results = qdrant.search(
        collection_name="documents",
        query_vector=query_embedding.tolist(),
        limit=initial_k
    )
    
    # Rerank with cross-encoder (slow, accurate)
    pairs = [
        (query, hit.payload['content']) 
        for hit in initial_results
    ]
    
    scores = reranker.predict(pairs)
    
    # Combine with rerank scores
    reranked = sorted(
        zip(initial_results, scores),
        key=lambda x: x[1],
        reverse=True
    )
    
    return [
        {
            'content': hit.payload['content'],
            'original_score': hit.score,
            'rerank_score': score,
            'source': hit.payload.get('source')
        }
        for hit, score in reranked[:final_k]
    ]
```

### Cohere Rerank API

```python
import cohere

co = cohere.Client(api_key="...")

def rerank_with_cohere(query: str, documents: list[str], top_k: int = 5):
    """Use Cohere's rerank API."""
    results = co.rerank(
        model="rerank-english-v2.0",
        query=query,
        documents=documents,
        top_n=top_k
    )
    
    return [
        {
            'index': r.index,
            'score': r.relevance_score,
            'document': documents[r.index]
        }
        for r in results
    ]
```

---

## Context Window Management

### Truncation Strategy

```python
def prepare_context(
    chunks: list[dict],
    max_tokens: int = 4000,
    query: str = None
) -> str:
    """Fit chunks into context window."""
    
    context_parts = []
    current_tokens = 0
    
    for chunk in chunks:
        chunk_tokens = count_tokens(chunk['content'])
        
        if current_tokens + chunk_tokens > max_tokens:
            break
        
        context_parts.append(
            f"[Source: {chunk.get('source', 'unknown')}]\n{chunk['content']}"
        )
        current_tokens += chunk_tokens
    
    return "\n\n---\n\n".join(context_parts)
```

### Summarization for Long Context

```python
def summarize_if_needed(
    chunks: list[dict],
    max_tokens: int = 4000
) -> list[dict]:
    """Summarize chunks that don't fit."""
    
    total_tokens = sum(count_tokens(c['content']) for c in chunks)
    
    if total_tokens <= max_tokens:
        return chunks
    
    # Summarize each chunk
    summarized = []
    for chunk in chunks:
        if count_tokens(chunk['content']) > max_tokens // len(chunks):
            summary = llm.complete(
                f"Summarize this text concisely:\n\n{chunk['content']}"
            )
            summarized.append({
                **chunk,
                'content': summary,
                'summarized': True
            })
        else:
            summarized.append(chunk)
    
    return summarized
```

---

## Quality Metrics

### Retrieval Evaluation

```python
def evaluate_retrieval(
    queries: list[str],
    ground_truth: dict[str, list[str]],  # query -> relevant doc IDs
    search_fn: callable,
    k: int = 5
) -> dict:
    """Evaluate retrieval quality."""
    
    metrics = {
        'precision_at_k': [],
        'recall_at_k': [],
        'mrr': []  # Mean Reciprocal Rank
    }
    
    for query in queries:
        relevant = set(ground_truth[query])
        results = search_fn(query, top_k=k)
        retrieved = [r['id'] for r in results]
        
        # Precision@k
        hits = len(set(retrieved) & relevant)
        metrics['precision_at_k'].append(hits / k)
        
        # Recall@k
        metrics['recall_at_k'].append(hits / len(relevant) if relevant else 0)
        
        # MRR
        for i, doc_id in enumerate(retrieved):
            if doc_id in relevant:
                metrics['mrr'].append(1 / (i + 1))
                break
        else:
            metrics['mrr'].append(0)
    
    return {
        'precision_at_k': np.mean(metrics['precision_at_k']),
        'recall_at_k': np.mean(metrics['recall_at_k']),
        'mrr': np.mean(metrics['mrr'])
    }
```

---

## Production Checklist

- [ ] Embedding model selected and tested
- [ ] Chunking strategy validated
- [ ] Index type appropriate for scale
- [ ] Metadata indexes for common filters
- [ ] Reranking implemented for quality
- [ ] Context window limits handled
- [ ] Caching for repeated queries
- [ ] Monitoring for latency and quality
- [ ] Backup strategy for vector data
- [ ] Update pipeline for new documents
