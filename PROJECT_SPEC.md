# Self-Healing Web Scraper — Project Specification

## 1. Problem

Web scrapers are brittle: websites change HTML structure, selectors, labels, and embedded data. A scraper can continue running while silently producing incomplete or incorrect data.

We will build a scraper that can detect extraction failures, diagnose likely causes, propose a repair, test the repair, and accept it only when validation passes.

## 2. Goal

Build a working prototype that can scrape a defined website/data source and automatically recover from realistic extraction changes without requiring the developer to manually rewrite the scraper.

## 3. Core workflow

1. Fetch a target page.
2. Extract structured records using the current scraper definition.
3. Validate the extracted records against explicit quality rules.
4. Detect and classify failures.
5. Generate one or more repair candidates.
6. Test candidates against the affected page/fixtures.
7. Validate repaired output.
8. Accept a repair only when confidence and validation thresholds are met.
9. Record the repair and its evidence for review/audit.
10. Escalate to human review when the agent cannot establish sufficient confidence.

## 4. Functional requirements

### FR1 — Scraping
The system must fetch a target page and extract a predefined schema of fields.

### FR2 — Validation
The system must validate presence, type, format, and basic plausibility of extracted fields.

### FR3 — Failure detection
The system must identify conditions such as zero records, missing required fields, abnormal field distributions, or validation failures.

### FR4 — Diagnosis
The system must inspect the page and scraper definition and produce a structured diagnosis of the likely failure cause.

### FR5 — Repair generation
The system must generate a replacement extraction strategy rather than blindly modifying production logic.

### FR6 — Repair validation
A candidate repair must run against test input and pass predefined validation checks before it can be accepted.

### FR7 — Safe acceptance
The system must not replace a working scraper merely because an alternative candidate exists. The candidate must meet explicit acceptance criteria.

### FR8 — Audit trail
Each healing attempt must record the failure, diagnosis, candidate repair, validation results, and final decision.

### FR9 — Human escalation
If no candidate satisfies the acceptance criteria, the system must report the failure and provide enough evidence for manual intervention.

## 5. Non-functional requirements

- Deterministic validation rules must be separate from LLM reasoning.
- Repairs must be reproducible from recorded inputs where practical.
- The system must provide structured logs for debugging.
- Network and model failures must fail safely rather than silently accepting bad data.
- The prototype should remain small enough to understand and test locally.

## 6. Self-healing boundary

For the first version, self-healing means repairing the **data extraction logic**. It does not mean automatically changing arbitrary application code, bypassing anti-bot protections, or making unrestricted changes to the target website.

The repair agent may propose changes to selectors, extraction expressions, or parsing logic within a constrained scraper interface.

## 7. Acceptance criteria

The prototype is successful when it can:

1. Correctly scrape the original fixture/site.
2. Detect a deliberately introduced structural change that breaks the original extraction logic.
3. Diagnose the extraction failure.
4. Produce a repair candidate.
5. Demonstrate that the candidate restores valid structured output.
6. Reject a deliberately bad repair candidate.
7. Preserve an audit record of the healing attempt.

## 8. Initial implementation constraints

- Python-based prototype.
- Automated tests are required.
- Scraper logic and healing/orchestration logic must be separated.
- Use fixtures for repeatable failure/recovery tests rather than depending exclusively on a live website.
- LLM integration will be introduced only after the deterministic scraper, validation, and failure-recovery interfaces are established.

## 9. Out of scope for v1

- Production-scale distributed crawling.
- CAPTCHA or anti-bot bypass.
- Arbitrary autonomous code execution.
- Fully autonomous deployment to production.
- Guaranteeing that every website change can be repaired.
