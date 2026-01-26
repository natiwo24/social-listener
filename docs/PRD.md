# Social Listener - Product Requirements Document

## Executive Summary

**Social Listener** is a daily intelligence platform that monitors developer conversations across Reddit and X (Twitter) to track sentiment, pain points, and highlights for **Microsoft's developer tools ecosystem**—specifically GitHub Copilot, Microsoft Azure, and Azure AI Foundry—along with their competitors. The system delivers actionable insights via daily email summaries and real-time alerts for high-engagement posts, enabling strategic decision-making by product and marketing teams.

---

## 1. Product Vision & Goals

### Vision Statement
*Enable product and marketing leaders to understand how developers perceive Microsoft's developer tools (GitHub Copilot, Azure, Azure AI Foundry) and competing products, so they can make informed decisions about product positioning, messaging, and competitive strategy.*

### Primary Objectives
1. **Track Product Sentiment** - Monitor positive/negative sentiment for target Microsoft products and adjacent tools
2. **Competitive Intelligence** - Understand how competitors are perceived and track comparison discussions
3. **Surface Pain Points** - Identify recurring problems developers face with target products
4. **Highlight Wins** - Recognize what developers appreciate about target products
5. **Enable Rapid Response** - Alert on high-engagement posts (positive or negative) for immediate action

### Success Criteria
- Daily email sends without errors (99%+ uptime)
- Sentiment accuracy ≥80% on sample data
- Track sentiment for all target products and top 3 competitors per category
- Identify product-specific pain points (≥3 per product per week)
- Real-time alerts for high-engagement posts (>100 upvotes or >50 retweets)
- Detect competitive comparison mentions with 90%+ recall

---

## 2. Target Products & Ecosystem

### Primary Target Products

| Product | Aliases / Search Terms | Category |
|---------|------------------------|----------|
| **GitHub Copilot** | "Copilot", "GitHub Copilot", "Copilot Chat", "GH Copilot", "copilot ai" | AI Coding Assistant |
| **Microsoft Azure** | "Azure", "Microsoft Azure", "Azure Cloud", "MS Azure" | Cloud Platform |
| **Azure AI Foundry** | "Azure AI Foundry", "Azure AI services", "Azure OpenAI", "Azure Cognitive Services", "Azure AI Studio", "Microsoft Foundry" | AI Platform |

### Adjacent Products to Track

These products are part of the broader Microsoft developer ecosystem and often appear in related discussions:

| Product | Relationship | Why Track |
|---------|--------------|-----------|
| **VS Code** | Primary IDE for Copilot | Copilot experience tied to VS Code quality |
| **GitHub Actions** | CI/CD platform | Often discussed alongside Azure DevOps |
| **Azure DevOps** | Developer workflow | Competes with GitHub in some scenarios |
| **Azure Functions** | Serverless compute | High-volume discussion, sentiment indicator |
| **Azure Kubernetes Service (AKS)** | Container orchestration | Enterprise cloud indicator |
| **GitHub** (general) | Code hosting platform | Context for Copilot discussions |

---

## 3. Competitive Landscape

### Direct Competitors by Category

| Target Product | Direct Competitors | Notes |
|----------------|-------------------|-------|
| **GitHub Copilot** | Cursor, Tabnine, Codeium, Amazon CodeWhisperer, JetBrains AI Assistant, Sourcegraph Cody | AI coding assistant market |
| **Microsoft Azure** | AWS, Google Cloud Platform (GCP), DigitalOcean, Vercel, Cloudflare | Cloud infrastructure |
| **Azure AI Foundry** | OpenAI API (direct), AWS Bedrock, Google Vertex AI, Hugging Face, Replicate, Anthropic API | AI/ML platforms |

### Competitive Signals to Detect

- **Direct comparisons**: "Copilot vs Cursor", "Azure vs AWS"
- **Switching intent**: "thinking of moving from X to Y", "switched from X to Y"
- **Pricing discussions**: Cost comparisons between products
- **Feature parity**: "X has this but Y doesn't"
- **Migration stories**: Developers sharing transition experiences

### Competitive Metrics to Track

| Metric | Description |
|--------|-------------|
| Share of Voice | % of mentions vs competitors in category |
| Sentiment Differential | Our sentiment vs competitor sentiment |
| Comparison Win Rate | When directly compared, % favoring our product |
| Switching Direction | Net flow of "switched to" vs "switched from" mentions |

---

## 4. Target Users & Use Cases

### Primary Users
1. **Natalie (Product Marketing)** - Uses insights for campaign strategy, messaging, competitive positioning
2. **Spencer (CEO/Technical)** - Uses insights for product roadmap, competitive intelligence
3. **Marketing Managers** - Develop content calendars, respond to competitive narratives

### Key Use Cases

**Use Case 1: Copilot Competitive Response**
- Alert fires: High-engagement Reddit post comparing Copilot unfavorably to Cursor
- Marketing reviews the specific complaints (e.g., "Cursor's multi-file editing is better")
- Team decides whether to respond, create content addressing the gap, or flag to product

**Use Case 2: Azure Sentiment Monitoring**
- Weekly report shows Azure sentiment dropped 8% while AWS sentiment rose
- Team investigates: complaints about Azure Portal UX are spiking
- Escalates to product team with specific pain points and quotes

**Use Case 3: Foundry Launch Tracking**
- New Azure AI Studio feature launches
- Monitor initial sentiment and competitor comparisons
- Identify early issues before they become widespread complaints

**Use Case 4: High-Engagement Alert Response**
- Real-time alert: Tweet with 200+ retweets praising Copilot
- Marketing amplifies the positive content
- OR: Alert for negative viral post, team prepares response strategy

---

## 5. Scope & Features

### MVP (Phase 1-3)

#### Data Collection (Phase 2)
- [ ] **Reddit - Product-Specific Communities**:
  - r/MicrosoftCopilot, r/github, r/vscode
  - r/azure, r/AZURE, r/AzureStack
  - r/MachineLearning, r/artificial, r/LocalLLaMA
- [ ] **Reddit - General Developer Communities** (for competitive context):
  - r/programming, r/webdev, r/dotnet, r/devops
- [ ] **X/Twitter - Product Search Terms**:
  - Product mentions: `"GitHub Copilot"`, `"Azure AI"`, `"Azure Foundry"`, `"Microsoft Azure"`
  - Handles: `@GitHubCopilot`, `@Azure`, `@AzureAI`
  - Hashtags: `#GitHubCopilot`, `#Azure`, `#AzureAI`
  - Competitor terms: `"Cursor AI"`, `"Cursor editor"`, `"AWS"`, `"Tabnine"`, `"CodeWhisperer"`
- [ ] Collect 200+ posts/comments per product category per day
- [ ] Store raw data with metadata (author, score/engagement, timestamp, source, product_tags)

#### Product-Specific Analysis (Phase 3)
- [ ] **Per-Product Sentiment**: Track sentiment separately for each target product
- [ ] **Pain Point Detection**: Flag complaints, bugs, friction tied to specific products
- [ ] **Highlight Detection**: Flag praise, success stories for specific products
- [ ] **Competitive Analysis**:
  - Detect direct product comparisons ("X vs Y")
  - Track switching intent signals
  - Calculate share of voice vs competitors
- [ ] **Engagement Scoring**: Flag high-engagement posts for alerting

#### Daily Email Report
- [ ] **Executive Summary**: Quick pulse across all target products
- [ ] **Per-Product Sections**: Sentiment, volume, top pain point, top highlight for each
- [ ] **Competitive Intelligence**: Share of voice, comparison win rate, switching signals
- [ ] **Adjacent Product Pulse**: Brief sentiment summary for VS Code, GitHub Actions, etc.
- [ ] **Actionable Insights**: Recommended responses or follow-ups

#### Real-Time Alerts (Phase 3)
- [ ] **High-Engagement Positive**: Posts with >100 upvotes or >50 retweets praising target products
- [ ] **High-Engagement Negative**: Posts with >100 upvotes or >50 retweets criticizing target products
- [ ] **Viral Competitive Comparison**: High-engagement posts comparing our products to competitors
- [ ] **Delivery**: Slack notification and/or email within 15 minutes of detection

#### Technical Foundation (Phase 1)
- [ ] SQLite database with posts, comments, analysis results, product tags
- [ ] Configuration management for API credentials and product aliases
- [ ] Error handling and logging
- [ ] Unit tests (80%+ coverage)

### Future (Phase 4+)
- [ ] Dashboard for product sentiment visualization
- [ ] Historical trend analysis (week-over-week, month-over-month per product)
- [ ] Sentiment trend lines by product and competitor
- [ ] Azure deployment for scaling
- [ ] Integration with marketing tools (Slack, Microsoft Teams)
- [ ] Automated competitive report generation
- [ ] Influencer/advocate identification

### Out of Scope (v1)
- Feature-level granularity (e.g., Copilot Chat vs code completion)
- Historical data >6 months
- Sentiment prediction/forecasting
- Automated response posting

---

## 6. Data & Technical Requirements

### Data Sources

**Reddit Communities**:
| Category | Subreddits |
|----------|------------|
| Product-Specific | r/MicrosoftCopilot, r/github, r/vscode, r/azure, r/AZURE, r/AzureStack |
| AI/ML | r/MachineLearning, r/artificial, r/LocalLLaMA, r/ChatGPT |
| General Dev | r/programming, r/webdev, r/dotnet, r/devops, r/coding |

**X/Twitter Search Queries**:
| Category | Search Terms |
|----------|--------------|
| GitHub Copilot | `"GitHub Copilot"`, `"Copilot AI"`, `@GitHubCopilot`, `#GitHubCopilot` |
| Azure | `"Microsoft Azure"`, `"Azure cloud"`, `@Azure`, `#Azure` |
| Azure AI | `"Azure AI"`, `"Azure OpenAI"`, `"Azure Foundry"`, `@AzureAI` |
| Competitors | `"Cursor AI"`, `"Cursor editor"`, `"Tabnine"`, `"CodeWhisperer"`, `"AWS Bedrock"` |

### Data Collection
- **Frequency**: Daily at 6 AM UTC (batch), continuous for high-engagement alerts
- **Volume**: 200+ posts/comments per product category per day
- **Storage**: SQLite locally, migrate to Cloud SQL in Phase 4
- **Retention**: 6 months (180 days) for analysis

### Analysis Requirements
- **Sentiment Accuracy**: ≥80% on validation set
- **Product Attribution Accuracy**: ≥90% (correctly tagging which product is discussed)
- **Processing Latency**: <1 hour from collection to daily email send
- **Alert Latency**: <15 minutes for high-engagement posts
- **Cost**: Estimate $150-250/month for Claude API usage (increased for product analysis)
- **Rate Limits**: Respect all API rate limits gracefully

### Delivery
- **Daily Email Time**: 9 AM UTC
- **Alerts**: Within 15 minutes of high-engagement threshold
- **Format**: HTML email with product sections, links back to source posts
- **Recipients**: natalie@, spencer@, marketing_team@
- **Alert Channels**: Slack (primary), email (backup)

---

## 7. Product Requirements

### Daily Email Report Template

```
Subject: Social Listener Daily Brief - [DATE]
From: social-listener@[domain]

═══════════════════════════════════════════════════════════════
SOCIAL LISTENER DAILY BRIEF
Monday, January 20, 2026
═══════════════════════════════════════════════════════════════

[EXECUTIVE SUMMARY]
• GitHub Copilot: 62% positive (↑3%), 47 mentions
• Microsoft Azure: 55% positive (stable), 112 mentions
• Azure AI Foundry: 48% positive (↓5%), 23 mentions
• 2 high-engagement alerts triggered (see below)

───────────────────────────────────────────────────────────────
[SECTION 1: GITHUB COPILOT]
───────────────────────────────────────────────────────────────
Sentiment: 62% positive (↑3% from yesterday)
Volume: 47 mentions across Reddit and X
Share of Voice vs Competitors: 38% (Cursor: 31%, Tabnine: 18%, Other: 13%)

Top Pain Point:
"Copilot suggestions have gotten noticeably worse since the last
VS Code update. Anyone else seeing this?"
- r/vscode, 156 upvotes

Top Highlight:
"Copilot Chat just saved me 2 hours debugging a regex issue.
Explained the problem AND fixed it."
- X/@dev_sarah, 89 retweets

Competitive Context:
• 8 direct comparisons to Cursor found (5 favored Copilot, 3 favored Cursor)
• 2 "switched from Tabnine" mentions (both positive about switch)

───────────────────────────────────────────────────────────────
[SECTION 2: MICROSOFT AZURE]
───────────────────────────────────────────────────────────────
Sentiment: 55% positive (stable)
Volume: 112 mentions across Reddit and X
Share of Voice vs Competitors: 28% (AWS: 45%, GCP: 22%, Other: 5%)

Top Pain Point:
"Azure Portal is painfully slow today. Takes 10+ seconds to load
any blade. Is there an outage?"
- r/azure, 234 upvotes

Top Highlight:
"Azure Functions cold start improvements in the latest runtime are
actually noticeable. Props to the team."
- r/dotnet, 67 upvotes

Competitive Context:
• 12 Azure vs AWS comparisons (7 favored AWS, 4 favored Azure, 1 neutral)
• Pricing mentioned negatively in 4 posts

───────────────────────────────────────────────────────────────
[SECTION 3: AZURE AI FOUNDRY]
───────────────────────────────────────────────────────────────
Sentiment: 48% positive (↓5% from yesterday)
Volume: 23 mentions across Reddit and X
Share of Voice vs Competitors: 15% (OpenAI direct: 52%, AWS Bedrock: 18%, Other: 15%)

Top Pain Point:
"Azure AI Studio documentation is a maze. Spent 3 hours trying to
figure out how to deploy a custom model."
- r/MachineLearning, 45 upvotes

Top Highlight:
"Finally got Azure OpenAI working in production. The content filtering
is actually a selling point for enterprise clients."
- X/@cloudarchitect, 34 retweets

Competitive Context:
• 3 comparisons to OpenAI direct API (all cited Azure's enterprise features positively)
• 1 migration story: moved FROM AWS Bedrock TO Azure AI (positive)

───────────────────────────────────────────────────────────────
[SECTION 4: ADJACENT PRODUCTS PULSE]
───────────────────────────────────────────────────────────────
• VS Code: 71% positive, 203 mentions (strong week)
• GitHub Actions: 58% positive, 45 mentions (stable)
• Azure DevOps: 42% positive, 28 mentions (↓8%, pipeline complaints)
• Azure Functions: 64% positive, 31 mentions (↑12%)

───────────────────────────────────────────────────────────────
[SECTION 5: COMPETITIVE INTELLIGENCE SUMMARY]
───────────────────────────────────────────────────────────────
Competitor Sentiment (for context):
• Cursor: 74% positive (high enthusiasm, "game changer" mentions)
• AWS: 61% positive (stable, mature perception)
• OpenAI API: 68% positive (but 12% pricing complaints)

Switching Signals This Week:
• 3 "switched to Copilot" mentions
• 1 "switched from Copilot to Cursor" mention
• 2 "considering Azure" mentions (from AWS)

───────────────────────────────────────────────────────────────
[SECTION 6: ACTIONABLE INSIGHTS]
───────────────────────────────────────────────────────────────
1. INVESTIGATE: Copilot quality complaints post-VS Code update -
   potential regression or perception issue?

2. AMPLIFY: Azure Functions cold start praise - good content opportunity

3. MONITOR: Azure AI Studio documentation complaints increasing -
   consider creating tutorial content or flagging to docs team

4. COMPETITIVE: Cursor enthusiasm high - track specific features
   being praised (multi-file editing mentioned 4x)

═══════════════════════════════════════════════════════════════
[FOOTER]
View full data | Configure alerts | Unsubscribe
═══════════════════════════════════════════════════════════════
```

### Real-Time Alert Template

```
Subject: 🚨 HIGH-ENGAGEMENT ALERT: [PRODUCT] - [POSITIVE/NEGATIVE]
From: social-listener-alerts@[domain]

═══════════════════════════════════════════════════════════════
⚡ HIGH-ENGAGEMENT ALERT
═══════════════════════════════════════════════════════════════

Product: GitHub Copilot
Sentiment: NEGATIVE
Engagement: 342 upvotes (threshold: 100)
Source: Reddit r/programming
Time: 2026-01-20 14:32 UTC

POST CONTENT:
"GitHub Copilot has mass-hallucinated AWS credentials into
thousands of repos. This is a serious security issue that
Microsoft needs to address immediately."

CONTEXT:
• Post is 2 hours old and climbing rapidly
• 127 comments, mostly negative
• Cross-posted to r/netsec

RECOMMENDED ACTION:
• Verify claim accuracy
• Prepare response if confirmed
• Monitor for mainstream tech press pickup

───────────────────────────────────────────────────────────────
[View Post] | [Snooze Product 1hr] | [Mark as Handled]
═══════════════════════════════════════════════════════════════
```

### Key Metrics to Track

| Metric | Target | Cadence |
|--------|--------|---------|
| Email Delivery Success Rate | 99%+ | Daily |
| Alert Delivery Latency | <15 min | Per alert |
| Per-Product Sentiment Accuracy | ≥80% | Weekly validation |
| Competitor Mention Detection | ≥90% recall | Weekly validation |
| Product Attribution Accuracy | ≥90% | Weekly validation |
| Pain Points per Product | ≥3 | Weekly |
| High-Engagement Alerts Sent | Track volume | Daily |
| Alert False Positive Rate | <10% | Weekly |
| Marketing Team Action Rate | ≥2 actions/week | Weekly |

---

## 8. Success Metrics & KPIs

### Technical Metrics
- **System Uptime**: 99%+ (daily email sends + alert delivery)
- **Alert Latency**: <15 minutes from post threshold to notification
- **Data Quality**: 0 critical errors, <5 warnings per day
- **Processing Time**: <60 minutes from collection to daily email delivery
- **Database Health**: 0 data loss events

### Product Metrics
- **Engagement**: Marketing team opens email ≥80% of days
- **Alert Response Rate**: Team acknowledges ≥90% of high-engagement alerts within 1 hour
- **Actionability**: Team creates ≥2 pieces of content/week based on insights
- **Sentiment Accuracy**: 80%+ of sentiment classifications validated as correct
- **Product Attribution Accuracy**: 90%+ of posts correctly tagged to products
- **Coverage**: All 3 target products + 6 adjacent products + top 3 competitors per category

### Competitive Intelligence Metrics
- **Share of Voice Tracking**: Daily calculation per product category
- **Comparison Detection Rate**: ≥90% of "X vs Y" posts identified
- **Switching Signal Detection**: Track all "switched to/from" mentions
- **Competitor Sentiment Baseline**: Weekly sentiment scores for top competitors

### Business Metrics (Future)
- Reduction in product surprises (competitor launches, viral issues)
- Faster response time to negative viral posts
- Improved competitive positioning based on gap analysis
- Marketing content aligned with actual developer sentiment

---

## 9. Timeline & Phases

### Phase 1: Foundation
- Set up environments, API credentials
- Configure product aliases and search terms
- Run existing tests
- **Delivery**: Ready-to-code setup with product configuration

### Phase 2: Data Collection
- Enhance Reddit collector for product-specific subreddits
- Implement X API integration with product/competitor search terms
- Add product tagging to data collection
- Rate limiting and error handling
- **Delivery**: Collect 500+ product-relevant posts/day

### Phase 3: Analysis & Intelligence
- Build product-specific sentiment analysis prompts
- Implement competitive comparison detection
- Create per-product analysis workflows
- Design product-focused email template
- Implement high-engagement detection and alerting
- **Delivery**: Working daily email + real-time alerts

### Phase 4: Integration & Deployment
- Connect pipeline end-to-end
- Implement email and Slack alert scheduling
- Deploy to Azure
- Create documentation
- **Delivery**: Production system running with alerts

### Phase 5: Optimization
- Dashboard for product sentiment visualization
- Historical trending by product
- Competitive benchmarking reports
- Performance tuning
- Marketing tool integrations

---

## 10. Constraints & Assumptions

### Constraints
- **Cost**: Keep API costs <$300/month (increased budget for product-specific analysis)
- **Privacy**: No storing personal data; aggregate only
- **Compliance**: Respect Reddit/X ToS
- **Scale**: Start with 500 posts/day, optimize later
- **Alert Volume**: Cap at 10 high-engagement alerts per day to avoid fatigue

### Assumptions
- Developers discussing Microsoft products on Reddit and X are representative of broader sentiment
- Product mentions can be accurately attributed (handling ambiguity like "Copilot" vs "Windows Copilot")
- Sentiment analysis with Claude will be ≥80% accurate for product-specific content
- High-engagement thresholds (100 upvotes, 50 retweets) are appropriate starting points
- Daily email + real-time alerts provide sufficient coverage (not continuous monitoring)
- Marketing team will respond to alerts within 1 hour during business hours
- Competitor sentiment provides useful context for benchmarking

---

## 11. Learning Objectives

### For Spencer
- Mastery of API integration (Reddit PRAW, X API)
- Database design and management at scale
- Error handling and resilience patterns
- System architecture for data pipelines
- Testing strategies (unit, integration)

### For Natalie
- Understanding AI/Claude API capabilities and limitations
- Prompt engineering for business use cases
- Data-driven insights generation
- Using analytics to inform strategy
- Translating technical outputs to business value

### For Both
- Collaborative development workflow (GitHub, Issues, PRs)
- End-to-end product development
- Balancing MVP vs. perfection
- Cloud deployment (Azure)
- Monitoring and observability

---

## 12. Dependencies & Risks

### External Dependencies
- **Reddit API** - Free but rate-limited; PRAW library stability
- **X API** - Free tier very limited; may need paid tier for comprehensive coverage
- **Claude API** - Cost variable based on usage; accuracy depends on prompts
- **Email Service** - Need SMTP or SendGrid account
- **Slack API** - For real-time alert delivery

### Key Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Claude API costs exceed budget | High | Monitor usage weekly, optimize prompts, batch analysis |
| Product attribution errors (e.g., "Copilot" ambiguity) | High | Build disambiguation rules, validate with sample data |
| Sentiment accuracy <80% | High | Validate with sample data, iterate prompts, use product context |
| High-engagement alert fatigue | Medium | Tune thresholds, implement daily caps, add snooze functionality |
| Missing competitor mentions | Medium | Regularly update competitor alias lists, monitor for new entrants |
| Reddit/X API changes ToS | Medium | Have fallback data sources, monitor announcements |
| Alert delivery latency >15 min | Medium | Implement continuous polling, optimize processing pipeline |
| Email delivery fails silently | High | Implement monitoring, Slack fallback |
| Competitor data gaps | Medium | Prioritize top 3 competitors per category, expand gradually |
| Data quality issues | Medium | Add validation layer, log all anomalies |

---

## 13. Non-Functional Requirements

### Performance
- Daily data collection: <30 minutes
- Analysis processing: <30 minutes
- Email generation: <5 minutes
- End-to-end: <60 minutes latency

### Reliability
- Graceful degradation (partial data is acceptable)
- Retry logic for transient failures
- Detailed logging for debugging
- Alerting on critical failures

### Maintainability
- Clear code structure and documentation
- Configurable settings (no hardcoding)
- Automated tests (80%+ coverage)
- Infrastructure as code (Azure deployment)

### Scalability (Future)
- Increase posts from 500 to 5,000/day without architecture change
- Add new data sources (HackerNews, Dev.to) without refactoring
- Scale to 1,000+ users viewing dashboard

---

## 14. Appendix: Key Terminology

- **Target Product**: Primary products being monitored (GitHub Copilot, Azure, Azure AI Foundry)
- **Adjacent Product**: Related Microsoft products tracked for context (VS Code, GitHub Actions, etc.)
- **Competitor**: Direct competitor products in the same category
- **Sentiment**: Emotional tone (Positive, Neutral, Negative)
- **Pain Point**: Problem or friction developers mention about a specific product
- **Highlight**: Praise, success story, or positive mention for a specific product
- **Share of Voice**: Percentage of mentions for a product vs competitors in its category
- **Comparison Win Rate**: When products are directly compared, percentage favoring our product
- **Switching Signal**: Mentions of moving from one product to another
- **High-Engagement Post**: Post exceeding threshold (>100 upvotes or >50 retweets)
- **Product Attribution**: Correctly identifying which product a post is discussing

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Jan 18, 2026 | GitHub Copilot | Initial draft |
| 2.0 | Jan 25, 2026 | Claude | Product-focused rewrite: Added target products (Copilot, Azure, Foundry), competitive intelligence, high-engagement alerts, adjacent product tracking |

---

**Status**: Draft - Updated for product-specific monitoring
