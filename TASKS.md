# Implementation Tasks

The tasks are ordered by dependency. Each task should produce a small, testable increment.

## Phase 1 — Foundation

- [x] **T1: Project setup**
  - Create the Python package structure.
  - Add dependency and test configuration.
  - Add a minimal executable entry point.
  - Verify the project can run and tests can execute.

- [x] **T2: Scraper configuration model**
  - Define the URL, expected fields, extraction rules, and validation rules.
  - Keep configuration separate from application logic.
  - Add configuration validation tests.

## Phase 2 — Deterministic Scraping Pipeline

- [ ] **T3: Fetcher**
  - Fetch HTML from a URL.
  - Return useful errors for failed requests.
  - Test with mocked HTTP responses.

- [ ] **T4: Extractor**
  - Execute the configured extraction rules.
  - Return structured data plus extraction diagnostics.
  - Test successful and broken selectors.

- [ ] **T5: Validator**
  - Validate extracted data against the configured schema and rules.
  - Produce structured validation failures.
  - Keep this component independent of the LLM.

- [ ] **T6: Failure detector**
  - Combine extraction and validation signals to determine whether the scraper is unhealthy.
  - Test missing fields, malformed values, and extraction failures.

## Phase 3 — Self-Healing

- [ ] **T7: Repairer interface**
  - Define a strict interface for an LLM repair proposal.
  - Use structured output.
  - Do not execute generated arbitrary code.

- [ ] **T8: Repair diagnosis and proposal**
  - Provide the repairer with page evidence, current extraction rules, and validation failures.
  - Generate a candidate extraction-rule change.
  - Test using a mocked repairer before integrating a real LLM.

- [ ] **T9: Repair tester**
  - Apply a candidate repair in isolation.
  - Run extraction and deterministic validation.
  - Never mutate the known-good configuration during testing.

- [ ] **T10: Acceptance and versioning**
  - Accept only validated repairs.
  - Preserve the previous known-good version on failure.
  - Record repair results and versions.

## Phase 4 — End-to-End Product

- [ ] **T11: End-to-end self-healing flow**
  - Connect fetch → extract → validate → detect → repair → test → accept/reject.
  - Demonstrate recovery from a deliberately changed page structure.

- [ ] **T12: CLI / user interface**
  - Add a simple command for running a scraper.
  - Show extraction results, failures, repair attempts, and final status.

- [ ] **T13: Observability and audit trail**
  - Record structured run and repair information.
  - Make it possible to understand why a repair was accepted or rejected.

## Phase 5 — Quality

- [ ] **T14: Integration tests**
  - Test the complete pipeline using controlled local HTML fixtures.

- [ ] **T15: Documentation and demonstration**
  - Document setup and usage.
  - Add a reproducible self-healing example.
  - Update the README with the final workflow.

## Execution Rule

Implement one task at a time. A task is complete only when its tests pass and its acceptance criteria are satisfied. Do not start the next task by assuming the previous task works.
