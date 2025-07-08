import pytest
from click.testing import CliRunner
import cli

def test_scrape_command(tmp_path, monkeypatch):
    runner = CliRunner()
    # Patch ScraperAPI to return predictable data
    class DummyAPI:
        def extract_data(self, url):
            return [{"foo": "bar"}]
    monkeypatch.setattr(cli, "ScraperAPI", DummyAPI)
    output_file = tmp_path / "out.json"
    result = runner.invoke(cli.cli, ["scrape", "--url", "https://example.com", "--output", str(output_file)])
    assert result.exit_code == 0
    assert output_file.read_text().startswith("[")


def test_products_command(monkeypatch):
    runner = CliRunner()
    class DummyAPI:
        def get_products(self, url):
            return [{"name": "Test", "price": 1.23} for _ in range(3)]
    monkeypatch.setattr(cli, "ScraperAPI", DummyAPI)
    result = runner.invoke(cli.cli, ["products", "--url", "https://shop.com"])
    assert result.exit_code == 0
    assert "Test" in result.output 