# AI Agent Instructions

## Project Goal

Build a self-healing web scraper that can detect extraction failures, propose constrained repairs, test those repairs, and safely accept only validated changes.

## Before Changing Code

1. Read `PROJECT_SPEC.md`.
2. Read `ARCHITECTURE.md`.
3. Identify the acceptance criteria affected by the change.
4. Prefer the smallest change that satisfies the requirement.

## Engineering Rules

- Keep components separated by responsibility.
- Keep validation deterministic and independent of the LLM.
- Never allow an LLM response to directly become trusted scraper logic without testing and validation.
- Never replace a known-good scraper version with an unvalidated repair.
- Prefer explicit interfaces between Fetcher, Extractor, Validator, Detector, Repairer, and Acceptance Logic.
- Do not add infrastructure or dependencies unless they solve a demonstrated requirement.
- Keep configuration separate from application logic.
- Make failures observable through useful errors and structured results.

## Testing Rules

Every behavioral change should include or update tests.

At minimum, test:

- Successful extraction.
- Invalid or incomplete extraction.
- Failure detection.
- Candidate repair generation at the interface level.
- Repair rejection when validation fails.
- Repair acceptance when validation succeeds.
- Preservation of the previous known-good version after a failed repair.

Tests must not require a live website unless the test specifically verifies integration with an external site.

## LLM Rules

- Treat LLM output as an untrusted proposal.
- Give the LLM only the evidence needed for diagnosis and repair.
- Require structured output from the repairer interface.
- Validate generated extraction logic before accepting it.
- Do not permit arbitrary code execution from generated output in the initial version.

## Change Discipline

- Do not make unrelated refactors while implementing a feature.
- Do not silently change the project requirements or architecture.
- If implementation reveals a conflict with the specification, document the conflict before changing the design.
- Keep commits focused and use clear commit messages.
- Update documentation when a design decision materially changes.

## Definition of Done

A change is complete only when:

1. The implementation matches the specification.
2. Relevant tests pass.
3. Failure paths are handled explicitly.
4. No known-good scraper state can be lost because of an unsuccessful repair.
5. Documentation is updated when required.
