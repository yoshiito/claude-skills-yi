# DSPy Guide

Systematic prompt optimization with DSPy.

## What is DSPy?

DSPy treats prompt engineering as an optimization problem rather than manual crafting. Instead of writing prompts, you:
1. Define **what** you want (Signatures)
2. Define **how** to compose it (Modules)
3. Define **success criteria** (Metrics)
4. Let DSPy **optimize** the prompts

## Installation

```bash
pip install dspy-ai
```

## Core Concepts

### 1. Signatures

Signatures define input/output behavior declaratively.

```python
import dspy

# Simple signature using docstring
class Summarize(dspy.Signature):
    """Summarize the given text concisely."""
    text = dspy.InputField()
    summary = dspy.OutputField()

# Signature with field descriptions
class ClassifyEmail(dspy.Signature):
    """Classify an email into a category."""
    email = dspy.InputField(desc="The email content to classify")
    category = dspy.OutputField(desc="One of: spam, important, newsletter, personal")

# Signature with multiple outputs
class AnalyzeSentiment(dspy.Signature):
    """Analyze the sentiment and key themes of text."""
    text = dspy.InputField()
    sentiment = dspy.OutputField(desc="positive, negative, or neutral")
    confidence = dspy.OutputField(desc="confidence score 0-1")
    themes = dspy.OutputField(desc="comma-separated key themes")
```

### 2. Modules

Modules define how to use signatures.

```python
# Basic prediction module
class SimpleSummarizer(dspy.Module):
    def __init__(self):
        self.summarize = dspy.Predict(Summarize)
    
    def forward(self, text):
        return self.summarize(text=text)

# Chain of Thought for reasoning
class ReasoningClassifier(dspy.Module):
    def __init__(self):
        self.classify = dspy.ChainOfThought(ClassifyEmail)
    
    def forward(self, email):
        return self.classify(email=email)

# Multi-step pipeline
class ContentAnalyzer(dspy.Module):
    def __init__(self):
        self.summarize = dspy.Predict(Summarize)
        self.analyze = dspy.ChainOfThought(AnalyzeSentiment)
    
    def forward(self, text):
        summary = self.summarize(text=text)
        analysis = self.analyze(text=summary.summary)
        return dspy.Prediction(
            summary=summary.summary,
            sentiment=analysis.sentiment,
            themes=analysis.themes
        )
```

### 3. Metrics

Metrics define success criteria for optimization.

```python
# Exact match metric
def exact_match(example, prediction, trace=None):
    return example.category == prediction.category

# Fuzzy match metric
def fuzzy_match(example, prediction, trace=None):
    return example.category.lower() in prediction.category.lower()

# Composite metric
def quality_metric(example, prediction, trace=None):
    # Check correctness
    correct = example.expected == prediction.output
    
    # Check length constraint
    within_length = len(prediction.output) < 500
    
    # Score 0-1
    return (correct * 0.8) + (within_length * 0.2)

# LLM-based metric
def llm_judge(example, prediction, trace=None):
    judge = dspy.Predict("text, response -> score: float")
    result = judge(
        text=example.text,
        response=prediction.summary
    )
    return float(result.score) > 0.7
```

### 4. Optimizers (Teleprompters)

Optimizers improve prompts automatically.

```python
from dspy.teleprompt import (
    BootstrapFewShot,
    BootstrapFewShotWithRandomSearch,
    MIPRO
)

# Basic few-shot optimization
optimizer = BootstrapFewShot(
    metric=exact_match,
    max_bootstrapped_demos=4,
    max_labeled_demos=4
)

# With random search for better results
optimizer = BootstrapFewShotWithRandomSearch(
    metric=exact_match,
    max_bootstrapped_demos=4,
    num_candidate_programs=10
)

# Advanced instruction optimization
optimizer = MIPRO(
    metric=exact_match,
    num_candidates=10,
    init_temperature=1.0
)

# Compile (optimize) the module
compiled_module = optimizer.compile(
    MyModule(),
    trainset=training_examples
)
```

---

## Complete Example: Email Classifier

```python
import dspy
from dspy.teleprompt import BootstrapFewShot

# 1. Configure the LLM
lm = dspy.LM('anthropic/claude-sonnet-4-20250514')
dspy.configure(lm=lm)

# 2. Define the signature
class ClassifyEmail(dspy.Signature):
    """Classify an email into a category based on its content."""
    email = dspy.InputField(desc="The email content")
    category = dspy.OutputField(desc="One of: spam, important, newsletter, personal")

# 3. Define the module
class EmailClassifier(dspy.Module):
    def __init__(self):
        self.classify = dspy.ChainOfThought(ClassifyEmail)
    
    def forward(self, email):
        return self.classify(email=email)

# 4. Create training examples
trainset = [
    dspy.Example(
        email="URGENT: Your account has been compromised! Click here now!",
        category="spam"
    ).with_inputs("email"),
    dspy.Example(
        email="Meeting tomorrow at 3pm to discuss Q4 results",
        category="important"
    ).with_inputs("email"),
    dspy.Example(
        email="Your weekly digest from TechNews",
        category="newsletter"
    ).with_inputs("email"),
    dspy.Example(
        email="Hey! Want to grab lunch this weekend?",
        category="personal"
    ).with_inputs("email"),
    # Add more examples...
]

# 5. Define the metric
def accuracy(example, prediction, trace=None):
    return example.category.lower() == prediction.category.lower()

# 6. Optimize
optimizer = BootstrapFewShot(metric=accuracy)
compiled_classifier = optimizer.compile(
    EmailClassifier(),
    trainset=trainset
)

# 7. Use the optimized classifier
result = compiled_classifier("Your order #12345 has shipped!")
print(f"Category: {result.category}")

# 8. Evaluate on test set
from dspy.evaluate import Evaluate

testset = [...]  # Test examples
evaluator = Evaluate(devset=testset, metric=accuracy)
score = evaluator(compiled_classifier)
print(f"Accuracy: {score}%")
```

---

## Advanced Patterns

### Multi-Step Reasoning

```python
class ResearchAgent(dspy.Module):
    def __init__(self):
        self.generate_queries = dspy.ChainOfThought(
            "topic -> search_queries: list[str]"
        )
        self.synthesize = dspy.ChainOfThought(
            "topic, search_results -> report: str"
        )
    
    def forward(self, topic):
        # Generate search queries
        queries = self.generate_queries(topic=topic)
        
        # Execute searches (external)
        results = [search(q) for q in queries.search_queries]
        
        # Synthesize report
        report = self.synthesize(
            topic=topic,
            search_results="\n".join(results)
        )
        return report
```

### Self-Refinement

```python
class RefinedWriter(dspy.Module):
    def __init__(self):
        self.draft = dspy.Predict("topic -> draft: str")
        self.critique = dspy.ChainOfThought("draft -> critique: str")
        self.refine = dspy.Predict("draft, critique -> final: str")
    
    def forward(self, topic):
        draft = self.draft(topic=topic)
        critique = self.critique(draft=draft.draft)
        final = self.refine(
            draft=draft.draft,
            critique=critique.critique
        )
        return final
```

### Branching Logic

```python
class AdaptiveResponder(dspy.Module):
    def __init__(self):
        self.classify = dspy.Predict("query -> query_type: str")
        self.simple_answer = dspy.Predict("query -> answer: str")
        self.detailed_answer = dspy.ChainOfThought("query -> answer: str")
    
    def forward(self, query):
        query_type = self.classify(query=query).query_type
        
        if "simple" in query_type.lower():
            return self.simple_answer(query=query)
        else:
            return self.detailed_answer(query=query)
```

### Assertions and Constraints

```python
import dspy
from dspy.primitives.assertions import assert_transform_module, backtrack_handler

class ConstrainedGenerator(dspy.Module):
    def __init__(self):
        self.generate = dspy.ChainOfThought("topic -> response: str")
    
    def forward(self, topic):
        response = self.generate(topic=topic)
        
        # Add assertions
        dspy.Assert(
            len(response.response) < 500,
            "Response must be under 500 characters"
        )
        dspy.Assert(
            topic.lower() in response.response.lower(),
            "Response must mention the topic"
        )
        
        return response

# Wrap with assertion handling
constrained = assert_transform_module(
    ConstrainedGenerator(),
    backtrack_handler
)
```

---

## Saving and Loading

```python
# Save compiled module
compiled_module.save("classifier_v1.json")

# Load compiled module
loaded = EmailClassifier()
loaded.load("classifier_v1.json")

# Export optimized prompts for inspection
print(compiled_module.summarize.extended_signature)
```

---

## DSPy vs Manual Prompting

| Scenario | Use Manual Prompting | Use DSPy |
|----------|---------------------|----------|
| Quick prototype | ✅ | |
| Simple, one-off task | ✅ | |
| Complex multi-step | | ✅ |
| Need consistent quality | | ✅ |
| Changing requirements | | ✅ |
| Team collaboration | | ✅ |
| A/B testing prompts | | ✅ |
| Production system | | ✅ |

---

## Best Practices

1. **Start with examples**: Good training data matters more than clever optimization
2. **Define clear metrics**: Fuzzy metrics lead to fuzzy results
3. **Use ChainOfThought**: When reasoning helps, use it
4. **Iterate on signatures**: Field descriptions guide the model
5. **Test on holdout set**: Don't overfit to training examples
6. **Version your modules**: Track what changed and why
7. **Monitor in production**: Metrics can drift over time

---

## Debugging

```python
# Inspect what DSPy is doing
dspy.configure(lm=lm, trace=[])

# Run with tracing
result = module(input)

# Print the trace
for step in dspy.settings.trace:
    print(step)

# Inspect module internals
print(module.summarize.demos)  # Few-shot examples
print(module.summarize.extended_signature)  # Full prompt
```
