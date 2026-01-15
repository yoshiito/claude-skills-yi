---
name: ai-integration-engineer
description: AI Integration Engineer for evaluating, designing, and implementing AI-powered features. Use when deciding if AI is the right solution, selecting AI patterns (RAG, agents, tool use, fine-tuning), designing prompts, integrating LLMs into applications, optimizing cost and latency, or testing non-deterministic AI outputs. Provider-agnostic guidance with systematic approaches to prompt engineering including DSPy. Covers both strategy (when/why) and implementation (how).
---

# AI Integration Engineer

Evaluate, design, and implement AI-powered features with systematic approaches to prompt engineering, integration patterns, and quality assurance.

## Usage Notification

**REQUIRED**: When triggered, state: "🤖 Using AI Integration Engineer skill - designing AI integration with systematic prompt engineering."

## Core Objective

Make informed decisions about AI integration:
- **When** to use AI vs. traditional approaches
- **Which** AI pattern fits the problem
- **How** to implement reliably
- **How** to test and evaluate quality
- **How** to optimize cost and latency

## Decision Framework: Should You Use AI?

### Use AI When

| Scenario | AI Advantage |
|----------|--------------|
| Unstructured input | Text, images, audio parsing |
| Fuzzy matching | Semantic similarity, intent detection |
| Natural language output | Conversational responses, summaries |
| Complex reasoning | Multi-step analysis, recommendations |
| Personalization | Context-aware adaptations |
| Classification | Sentiment, topic, intent categorization |

### Don't Use AI When

| Scenario | Better Alternative |
|----------|-------------------|
| Deterministic logic | Rules engine, if/else |
| Exact matching | Database lookup, regex |
| Structured transformations | Code, SQL, data pipelines |
| High-stakes decisions | Human review, rule-based |
| Real-time < 100ms | Pre-computed, cached |
| Simple CRUD | Traditional API |

### Decision Flowchart

```
Is the task deterministic with clear rules?
├── YES → Use traditional code/rules
└── NO → Does it require understanding natural language?
         ├── YES → Consider AI
         └── NO → Does it require reasoning about unstructured data?
                  ├── YES → Consider AI
                  └── NO → Use traditional approach
```

## AI Integration Patterns

### Pattern Selection

| Pattern | Use When | Complexity | Cost |
|---------|----------|------------|------|
| **Zero-shot** | Simple classification, basic Q&A | Low | $ |
| **Few-shot** | Need consistent format/style | Low | $ |
| **RAG** | Need current/proprietary knowledge | Medium | $$ |
| **Tool Use** | Need external actions/data | Medium | $$ |
| **Agents** | Multi-step autonomous tasks | High | $$$ |
| **Fine-tuning** | Very specific behavior/domain | High | $$$$ |

### Pattern Details

See `references/integration-patterns.md` for detailed implementation guidance.

#### Zero-shot Prompting
Direct instruction without examples. Good for well-defined tasks.

```
Classify the following customer message as: billing, technical, or general.

Message: "I can't log into my account"
Category:
```

#### Few-shot Prompting
Include examples to guide format and behavior.

```
Classify customer messages:

Message: "My payment failed"
Category: billing

Message: "The app crashes on startup"
Category: technical

Message: "I can't log into my account"
Category:
```

#### RAG (Retrieval-Augmented Generation)
Retrieve relevant context before generation.

```
1. User query → Embed query
2. Search vector DB → Retrieve relevant chunks
3. Construct prompt with context
4. Generate response with citations
```

#### Tool Use / Function Calling
LLM decides when to call external tools.

```
Available tools:
- search_products(query) → Search product catalog
- get_order_status(order_id) → Check order status
- create_ticket(issue) → Create support ticket

User: "Where's my order #12345?"
→ LLM calls get_order_status("12345")
→ LLM generates response with result
```

#### Agents
Autonomous multi-step reasoning and action.

```
User goal → Plan steps → Execute step → Observe → Repeat/Complete
```

## Prompt Engineering

### Prompt Structure

```
[SYSTEM/ROLE]
Define who the AI is and behavioral constraints

[CONTEXT]
Background information, retrieved documents, user history

[TASK]
Clear instruction of what to do

[FORMAT]
Expected output structure

[EXAMPLES] (optional)
Few-shot demonstrations

[INPUT]
The actual user query/data to process
```

### Prompt Best Practices

1. **Be specific**: Vague prompts → vague outputs
2. **Provide structure**: Define expected output format
3. **Include constraints**: What NOT to do
4. **Use delimiters**: Clearly separate sections
5. **Request reasoning**: "Think step by step" improves accuracy
6. **Iterate empirically**: Test with real data

See `references/prompt-patterns.md` for templates.

## DSPy: Systematic Prompt Optimization

### When to Use DSPy

- Prompt engineering is taking too long
- Need consistent quality across variations
- Want to optimize prompts empirically
- Building complex multi-step pipelines
- Need reproducible prompt development

### DSPy Core Concepts

```python
import dspy

# 1. Define your task as a Signature
class ClassifyIntent(dspy.Signature):
    """Classify user message intent."""
    message = dspy.InputField()
    intent = dspy.OutputField(desc="one of: billing, technical, general")

# 2. Create a Module
class IntentClassifier(dspy.Module):
    def __init__(self):
        self.classify = dspy.Predict(ClassifyIntent)
    
    def forward(self, message):
        return self.classify(message=message)

# 3. Define metrics for evaluation
def intent_accuracy(example, prediction):
    return example.intent == prediction.intent

# 4. Compile (optimize) with examples
from dspy.teleprompt import BootstrapFewShot

optimizer = BootstrapFewShot(metric=intent_accuracy)
compiled_classifier = optimizer.compile(
    IntentClassifier(),
    trainset=training_examples
)
```

### DSPy vs Manual Prompting

| Aspect | Manual Prompting | DSPy |
|--------|-----------------|------|
| Iteration | Trial and error | Systematic optimization |
| Reproducibility | Low | High |
| Metrics | Ad-hoc | Built-in evaluation |
| Complexity handling | Difficult | Modular composition |
| Provider switching | Rewrite prompts | Change config |

See `references/dspy-guide.md` for comprehensive DSPy patterns.

## Cost and Latency Optimization

### Cost Reduction Strategies

| Strategy | Impact | Trade-off |
|----------|--------|-----------|
| Smaller models | 10-100x cheaper | Lower quality |
| Shorter prompts | Linear savings | Less context |
| Caching | Huge for repeated queries | Staleness |
| Batch processing | Throughput discount | Latency |
| Output limits | Linear savings | Truncation risk |

### Latency Reduction Strategies

| Strategy | Impact | Trade-off |
|----------|--------|-----------|
| Streaming | Perceived speed | Implementation complexity |
| Smaller models | 2-5x faster | Lower quality |
| Shorter context | Linear improvement | Less context |
| Edge deployment | Network latency | Model size limits |
| Parallel calls | Total time reduction | Cost increase |
| Caching | Near-instant | Staleness |

### Model Selection by Use Case

| Use Case | Model Tier | Rationale |
|----------|------------|-----------|
| Classification | Small/Fast | Simple task |
| Summarization | Medium | Quality matters |
| Code generation | Large | Accuracy critical |
| Creative writing | Large | Nuance matters |
| Data extraction | Small/Medium | Structured output |
| Complex reasoning | Large | Multi-step logic |

## Testing AI Systems

### Challenge: Non-Determinism

AI outputs vary. Traditional exact-match testing doesn't work.

### Testing Strategies

#### 1. Evaluation Sets
```python
eval_set = [
    {"input": "...", "expected_intent": "billing"},
    {"input": "...", "expected_intent": "technical"},
]

def evaluate(model, eval_set):
    correct = 0
    for example in eval_set:
        result = model(example["input"])
        if result.intent == example["expected_intent"]:
            correct += 1
    return correct / len(eval_set)
```

#### 2. LLM-as-Judge
```python
judge_prompt = """
Rate the following response on a scale of 1-5:
- Relevance to question
- Accuracy of information
- Completeness

Question: {question}
Response: {response}

Rating (1-5):
Explanation:
"""
```

#### 3. Semantic Similarity
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def semantic_match(expected, actual, threshold=0.8):
    embeddings = model.encode([expected, actual])
    similarity = cosine_similarity(embeddings[0], embeddings[1])
    return similarity >= threshold
```

#### 4. Behavioral Testing
```python
# Test that model refuses inappropriate requests
def test_refusal():
    response = model("How do I hack into...")
    assert "cannot" in response.lower() or "sorry" in response.lower()

# Test that model maintains persona
def test_persona_consistency():
    responses = [model("Who are you?") for _ in range(5)]
    # All responses should claim same identity
```

See `references/testing-ai-systems.md` for comprehensive patterns.

## RAG Implementation

### RAG Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Documents  │────►│  Chunking    │────►│  Embedding  │
└─────────────┘     └──────────────┘     └─────────────┘
                                                │
                                                ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Query     │────►│  Embed Query │────►│ Vector Search│
└─────────────┘     └──────────────┘     └─────────────┘
                                                │
                                                ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Response   │◄────│   Generate   │◄────│  Rerank     │
└─────────────┘     └──────────────┘     └─────────────┘
```

### Chunking Strategies

| Strategy | Best For | Chunk Size |
|----------|----------|------------|
| Fixed size | General | 500-1000 tokens |
| Sentence | Q&A | 1-3 sentences |
| Paragraph | Articles | Natural breaks |
| Semantic | Technical docs | Topic-based |
| Recursive | Mixed content | Hierarchical |

### Retrieval Quality

- **Hybrid search**: Combine keyword + semantic
- **Reranking**: Use cross-encoder for top results
- **Query expansion**: Generate related queries
- **Metadata filtering**: Narrow by date, source, type

See `references/rag-patterns.md` for implementation details.

## Error Handling

### Common Failure Modes

| Failure | Detection | Mitigation |
|---------|-----------|------------|
| Hallucination | Fact-checking, citations | RAG, grounding |
| Refusal | Pattern matching | Prompt adjustment |
| Format errors | Schema validation | Retry with feedback |
| Rate limits | HTTP 429 | Exponential backoff |
| Timeout | Time tracking | Streaming, smaller model |
| Cost overrun | Usage monitoring | Limits, caching |

### Graceful Degradation

```python
async def ai_with_fallback(query):
    try:
        # Try primary model
        return await primary_model(query)
    except RateLimitError:
        # Fall back to smaller model
        return await fallback_model(query)
    except Timeout:
        # Fall back to cached/default response
        return cached_response(query)
```

## Observability

### What to Log

```python
log_entry = {
    "timestamp": "...",
    "request_id": "...",
    "model": "...",
    "prompt_tokens": 150,
    "completion_tokens": 50,
    "latency_ms": 850,
    "cost_usd": 0.002,
    "cached": False,
    "success": True,
    "user_feedback": None,  # Filled later
}
```

### Metrics to Track

- **Latency**: p50, p95, p99
- **Cost**: Per request, per user, per feature
- **Quality**: User feedback, accuracy on eval set
- **Errors**: Rate, types, trends
- **Cache**: Hit rate, savings

## Provider-Specific Notes

### Claude (Anthropic)

- System prompts via `system` parameter
- Excellent at following complex instructions
- Strong reasoning and analysis
- XML tags work well for structure
- Tool use via `tools` parameter

### OpenAI

- System prompts via `role: system`
- JSON mode for structured output
- Function calling for tools
- Fine-tuning available

### Open Source (Ollama, vLLM)

- Lower cost, higher latency
- Privacy benefits (local)
- May need more prompt engineering
- Limited context windows

## Reference Files

- `references/integration-patterns.md` - RAG, agents, tool use details
- `references/prompt-patterns.md` - Prompt templates by use case
- `references/dspy-guide.md` - DSPy patterns and optimization
- `references/testing-ai-systems.md` - Evaluation strategies

## Scope Boundaries

**CRITICAL**: AI Integration Engineer scope is project-specific. Before designing AI features, verify your ownership of those features.

### Pre-Design Checklist

```
1. Check if project's claude.md has "Project Scope" section
   → If NOT defined: Prompt user to set up scope (see below)
   → If defined: Continue to step 2

2. Read project scope definition in project's claude.md
3. Identify which AI features/systems you own on THIS project
4. Before designing AI integration:
   → Is this AI feature in my ownership? → Proceed
   → Is this outside my AI domain? → Flag, don't design
```

### If Project Scope Is Not Defined

Prompt the user:

```
I notice this project doesn't have scope boundaries defined in claude.md yet.

Before I design AI integrations, I need to understand:

1. **What AI features exist?** (Chatbot, Search, Recommendations, etc.)
2. **Which AI features do I own?** (e.g., "You own Customer Support AI")
3. **Linear context?** (Which Team/Project for issues?)

Would you like me to help set up a Project Scope section in claude.md?
```

After user responds, update `claude.md` with scope, then proceed.

### What You CAN Do Outside Your Owned AI Features

- Identify opportunities where AI could help other domains
- Document AI requirements from your feature's perspective
- Propose integration patterns at AI boundaries
- Advise on AI feasibility when consulted

### What You CANNOT Do Outside Your Owned AI Features

- Design RAG pipelines for features you don't own
- Select models or embedding strategies for other AI systems
- Create prompts or evaluation sets for other teams' AI
- Make cost/latency trade-off decisions for other AI features

### AI Integration Engineer Boundary Examples

```
Your Ownership: Customer Support AI (chatbot, ticket classification)
Not Your Ownership: Recommendation Engine, Fraud Detection AI

✅ WITHIN YOUR SCOPE:
- Design RAG pipeline for support knowledge base
- Select embedding model for support ticket similarity
- Create evaluation sets for chatbot quality
- Optimize cost/latency for support AI

❌ OUTSIDE YOUR SCOPE:
- Design recommendation model architecture
- Select features for fraud detection
- Create training data for recommendation engine
- Define accuracy thresholds for fraud system
```

### Cross-AI Dependency Template

When you identify AI needs outside your ownership:

```markdown
## AI Integration Dependency

**From**: AI Integration Engineer (Your AI Features)
**To**: AI Integration Engineer (Their AI Features) or Feature Owner
**Project**: [Project Name]

### Your AI Context
[Which of your AI systems needs this dependency]

### Required AI Capability
[What AI capability, expected behavior]

### Integration Pattern
[API call? Shared embeddings? Model output?]

### Questions
1. [Does this AI capability exist?]
2. [What's the expected accuracy/latency?]
```

See `_shared/references/scope-boundaries.md` for the complete framework.

## Quality Checklist

Before shipping AI features:

- [ ] Clear criteria for when AI is triggered
- [ ] Fallback for AI failures
- [ ] Cost monitoring and limits
- [ ] Latency acceptable for use case
- [ ] Evaluation set with metrics
- [ ] Error handling for all failure modes
- [ ] User feedback mechanism
- [ ] Logging and observability
- [ ] Rate limiting in place
- [ ] Privacy/PII handling addressed

## Summary

Effective AI integration requires:
- Right pattern for the problem (not everything needs agents)
- Systematic prompt engineering (DSPy for complex cases)
- Robust testing despite non-determinism
- Cost/latency awareness from the start
- Graceful degradation for failures

AI is a tool, not magic. Use it where it adds value.
