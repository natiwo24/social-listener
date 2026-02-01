# Analysis Design Document

**Version:** 1.0  
**Date:** 2026-01-31  
**Parent Document:** [TECHNICAL_DESIGN.md](./TECHNICAL_DESIGN.md)  
**Status:** Draft

---

## Table of Contents

1. [Overview](#1-overview)
2. [Data Collection Prerequisites](#2-data-collection-prerequisites)
   - 2.1 [Current Collector Output](#21-current-collector-output)
   - 2.2 [Missing Fields to Add](#22-missing-fields-to-add)
   - 2.3 [Sample Data Requirements](#23-sample-data-requirements)
3. [Processing Strategy](#3-processing-strategy)
   - 3.1 [Individual vs Batch Processing](#31-individual-vs-batch-processing)
   - 3.2 [Recommended Approach](#32-recommended-approach)
   - 3.3 [Token Budget Analysis](#33-token-budget-analysis)
4. [Prompt Design](#4-prompt-design)
   - 4.1 [Design Principles](#41-design-principles)
   - 4.2 [Unified Analysis Prompt](#42-unified-analysis-prompt)
   - 4.3 [Structured Output Schema](#43-structured-output-schema)
   - 4.4 [Edge Cases](#44-edge-cases)
5. [Digest Synthesis](#5-digest-synthesis)
   - 5.1 [Aggregation Strategy](#51-aggregation-strategy)
   - 5.2 [Synthesis Prompt](#52-synthesis-prompt)
   - 5.3 [Ranking Algorithm](#53-ranking-algorithm)
6. [Error Handling](#6-error-handling)
   - 6.1 [API Failures](#61-api-failures)
   - 6.2 [Malformed Responses](#62-malformed-responses)
   - 6.3 [Partial Pipeline Failures](#63-partial-pipeline-failures)
7. [Cost Optimization](#7-cost-optimization)
8. [Validation & Tuning](#8-validation--tuning)
9. [Implementation Checklist](#9-implementation-checklist)

---

## 1. Overview

This document details the NLP analysis strategy for Social Listener, covering:
- How we process Reddit posts through Claude
- Prompt design and structured outputs
- How individual analyses are synthesized into a daily digest
- Error handling and cost optimization

**Key Design Goals:**
1. Minimize API costs (combine calls where possible)
2. Ensure consistent, parseable output (structured JSON)
3. Support the email digest format defined in TECHNICAL_DESIGN.md Appendix B
4. Enable quality measurement per success metrics in section 3

---

## 2. Data Collection Prerequisites

### 2.1 Current Collector Output

The `RedditCollector._parse_post()` currently returns:

```python
{
    "id": "reddit_abc123",
    "platform": "reddit",
    "source": "python",           # subreddit name
    "title": "Post title here",
    "content": "Self-text content...",  # Empty for link posts
    "author": "username",
    "url": "https://...",         # External URL or Reddit permalink
    "score": 142,                 # Upvotes minus downvotes
    "created_at": "2026-01-31T10:00:00"
}
```

### 2.2 Missing Fields to Add

Per PRAW documentation, we should capture these additional fields:

| Field | PRAW Attribute | Purpose | Priority |
|-------|----------------|---------|----------|
| `num_comments` | `submission.num_comments` | Display in digest, significance threshold | **Required** |
| `upvote_ratio` | `submission.upvote_ratio` | Controversy detection (low ratio = divisive) | Nice-to-have |
| `permalink` | `submission.permalink` | Reliable Reddit link (vs external `url`) | **Required** |
| `is_self` | `submission.is_self` | Know if content is text vs link post | Nice-to-have |
| `link_flair_text` | `submission.link_flair_text` | Category context (e.g., "Question", "Discussion") | Nice-to-have |

**Action Required:** Update `RedditCollector._parse_post()` before analysis design is implemented.

Proposed updated parser:

```python
def _parse_post(self, submission, subreddit: str) -> Dict:
    """Parse a PRAW submission object into a dictionary."""
    return {
        "id": f"reddit_{submission.id}",
        "platform": "reddit",
        "source": subreddit,
        "title": submission.title,
        "content": submission.selftext,
        "author": submission.author.name if submission.author else "[deleted]",
        "url": submission.url,
        "permalink": f"https://reddit.com{submission.permalink}",  # NEW
        "score": submission.score,
        "num_comments": submission.num_comments,                    # NEW
        "upvote_ratio": submission.upvote_ratio,                    # NEW
        "is_self": submission.is_self,                              # NEW
        "flair": submission.link_flair_text,                        # NEW
        "created_at": datetime.fromtimestamp(submission.created_utc).isoformat(),
    }
```

### 2.3 Sample Data Requirements

Before finalizing prompt design, we should collect sample data to validate:

| Validation Need | Sample Size | Purpose |
|-----------------|-------------|---------|
| Token count per post | 50 posts | Validate token budget assumptions |
| Content length variance | 50 posts | Understand truncation needs |
| Empty content ratio | 50 posts | How many link-only posts? |
| Topic diversity | 50 posts | Test topic extraction coverage |

**Recommendation:** Run a single collection pass and save raw output before implementing analysis. This can be done with current code.

---

## 3. Processing Strategy

### 3.1 Individual vs Batch Processing

| Approach | Pros | Cons |
|----------|------|------|
| **Individual** (1 post → 1 API call) | Simple error isolation, easy retry | More API calls, higher latency |
| **Batch per subreddit** (20 posts → 1 call) | Fewer calls, context sharing | Large prompts, complex parsing, all-or-nothing failure |
| **Micro-batch** (5 posts → 1 call) | Balance of efficiency and reliability | Moderate complexity |

### 3.2 Recommended Approach

**Hybrid Strategy:**

1. **Individual analysis** for each post (but unified prompt - 1 call instead of 3)
2. **Batch synthesis** for digest generation (all analyses → 1 summary call)

```
┌─────────────────────────────────────────────────────────────────┐
│                     ANALYSIS PIPELINE                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Collection (100 posts)                                         │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  PHASE 1: Individual Analysis (100 API calls)           │   │
│  │                                                          │   │
│  │  Post 1 ──▶ Claude ──▶ {sentiment, topics, summary}     │   │
│  │  Post 2 ──▶ Claude ──▶ {sentiment, topics, summary}     │   │
│  │  ...                                                     │   │
│  │  Post N ──▶ Claude ──▶ {sentiment, topics, summary}     │   │
│  └─────────────────────────────────────────────────────────┘   │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  PHASE 2: Digest Synthesis (1 API call)                 │   │
│  │                                                          │   │
│  │  All analyses ──▶ Claude ──▶ {                          │   │
│  │                                  overall_sentiment,      │   │
│  │                                  top_topics,             │   │
│  │                                  notable_posts,          │   │
│  │                                  microsoft_mentions      │   │
│  │                               }                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│       │                                                         │
│       ▼                                                         │
│  Email Generation                                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Rationale:**
- Individual analysis allows granular retry on failure
- Each post gets dedicated attention (no context bleed)
- Synthesis step adds "editorial" intelligence to aggregate
- Reduces API calls from 300 (current: 3 per post) to 101 (1 per post + 1 synthesis)

### 3.3 Token Budget Analysis

**Input tokens per post (estimated):**

| Component | Tokens | Notes |
|-----------|--------|-------|
| System prompt | ~200 | Fixed overhead |
| Post title | ~20-50 | Avg 10-25 words |
| Post content | ~100-500 | Highly variable; link posts = 0 |
| Few-shot examples | ~150 | 1-2 examples in prompt |
| **Total input** | **~470-900** | |

**Output tokens per post:**

| Component | Tokens | Notes |
|-----------|--------|-------|
| Sentiment + confidence | ~15 | `{"sentiment": "positive", "confidence": 0.85}` |
| Topics (3-5) | ~30 | `["python", "async", "web development"]` |
| Technologies (2-4) | ~20 | `["FastAPI", "PostgreSQL"]` |
| Summary | ~50-80 | 1-2 sentences |
| **Total output** | **~115-145** | |

**Monthly cost validation (100 posts/day):**

| Model | Input Cost | Output Cost | Daily | Monthly |
|-------|------------|-------------|-------|---------|
| Claude Sonnet 4.5 | $3/M tokens | $15/M tokens | $0.006 | **$0.18** |
| GPT-5.2 | $1.75/M tokens | $14/M tokens | $0.005 | **$0.15** |

*Synthesis call adds ~$0.01/day. Total remains well under $1/month.*

---

## 4. Prompt Design

### 4.1 Design Principles

1. **Single unified prompt** - Combine sentiment, topics, and summary into one call
2. **Structured JSON output** - Use JSON schema for reliable parsing
3. **Few-shot examples** - Include 1-2 examples for consistency
4. **Explicit constraints** - Character limits, allowed values, required fields
5. **Context awareness** - Mention this is developer/tech community content

### 4.2 Unified Analysis Prompt

```
SYSTEM:
You are an analyst reviewing posts from developer communities on Reddit. 
Your job is to extract structured insights for a daily digest.

Analyze the post and return a JSON object with exactly this structure:
{
  "sentiment": "positive" | "neutral" | "negative",
  "sentiment_confidence": 0.0-1.0,
  "topics": ["topic1", "topic2", ...],  // 2-5 general topics
  "technologies": ["tech1", "tech2", ...],  // 0-5 specific technologies mentioned
  "summary": "1-2 sentence summary",
  "microsoft_relevant": true | false,  // mentions Microsoft, Azure, VS Code, GitHub, Copilot, .NET, TypeScript, etc.
  "controversy_flag": true | false  // heated debate, strong disagreement, complaints
}

Guidelines:
- sentiment: Overall emotional tone. "positive" = enthusiasm, success, praise. "negative" = frustration, complaints, problems. "neutral" = informational, questions, balanced.
- topics: High-level themes like "career advice", "debugging", "architecture", "learning", "tooling"
- technologies: Specific tools, languages, frameworks: "Python", "React", "AWS", "Docker"
- summary: Capture the main point in ≤150 characters. Write for a busy executive.
- microsoft_relevant: True if post discusses any Microsoft ecosystem product
- controversy_flag: True if post contains complaints, heated debate, or negative experiences

USER:
Subreddit: r/{subreddit}
Title: {title}
Content: {content}

---
Respond with only the JSON object, no markdown formatting.
```

### 4.3 Structured Output Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["sentiment", "sentiment_confidence", "topics", "technologies", "summary", "microsoft_relevant", "controversy_flag"],
  "properties": {
    "sentiment": {
      "type": "string",
      "enum": ["positive", "neutral", "negative"]
    },
    "sentiment_confidence": {
      "type": "number",
      "minimum": 0,
      "maximum": 1
    },
    "topics": {
      "type": "array",
      "items": {"type": "string"},
      "minItems": 1,
      "maxItems": 5
    },
    "technologies": {
      "type": "array",
      "items": {"type": "string"},
      "maxItems": 5
    },
    "summary": {
      "type": "string",
      "maxLength": 200
    },
    "microsoft_relevant": {
      "type": "boolean"
    },
    "controversy_flag": {
      "type": "boolean"
    }
  }
}
```

**Implementation note:** Use `json.loads()` with a validation wrapper. Consider `pydantic` for schema enforcement.

### 4.4 Edge Cases

| Scenario | Handling |
|----------|----------|
| **Empty content** (link post) | Analyze title only; add note: "Link post - title only" |
| **Very long content** (>2000 chars) | Truncate to first 2000 chars with "..." indicator |
| **Non-English content** | Detect and skip, or translate (future enhancement) |
| **Deleted/removed post** | Skip analysis, log warning |
| **Image/video only** | Analyze title only; note media type |
| **JSON parse failure** | Retry once with explicit "Return valid JSON only" append |

**Truncation strategy:**

```python
def prepare_content_for_analysis(post: dict) -> str:
    """Prepare post content for analysis, handling edge cases."""
    title = post.get("title", "").strip()
    content = post.get("content", "").strip()
    
    # Handle empty content (link posts)
    if not content:
        content = "[Link post - no text content]"
    
    # Truncate long content
    MAX_CONTENT_LENGTH = 2000
    if len(content) > MAX_CONTENT_LENGTH:
        content = content[:MAX_CONTENT_LENGTH] + "... [truncated]"
    
    return f"Title: {title}\n\nContent: {content}"
```

---

## 5. Digest Synthesis

### 5.1 Aggregation Strategy

After individual post analysis, we need to synthesize a digest. This can be done:

| Approach | Pros | Cons |
|----------|------|------|
| **Code-only aggregation** | Deterministic, no API cost | Can't generate narrative insights |
| **LLM synthesis** | Natural language summary, pattern detection | Additional API call, potential hallucination |
| **Hybrid** | Best of both | Slightly more complex |

**Recommended: Hybrid approach**

1. **Code-based aggregation:**
   - Count sentiment distribution (X% positive, Y% negative)
   - Aggregate topic frequencies
   - Rank posts by score + comments
   - Filter Microsoft-relevant posts

2. **LLM synthesis (optional, Phase 2):**
   - Generate narrative summary of the day
   - Identify emerging themes
   - Highlight notable patterns

### 5.2 Synthesis Prompt

*For Phase 2 - LLM-generated digest summary:*

```
SYSTEM:
You are writing the executive summary for a daily developer community digest.
Given the aggregated data below, write a 2-3 sentence overview of what happened today.

Focus on:
- Major themes or trends
- Any notable sentiment patterns
- Microsoft-relevant discussions (highlight if significant)

Keep it concise and actionable for a marketing leader.

USER:
Date: {date}
Posts analyzed: {count}

Sentiment breakdown:
- Positive: {positive_count} ({positive_pct}%)
- Neutral: {neutral_count} ({neutral_pct}%)
- Negative: {negative_count} ({negative_pct}%)

Top topics (by frequency):
{topics_list}

Top technologies mentioned:
{tech_list}

Microsoft-relevant posts: {ms_count}
Controversy flags: {controversy_count}

Top 3 posts by engagement:
1. "{title1}" (r/{sub1}, {score1} pts, {comments1} comments) - {sentiment1}
2. "{title2}" (r/{sub2}, {score2} pts, {comments2} comments) - {sentiment2}
3. "{title3}" (r/{sub3}, {score3} pts, {comments3} comments) - {sentiment3}

---
Write a 2-3 sentence executive summary:
```

### 5.3 Ranking Algorithm

Posts are ranked for inclusion in the digest using a weighted score:

```python
def calculate_digest_rank(post: dict, analysis: dict) -> float:
    """
    Calculate ranking score for digest inclusion.
    Higher score = more prominent placement.
    """
    # Base engagement score (normalized)
    score = post.get("score", 0)
    comments = post.get("num_comments", 0)
    
    # Engagement score (log scale to prevent outlier dominance)
    import math
    engagement = math.log1p(score) * 2 + math.log1p(comments) * 1.5
    
    # Sentiment boost (prioritize strong sentiment for interest)
    confidence = analysis.get("sentiment_confidence", 0.5)
    sentiment = analysis.get("sentiment")
    if sentiment == "negative":
        sentiment_boost = 1.5  # Surface problems
    elif sentiment == "positive":
        sentiment_boost = 1.2  # Surface wins
    else:
        sentiment_boost = 1.0
    
    # Microsoft relevance boost
    ms_boost = 1.5 if analysis.get("microsoft_relevant") else 1.0
    
    # Controversy boost (surface heated discussions)
    controversy_boost = 1.3 if analysis.get("controversy_flag") else 1.0
    
    # Final score
    rank = engagement * sentiment_boost * ms_boost * controversy_boost * confidence
    
    return rank
```

**Digest structure:**

| Section | Selection Criteria | Max Items |
|---------|-------------------|-----------|
| Top Stories | Highest rank score | 5 |
| Microsoft Watch | `microsoft_relevant=True`, sorted by rank | 3 |
| Community Concerns | `sentiment=negative` OR `controversy_flag=True` | 3 |
| Trending Topics | Topic frequency across all posts | 5 |

---

## 6. Error Handling

### 6.1 API Failures

```python
import time
from anthropic import APIError, RateLimitError

def analyze_with_retry(client, prompt: str, max_retries: int = 3) -> dict:
    """Analyze with exponential backoff retry."""
    for attempt in range(max_retries):
        try:
            response = client.messages.create(
                model="claude-sonnet-4-5-20250514",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            return parse_response(response)
        
        except RateLimitError:
            wait_time = 2 ** attempt * 10  # 10s, 20s, 40s
            logger.warning(f"Rate limited, waiting {wait_time}s...")
            time.sleep(wait_time)
        
        except APIError as e:
            logger.error(f"API error on attempt {attempt + 1}: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)
    
    raise Exception("Max retries exceeded")
```

### 6.2 Malformed Responses

```python
import json
from typing import Optional

def parse_analysis_response(response_text: str) -> Optional[dict]:
    """Parse Claude response, handling common malformations."""
    
    # Strip markdown code blocks if present
    text = response_text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    text = text.strip()
    
    try:
        result = json.loads(text)
        
        # Validate required fields
        required = ["sentiment", "topics", "summary"]
        for field in required:
            if field not in result:
                logger.warning(f"Missing required field: {field}")
                return None
        
        # Validate sentiment enum
        if result["sentiment"] not in ["positive", "neutral", "negative"]:
            result["sentiment"] = "neutral"  # Default fallback
        
        return result
    
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {e}")
        logger.debug(f"Raw response: {response_text[:500]}")
        return None
```

### 6.3 Partial Pipeline Failures

| Failure Point | Impact | Recovery Strategy |
|---------------|--------|-------------------|
| Collection fails | No posts | Abort run, alert, retry next hour |
| 1 post analysis fails | 99/100 posts | Log error, continue, note in digest |
| >10% analysis failures | Degraded quality | Complete run, add warning to digest |
| Synthesis fails | No summary | Use code-generated summary fallback |
| Email send fails | No delivery | Retry 3x, then alert Spencer |

```python
class PipelineResult:
    """Track pipeline execution status."""
    posts_collected: int = 0
    posts_analyzed: int = 0
    analysis_failures: int = 0
    synthesis_success: bool = False
    email_sent: bool = False
    errors: list[str] = []
    
    @property
    def success_rate(self) -> float:
        if self.posts_collected == 0:
            return 0
        return self.posts_analyzed / self.posts_collected
    
    @property
    def is_degraded(self) -> bool:
        return self.success_rate < 0.9
```

---

## 7. Cost Optimization

### 7.1 Implemented Optimizations

| Optimization | Savings | Implemented |
|--------------|---------|-------------|
| Unified prompt (3→1 calls) | 66% | In this design |
| Skip empty/deleted posts | Variable | In this design |
| Truncate long content | Reduced input tokens | In this design |

### 7.2 Future Optimizations

| Optimization | Potential Savings | Complexity |
|--------------|-------------------|------------|
| Prompt caching (Anthropic) | Up to 90% on system prompt | Low |
| Batch API (50% off) | 50% if latency acceptable | Medium |
| Cheaper model for simple posts | 30-50% | Medium |
| Skip analysis for low-engagement posts | 20-40% | Low |

### 7.3 Cost Monitoring

```python
class CostTracker:
    """Track API costs per run."""
    
    # Claude Sonnet 4.5 pricing
    INPUT_COST_PER_M = 3.00
    OUTPUT_COST_PER_M = 15.00
    
    def __init__(self):
        self.input_tokens = 0
        self.output_tokens = 0
    
    def add(self, input_tokens: int, output_tokens: int):
        self.input_tokens += input_tokens
        self.output_tokens += output_tokens
    
    @property
    def total_cost(self) -> float:
        input_cost = (self.input_tokens / 1_000_000) * self.INPUT_COST_PER_M
        output_cost = (self.output_tokens / 1_000_000) * self.OUTPUT_COST_PER_M
        return input_cost + output_cost
    
    def log_summary(self):
        logger.info(f"API Usage: {self.input_tokens:,} input, {self.output_tokens:,} output")
        logger.info(f"Estimated cost: ${self.total_cost:.4f}")
```

---

## 8. Validation & Tuning

### 8.1 Pre-Launch Validation

Before going live, validate with real data:

| Test | Method | Success Criteria |
|------|--------|------------------|
| Token estimates | Run 50 posts, measure actual tokens | Within 20% of estimates |
| Parse success rate | Analyze 50 posts | ≥95% valid JSON responses |
| Sentiment accuracy | Manual review 20 posts | ≥80% agreement |
| Topic relevance | Manual review 20 posts | ≥75% relevant topics |
| End-to-end timing | Full pipeline run | <15 minutes for 100 posts |

### 8.2 Ongoing Tuning

Track these metrics weekly:

| Metric | Target | Action if Miss |
|--------|--------|----------------|
| JSON parse success | ≥98% | Review failed responses, adjust prompt |
| Sentiment accuracy | ≥85% | Add few-shot examples for edge cases |
| Summary usefulness | Natalie rating ≥4/5 | Adjust summary prompt constraints |
| Microsoft detection | ≥95% recall | Expand keyword list in prompt |

### 8.3 Prompt Iteration Log

Track prompt changes over time:

| Version | Date | Change | Result |
|---------|------|--------|--------|
| 1.0 | 2026-01-31 | Initial prompt | Baseline |
| | | | |

---

## 9. Implementation Checklist

### Phase 1 Prerequisites

- [ ] **Update RedditCollector** to capture `num_comments`, `permalink`, `upvote_ratio`
- [ ] **Collect sample data** - Run collection on 5 subreddits, save 50 posts
- [ ] **Validate token estimates** - Measure actual token usage vs estimates

### Phase 1 Implementation

- [ ] **Create unified analyzer** - Replace 3-call pattern with single prompt
- [ ] **Add JSON validation** - Pydantic model or manual validation
- [ ] **Add retry logic** - Exponential backoff for API failures
- [ ] **Add cost tracking** - Log token usage per run
- [ ] **Update database schema** - Store new analysis fields

### Phase 1 Testing

- [ ] **Unit tests** - Test JSON parsing, edge cases
- [ ] **Integration test** - Full pipeline with 10 posts
- [ ] **Manual review** - Validate 20 analyses for quality

### Phase 2 (After MVP)

- [ ] Add synthesis prompt for executive summary
- [ ] Implement prompt caching
- [ ] Add confidence-based filtering (skip low-confidence analyses)

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-31 | Spencer | Initial draft |

---

*End of Analysis Design Document*
