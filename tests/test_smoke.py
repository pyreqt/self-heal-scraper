import subprocess
import sys


def test_package_smoke():
    import self_heal_scraper

    assert self_heal_scraper.__version__ == "0.1.0"


def test_package_has_executable_entry_point():
    result = subprocess.run(
        [sys.executable, "-m", "self_heal_scraper"],
        capture_output=True,
        text=True,
        check=True,
    )

    assert "self-heal-scraper 0.1.0" in result.stdout
