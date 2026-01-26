# Issues vs PRD Gap Analysis

## Overview
The GitHub issues were created based on an earlier version of the PRD focused on generic "developer trends." The current PRD has evolved significantly to focus on **Microsoft-specific competitive intelligence** around Copilot, Azure, and Azure AI Foundry. This document outlines the gaps and what needs to change.

---

## Key PRD Changes Since Issues Were Created

### Scope Expansion
- **Old Scope**: Generic developer sentiment across 8 subreddits
- **New Scope**: Microsoft product-specific sentiment + competitive intelligence tracking
  - GitHub Copilot vs Cursor, Tabnine, CodeWhisperer
  - Azure vs AWS, GCP
  - Azure AI Foundry vs OpenAI, AWS Bedrock

### New Feature: Real-Time Alerts
- **OLD**: Daily email only
- **NEW**: Real-time alerts for high-engagement posts (>100 upvotes or >50 retweets)
  - Positive AND negative alerts
  - Slack + email delivery
  - <15 minute latency requirement

### Enhanced Analysis Requirements
- **OLD**: Generic sentiment, topics, pain points
- **NEW**: Product-specific sentiment tracking + competitive comparison detection
  - Per-product sentiment buckets
  - Direct comparison detection ("X vs Y")
  - Switching intent signals
  - Share of voice vs competitors
  - Comparison win rate

### Data Source Changes
- **OLD**: 8 general subreddits (r/programming, r/Python, r/javascript, etc.)
- **NEW**: 
  - Product-specific: r/MicrosoftCopilot, r/github, r/vscode, r/azure, r/AZURE, r/AzureStack
  - Competitor-context: r/MachineLearning, r/artificial, r/LocalLLaMA, r/ChatGPT
  - General dev: r/programming, r/webdev, r/dotnet, r/devops, r/coding
  - X/Twitter: Product mentions, handles, hashtags, competitor terms

---

## Issues That Need Updates

### Phase 2: Data Collection (Spencer-Led)

#### ❌ Issue #4: "Enhance Reddit collector with pagination and filtering"
**Gap**: Doesn't mention product-specific subreddit handling or product tagging
**Required Changes**:
- Add product-specific subreddit list (11 subreddits vs original 8)
- Add product tagging/attribution logic (identify which product is being discussed)
- Add engagement scoring for alert triggering
- Update acceptance criteria to include product attribution accuracy (≥90%)

#### ❌ Issue #5: "Add X/Twitter API integration"
**Gap**: Minimal detail on search strategy
**Required Changes**:
- Define X/Twitter search terms (product mentions, handles, hashtags, competitor terms)
- Add engagement scoring thresholds (>100 upvotes or >50 retweets)
- Add real-time processing requirement (<15 min latency for alerts)
- Note: Free tier may be insufficient; may need to research paid tier

#### ❌ Issue #6: "Implement rate limiting and error handling"
**Status**: Still relevant, no major changes needed
**Enhancement**: Add alert delivery error handling (Slack + email fallback)

#### ❌ Issue #7: "Add data validation layer"
**Gap**: Doesn't mention product attribution validation
**Required Changes**:
- Add validation for product tagging accuracy
- Validate competitive comparison detection
- Validate engagement scoring

#### ❌ Issue #8: "Write collector tests"
**Gap**: Doesn't mention product-specific testing
**Required Changes**:
- Tests for product attribution accuracy (≥90%)
- Tests for competitive comparison detection (≥90% recall)
- Mock data for each product category
- Tests for engagement scoring

---

### Phase 3: Analysis & Intelligence (Natalie-Led)

#### ❌ Issue #9: "Define what 'developer trends' means"
**Gap**: Title and scope are now outdated
**Required Changes**:
- **Rename**: "Define competitive intelligence requirements and analysis framework"
- **New Content**: 
  - Define sentiment analysis per-product (not global)
  - Define competitive analysis: direct comparisons, switching signals, share of voice
  - Product categories: Copilot, Azure, Azure AI Foundry, Adjacent
  - Competitive benchmarks: which competitors to track per category
  - Update acceptance criteria

#### ❌ Issue #10: "Build Claude prompts for sentiment analysis"
**Gap**: Doesn't mention product-specific analysis or alert-trigger detection
**Required Changes**:
- Add per-product sentiment classification (not just overall)
- Add competitive comparison detection prompt
- Add switching intent detection prompt
- Add engagement alert prioritization (important vs noise)
- Add product attribution prompts
- Update accuracy targets (≥80% per-product, ≥90% for competitive detection)

#### ❌ Issue #11: "Create analysis workflows"
**Gap**: Doesn't address competitive intelligence workflows
**Required Changes**:
- Workflow: Track per-product sentiment over time
- Workflow: Detect and tag direct product comparisons
- Workflow: Identify switching signals
- Workflow: Calculate share of voice vs competitors
- Workflow: Prioritize issues for alerts
- Add workflows for real-time alert pipeline

#### ❌ Issue #12: "Design dashboard/report outputs"
**Gap**: Describes generic dashboard; new PRD requires product-specific sections
**Required Changes**:
- Daily email now has 6 distinct sections (instead of 5 themes)
  - Executive Summary (per-product overview)
  - GitHub Copilot Section (sentiment, pain points, highlights, competitive context)
  - Microsoft Azure Section (sentiment, pain points, highlights, competitive context)
  - Azure AI Foundry Section (sentiment, pain points, highlights, competitive context)
  - Adjacent Products Pulse (VS Code, GitHub Actions, etc.)
  - Competitive Intelligence Summary (competitor sentiment, switching signals)
  - Actionable Insights (recommended actions)
- Real-time alert template (new requirement)
- Add Slack alert formatting
- Add metrics dashboard (for internal tracking, not necessarily in daily email)

#### ❌ Issue #13: "Write analysis tests"
**Gap**: Doesn't mention competitive intelligence testing
**Required Changes**:
- Tests for per-product sentiment accuracy (≥80%)
- Tests for competitive comparison detection (≥90% recall)
- Tests for switching signal detection
- Tests for share of voice calculation
- Tests for alert prioritization logic

---

### Phase 4: Integration & Learning

#### ✅ Issue #14: "Connect collectors → analyzer → database"
**Status**: Still relevant
**Enhancement**: Add real-time alert path (alongside daily batch)
- Separate pipeline for high-engagement post detection (<15 min latency)
- Alert delivery to Slack + email

#### ❌ Issue #15: "Build reporting/visualization layer"
**Gap**: Focused on generic dashboard; needs product-specific visualization
**Required Changes**:
- Per-product sentiment trend lines (week-over-week)
- Competitive sentiment comparison charts
- Competitor mention volume vs our products
- Pain point tracking by product (recurring issues)
- Switching signal tracking

#### ✅ Issue #16: "Create documentation for learning outcomes"
**Status**: Still relevant, no changes needed

#### ❌ Issue #17: "Deploy to Azure"
**Gap**: Should mention real-time alert processing requirements
**Required Changes**:
- Deployment must support both batch processing (daily email) and streaming (real-time alerts)
- Async job scheduling for daily email
- Real-time event processing for alert pipeline

---

## NEW Issues to Create

### Phase 2: Data Collection

1. **Product Attribution & Tagging Pipeline**
   - Owner: Spencer
   - Complexity: Medium-High
   - Tasks:
     - Build product tag detection (which product is being discussed)
     - Build product alias mapping (Copilot vs "GH Copilot" vs "copilot ai")
     - Build competitive product mention detection
     - Accuracy target: ≥90%
   
2. **Real-Time Engagement Scoring & Alert Pipeline**
   - Owner: Spencer
   - Complexity: Medium
   - Tasks:
     - Calculate engagement score (upvotes, retweets, comment count)
     - Detect high-engagement thresholds (>100 upvotes or >50 retweets)
     - Stream processing for <15 min latency
     - Integration with alert system

### Phase 3: Analysis & Intelligence

1. **Competitive Comparison Detection**
   - Owner: Natalie
   - Complexity: Medium
   - Tasks:
     - Build Claude prompt for detecting "X vs Y" comparisons
     - Extract competing products and sentiment toward each
     - Track comparison win rate
     - Accuracy target: ≥90% recall

2. **Switching Intent Detection**
   - Owner: Natalie
   - Complexity: Medium
   - Tasks:
     - Build Claude prompt for "switched from X to Y" signals
     - Track direction (TO us vs FROM us)
     - Identify reasons for switching
     - Create weekly switching signals report

3. **Share of Voice Calculation**
   - Owner: Natalie
   - Complexity: Low
   - Tasks:
     - Calculate % of mentions for our products vs competitors
     - Weekly trend analysis
     - Competitive benchmarking metrics

### Phase 3-4: Alert System

1. **Real-Time Alert Pipeline (Slack + Email)**
   - Owner: Spencer + Natalie
   - Complexity: High
   - Tasks:
     - Build Slack webhook integration
     - Template high-engagement alert messages
     - Email fallback delivery
     - Alert routing (product-specific channels)
     - <15 minute latency requirement
     - Alert deduplication (don't alert on same post twice)

2. **Alert Prioritization & Routing**
   - Owner: Natalie
   - Complexity: Medium
   - Tasks:
     - Define alert priority rules (negative > positive, higher engagement = higher priority)
     - Route alerts to appropriate recipients based on product
     - Add ability to snooze/mute certain alerts
     - Track alert response rates (how many alerts result in action)

---

## Summary Table: Issues to Update

| Issue # | Title | Status | Action |
|---------|-------|--------|--------|
| #4 | Enhance Reddit collector | ❌ Update | Add product tagging, product-specific subreddits, attribution accuracy |
| #5 | Add X/Twitter API | ❌ Update | Add search terms, engagement scoring, real-time requirement |
| #6 | Rate limiting & error handling | ✅ OK | Minor: add alert delivery error handling |
| #7 | Data validation | ❌ Update | Add product attribution validation |
| #8 | Collector tests | ❌ Update | Add product attribution tests, competitive detection tests |
| #9 | Define "developer trends" | ❌ Rename & Update | Change to "Define competitive intelligence requirements" |
| #10 | Build Claude prompts | ❌ Update | Add per-product sentiment, competitive comparison, switching intent |
| #11 | Create analysis workflows | ❌ Update | Add competitive intelligence workflows, real-time alert workflows |
| #12 | Design dashboard/report | ❌ Update | Add product-specific sections, alert template, Slack format |
| #13 | Write analysis tests | ❌ Update | Add competitive detection tests, per-product accuracy tests |
| #14 | Connect collectors → analyzer → database | ✅ Update | Enhance with real-time alert path |
| #15 | Build reporting/visualization | ❌ Update | Add per-product sentiment trends, competitive benchmarks |
| #16 | Create documentation | ✅ OK | No changes needed |
| #17 | Deploy to Azure | ❌ Update | Add real-time alert processing requirements |
| — | **NEW**: Product Attribution & Tagging | 🆕 Create | Phase 2, Spencer-led |
| — | **NEW**: Real-Time Engagement Scoring | 🆕 Create | Phase 2, Spencer-led |
| — | **NEW**: Competitive Comparison Detection | 🆕 Create | Phase 3, Natalie-led |
| — | **NEW**: Switching Intent Detection | 🆕 Create | Phase 3, Natalie-led |
| — | **NEW**: Share of Voice Calculation | 🆕 Create | Phase 3, Natalie-led |
| — | **NEW**: Real-Time Alert Pipeline | 🆕 Create | Phase 3-4, Both |
| — | **NEW**: Alert Prioritization & Routing | 🆕 Create | Phase 3-4, Natalie-led |

---

## Recommended Next Steps

1. **Update existing issues** to reflect the new PRD scope (update descriptions, acceptance criteria)
2. **Create new issues** for product-specific features (product attribution, competitive analysis, alert system)
3. **Consider phase timing**: Some Phase 3 items (alert system) might need Phase 2 support
4. **Review with team**: Spencer and Natalie should review these changes to confirm alignment

---

## Questions for Clarification

1. **X/Twitter Free Tier**: Current requirements assume we can filter by engagement level. Free tier may not support this. Should we plan for paid tier?
2. **Alert Channels**: Should alerts go to Slack or email? Both? Different channels for different product categories?
3. **Product Boundaries**: How to handle posts discussing multiple products? (e.g., "Copilot in VS Code is great for Azure development")
4. **Competitor List**: Are the competitor lists (Cursor, Tabnine, AWS, etc.) complete? Should we add others?
5. **Timeline Impact**: Do these additions shift the 4-5 week timeline for MVP? Should we phase real-time alerts into Phase 4?

