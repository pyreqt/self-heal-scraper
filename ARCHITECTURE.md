# System Architecture

## 1. Overview

Self-Heal Scraper is a pipeline that extracts structured data from a web page, validates the result, detects extraction failures, and attempts a constrained repair when the website changes.

```text
Web Page
   |
   v
Fetcher -> Extractor -> Validator -> Detector
                                      |
                              failure detected
                                      v
                              Diagnoser / Repairer
                                      |
                                      v
                                Repair Tester
                                      |
                               +------+------+
                               |             |
                            Accept         Reject
                               |             |
                               v             v
                         New Extraction   Human Review
```

## 2. Components

### Fetcher
Retrieves the target page and preserves the HTML needed for extraction and diagnosis.

### Extractor
Runs the current extraction definition against the fetched page and produces structured output.

### Validator
Checks the output against the configured schema and semantic validation rules. It is independent of the LLM.

### Detector
Determines whether the scraper is healthy using extraction errors, validation failures, missing fields, and significant output anomalies.

### Diagnoser / Repairer
Uses an LLM to inspect the failed extraction, page structure, configuration, and validation errors. It proposes a minimal repair to the extraction logic.

The LLM proposes changes; it does not decide whether its own repair is correct.

### Repair Tester
Runs the proposed repair against the page and validates the resulting output using the same deterministic validation layer.

### Acceptance Logic
Accepts a repair only when it satisfies the configured validation and safety criteria. Otherwise, the repair is rejected and can be escalated for human review.

## 3. Data Flow

1. Fetch the configured URL.
2. Execute the current extractor.
3. Validate the extracted data.
4. Record the result and detect failures or anomalies.
5. If healthy, return the validated result.
6. If unhealthy, provide the relevant evidence to the repairer.
7. Generate a candidate extraction repair.
8. Test the candidate independently.
9. Accept the candidate only if validation succeeds and safety criteria are met.
10. Record the repair and resulting scraper version.

## 4. Key Design Decisions

### Deterministic validation is authoritative
The repair agent cannot declare success. Acceptance is based on deterministic validation and explicit acceptance criteria.

### Repairs are constrained
The repairer changes extraction logic, not arbitrary application code or infrastructure.

### Evidence is preserved
The system should retain the page/extraction evidence required to explain why a repair was proposed and whether it worked.

### Failed repairs are safe
A failed or low-confidence repair must not silently replace a known-good scraper version.

### Components remain separable
Fetcher, extractor, validator, detector, repairer, and acceptance logic have distinct responsibilities so they can be tested independently.

## 5. Initial Technology Boundary

The first implementation should remain small and replaceable:

- Python for the application.
- HTTP/HTML tooling for fetching and parsing.
- A structured extraction configuration rather than hard-coded site-specific logic.
- An LLM provider behind a small repairer interface.
- Automated tests for extraction, validation, failure detection, and repair acceptance.

Specific libraries and infrastructure will be selected during implementation rather than prematurely fixed here.

## 6. Out of Scope for the First Version

- Large-scale distributed crawling.
- Browser automation unless a target site requires it.
- Automatic deployment of arbitrary generated code.
- Unbounded autonomous changes to scraper infrastructure.
- Production-scale scheduling and observability.
