import pytest

from self_heal_scraper.config import ExtractionRule, ScraperConfig, ValidationRule


def valid_config() -> ScraperConfig:
    return ScraperConfig(
        url="https://example.com/products",
        fields=("name", "price"),
        extraction_rules={
            "name": ExtractionRule(".product-name"),
            "price": ExtractionRule(".price"),
        },
        validation_rules={
            "name": ValidationRule(required=True, min_length=1),
            "price": ValidationRule(required=True, min_length=1),
        },
    )


def test_valid_configuration_is_accepted():
    config = valid_config()

    assert config.url == "https://example.com/products"
    assert config.extraction_rules["name"].selector == ".product-name"
    assert config.validation_for("name").min_length == 1


def test_url_must_be_absolute_http_url():
    with pytest.raises(ValueError, match="absolute HTTP\(S\) URL"):
        ScraperConfig(
            url="example.com/products",
            fields=("name",),
            extraction_rules={"name": ExtractionRule(".name")},
        )


def test_fields_and_extraction_rules_must_match():
    with pytest.raises(ValueError, match="same names"):
        ScraperConfig(
            url="https://example.com",
            fields=("name",),
            extraction_rules={"price": ExtractionRule(".price")},
        )


def test_validation_rules_cannot_reference_unknown_fields():
    with pytest.raises(ValueError, match="unknown fields"):
        ScraperConfig(
            url="https://example.com",
            fields=("name",),
            extraction_rules={"name": ExtractionRule(".name")},
            validation_rules={"price": ValidationRule()},
        )


def test_empty_selector_is_rejected():
    with pytest.raises(ValueError, match="selector must not be empty"):
        ExtractionRule("   ")


def test_negative_min_length_is_rejected():
    with pytest.raises(ValueError, match="min_length must be >= 0"):
        ValidationRule(min_length=-1)
