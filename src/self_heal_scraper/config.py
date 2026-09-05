"""Configuration models for scraper definitions."""

from dataclasses import dataclass, field
from urllib.parse import urlparse


@dataclass(frozen=True)
class ExtractionRule:
    """Describes how one output field is extracted from HTML."""

    selector: str
    attribute: str | None = None

    def __post_init__(self) -> None:
        if not self.selector.strip():
            raise ValueError("selector must not be empty")
        if self.attribute is not None and not self.attribute.strip():
            raise ValueError("attribute must not be empty")


@dataclass(frozen=True)
class ValidationRule:
    """Describes a deterministic validation constraint for one field."""

    required: bool = True
    min_length: int | None = None

    def __post_init__(self) -> None:
        if self.min_length is not None and self.min_length < 0:
            raise ValueError("min_length must be >= 0")


@dataclass(frozen=True)
class ScraperConfig:
    """Complete, declarative configuration for one scraper."""

    url: str
    fields: tuple[str, ...]
    extraction_rules: dict[str, ExtractionRule]
    validation_rules: dict[str, ValidationRule] = field(default_factory=dict)

    def __post_init__(self) -> None:
        parsed = urlparse(self.url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("url must be an absolute HTTP(S) URL")

        if not self.fields:
            raise ValueError("fields must not be empty")
        if len(set(self.fields)) != len(self.fields):
            raise ValueError("fields must be unique")

        field_names = set(self.fields)
        rule_names = set(self.extraction_rules)
        if field_names != rule_names:
            raise ValueError("fields and extraction_rules must contain the same names")

        unknown_validation = set(self.validation_rules) - field_names
        if unknown_validation:
            raise ValueError(
                "validation_rules contains unknown fields: "
                + ", ".join(sorted(unknown_validation))
            )

    def validation_for(self, field_name: str) -> ValidationRule:
        """Return the configured validation rule, or the default rule."""
        return self.validation_rules.get(field_name, ValidationRule())
