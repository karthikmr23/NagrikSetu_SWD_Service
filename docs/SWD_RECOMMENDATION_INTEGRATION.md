# NAGRIKSETU — SWD RECOMMENDATION ENGINE INTEGRATION (FR-REC-015 to FR-REC-018)

### 1. Endpoint Contract
* **URL:** `POST /api/swd/recommendations/match`
* **Consumer:** Member 3's Recommendation Engine / Central Agentic AI Orchestrator

### 2. Match Categories & Confidence Scoring
* **`LIKELY_MATCH`** (Score: 0.95): All mandatory and optional preliminary criteria satisfied.
* **`POSSIBLE_MATCH`** (Score: 0.50): Key mandatory criteria met, supplementary optional data missing.
* **`INSUFFICIENT_INFORMATION`** (Score: 0.30): Essential profile attributes unavailable.
* **`UNMET_CRITERIA`** (Score: 0.10): Explicit conflict with one or more mandatory criteria.
