# AI Integration Patterns

Detailed implementation guidance for common AI integration patterns.

## Pattern 1: Zero-Shot Prompting

### When to Use
- Well-defined tasks with clear instructions
- Model has strong baseline capability
- Quick iteration needed

### Implementation

```python
from anthropic import Anthropic

client = Anthropic()

def classify_intent(message: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=50,
        messages=[{
            "role": "user",
            "content": f"""Classify this customer message into exactly one category:
- billing: payment, invoice, subscription, refund
- technical: bugs, errors, how-to, features
- general: other inquiries

Message: {message}

Category:"""
        }]
    )
    return response.content[0].text.strip().lower()
```

### Best Practices
- Be explicit about output format
- List all valid categories
- Provide category definitions
- Request single-word responses for classification

---

## Pattern 2: Few-Shot Prompting

### When to Use
- Need consistent output format
- Edge cases need demonstration
- Model struggles with zero-shot

### Implementation

```python
def classify_with_examples(message: str) -> str:
    examples = """
Message: "I was charged twice for my subscription"
Category: billing

Message: "The app crashes when I try to upload a photo"
Category: technical

Message: "What are your business hours?"
Category: general

Message: "I need a refund for my last payment"
Category: billing

Message: "How do I reset my password?"
Category: technical
"""
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=50,
        messages=[{
            "role": "user",
            "content": f"""{examples}
Message: "{message}"
Category:"""
        }]
    )
    return response.content[0].text.strip().lower()
```

### Best Practices
- 3-5 examples usually sufficient
- Cover edge cases in examples
- Balance examples across categories
- Use realistic, diverse examples

---

## Pattern 3: RAG (Retrieval-Augmented Generation)

### When to Use
- Need current information beyond training
- Proprietary/domain-specific knowledge
- Want to cite sources
- Reduce hallucination risk

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     INDEXING PIPELINE                        │
├─────────────────────────────────────────────────────────────┤
│  Documents → Chunk → Embed → Store in Vector DB             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                     QUERY PIPELINE                           │
├─────────────────────────────────────────────────────────────┤
│  Query → Embed → Search → Rerank → Generate with Context    │
└─────────────────────────────────────────────────────────────┘
```

### Implementation

```python
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Setup
embed_model = SentenceTransformer('all-MiniLM-L6-v2')
qdrant = QdrantClient(host="localhost", port=6333)

# Indexing
def index_documents(documents: list[dict]):
    for doc in documents:
        chunks = chunk_document(doc["content"])
        for i, chunk in enumerate(chunks):
            embedding = embed_model.encode(chunk)
            qdrant.upsert(
                collection_name="knowledge",
                points=[{
                    "id": f"{doc['id']}_{i}",
                    "vector": embedding.tolist(),
                    "payload": {
                        "content": chunk,
                        "source": doc["source"],
                        "title": doc["title"]
                    }
                }]
            )

# Retrieval
def retrieve(query: str, top_k: int = 5) -> list[dict]:
    query_embedding = embed_model.encode(query)
    results = qdrant.search(
        collection_name="knowledge",
        query_vector=query_embedding.tolist(),
        limit=top_k
    )
    return [hit.payload for hit in results]

# Generation
def rag_query(query: str) -> str:
    # Retrieve relevant context
    contexts = retrieve(query, top_k=5)
    
    # Format context
    context_text = "\n\n".join([
        f"Source: {c['title']}\n{c['content']}" 
        for c in contexts
    ])
    
    # Generate with context
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system="Answer based on the provided context. Cite sources.",
        messages=[{
            "role": "user",
            "content": f"""Context:
{context_text}

Question: {query}

Answer:"""
        }]
    )
    return response.content[0].text
```

### Chunking Strategies

```python
# Fixed size chunking
def chunk_fixed(text: str, chunk_size: int = 500, overlap: int = 50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

# Sentence-based chunking
import nltk
def chunk_sentences(text: str, sentences_per_chunk: int = 5):
    sentences = nltk.sent_tokenize(text)
    chunks = []
    for i in range(0, len(sentences), sentences_per_chunk):
        chunk = " ".join(sentences[i:i + sentences_per_chunk])
        chunks.append(chunk)
    return chunks

# Recursive chunking (respects structure)
def chunk_recursive(text: str, max_size: int = 1000):
    separators = ["\n\n", "\n", ". ", " "]
    
    def split(text, separators):
        if len(text) <= max_size:
            return [text]
        
        sep = separators[0]
        parts = text.split(sep)
        
        chunks = []
        current = ""
        for part in parts:
            if len(current) + len(part) <= max_size:
                current += sep + part if current else part
            else:
                if current:
                    chunks.append(current)
                if len(part) > max_size and len(separators) > 1:
                    chunks.extend(split(part, separators[1:]))
                else:
                    current = part
        if current:
            chunks.append(current)
        return chunks
    
    return split(text, separators)
```

---

## Pattern 4: Tool Use / Function Calling

### When to Use
- Need to take actions (API calls, DB queries)
- Need real-time data
- Multi-step workflows
- Structured data extraction

### Implementation

```python
import json

tools = [
    {
        "name": "search_products",
        "description": "Search the product catalog",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query"
                },
                "category": {
                    "type": "string",
                    "description": "Product category filter"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_order_status",
        "description": "Get the status of an order by ID",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The order ID"
                }
            },
            "required": ["order_id"]
        }
    }
]

def execute_tool(name: str, args: dict) -> str:
    if name == "search_products":
        # Call your product search API
        return json.dumps({"products": [...]})
    elif name == "get_order_status":
        # Call your order API
        return json.dumps({"status": "shipped", "eta": "2025-01-20"})

def chat_with_tools(user_message: str):
    messages = [{"role": "user", "content": user_message}]
    
    while True:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            tools=tools,
            messages=messages
        )
        
        # Check if model wants to use a tool
        if response.stop_reason == "tool_use":
            # Find tool use blocks
            for block in response.content:
                if block.type == "tool_use":
                    # Execute the tool
                    result = execute_tool(block.name, block.input)
                    
                    # Add assistant response and tool result
                    messages.append({"role": "assistant", "content": response.content})
                    messages.append({
                        "role": "user",
                        "content": [{
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result
                        }]
                    })
        else:
            # Model is done, return final response
            return response.content[0].text
```

---

## Pattern 5: Agents

### When to Use
- Complex multi-step tasks
- Need autonomous decision-making
- Dynamic workflows based on results
- Research/analysis tasks

### Simple ReAct Agent

```python
class SimpleAgent:
    def __init__(self, tools: list[dict]):
        self.tools = tools
        self.max_steps = 10
    
    def run(self, goal: str) -> str:
        messages = [{
            "role": "user",
            "content": f"""You are an agent that accomplishes goals step by step.

Goal: {goal}

Think through what you need to do, then take actions using the available tools.
When you have accomplished the goal, respond with DONE: followed by your final answer."""
        }]
        
        for step in range(self.max_steps):
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                tools=self.tools,
                messages=messages
            )
            
            # Check for completion
            for block in response.content:
                if block.type == "text" and "DONE:" in block.text:
                    return block.text.split("DONE:")[1].strip()
            
            # Handle tool use
            if response.stop_reason == "tool_use":
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        result = execute_tool(block.name, block.input)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result
                        })
                
                messages.append({"role": "assistant", "content": response.content})
                messages.append({"role": "user", "content": tool_results})
            else:
                messages.append({"role": "assistant", "content": response.content})
                messages.append({
                    "role": "user", 
                    "content": "Continue working toward the goal."
                })
        
        return "Max steps reached without completion"
```

### Agent Best Practices

1. **Limit autonomy**: Set max steps, require confirmation for actions
2. **Structured thinking**: Use ReAct (Reason, Act, Observe) pattern
3. **Error recovery**: Handle tool failures gracefully
4. **Logging**: Track all decisions and actions
5. **Guardrails**: Restrict which tools can be used

---

## Pattern 6: Structured Output

### When to Use
- Need to parse response programmatically
- Data extraction tasks
- API responses
- Form filling

### Implementation

```python
from pydantic import BaseModel
import json

class ExtractedContact(BaseModel):
    name: str
    email: str | None
    phone: str | None
    company: str | None

def extract_contact(text: str) -> ExtractedContact:
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": f"""Extract contact information from this text.
Return a JSON object with these fields:
- name (required)
- email (optional)
- phone (optional)  
- company (optional)

Text: {text}

JSON:"""
        }]
    )
    
    # Parse JSON from response
    json_str = response.content[0].text.strip()
    if json_str.startswith("```"):
        json_str = json_str.split("```")[1]
        if json_str.startswith("json"):
            json_str = json_str[4:]
    
    data = json.loads(json_str)
    return ExtractedContact(**data)
```

### With Tool Use for Guaranteed Structure

```python
extract_tool = {
    "name": "save_contact",
    "description": "Save extracted contact information",
    "input_schema": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "email": {"type": "string"},
            "phone": {"type": "string"},
            "company": {"type": "string"}
        },
        "required": ["name"]
    }
}

def extract_contact_structured(text: str) -> dict:
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        tools=[extract_tool],
        tool_choice={"type": "tool", "name": "save_contact"},
        messages=[{
            "role": "user",
            "content": f"Extract contact info from: {text}"
        }]
    )
    
    for block in response.content:
        if block.type == "tool_use":
            return block.input
```

---

## Pattern Comparison

| Pattern | Latency | Cost | Complexity | Reliability |
|---------|---------|------|------------|-------------|
| Zero-shot | Low | Low | Low | Medium |
| Few-shot | Low | Low-Med | Low | High |
| RAG | Medium | Medium | Medium | High |
| Tool Use | Medium | Medium | Medium | High |
| Agents | High | High | High | Medium |
| Structured | Low | Low | Low | High |

## Combining Patterns

Real applications often combine patterns:

```
User Query
    │
    ▼
┌─────────────┐
│ Intent      │ ← Zero-shot classification
│ Classification│
└─────────────┘
    │
    ├─── "product_search" ──► Tool Use (search API)
    │
    ├─── "order_status" ──► Tool Use (order API)
    │
    └─── "general_question" ──► RAG (knowledge base)
                                    │
                                    ▼
                              Structured Output
                              (JSON response)
```
