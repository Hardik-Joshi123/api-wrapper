import click
from main import ScraperAPI

@click.group()
def cli():
    """Free API Wrapper CLI Tool"""
    pass

@cli.command()
@click.option("--url", required=True, help="URL to scrape")
@click.option("--output", default="data.json", help="Output file")
def scrape(url, output):
    """Scrape a webpage and save results"""
    api = ScraperAPI()
    data = api.extract_data(url)
    
    with open(output, 'w') as f:
        json.dump(data, f, indent=2)
    
    click.echo(f"Saved {len(data)} items to {output}")

@cli.command()
@click.option("--url", required=True, help="URL to scrape")
def products(url):
    """Extract product data"""
    api = ScraperAPI()
    products = api.get_products(url)
    
    for i, p in enumerate(products[:5]):
        click.echo(f"{i+1}. {p.get('name')} - ${p.get('price')}")
    
    click.echo(f"\nTotal products: {len(products)}")

@cli.command()
@click.option("--url", required=True, help="URL to test")
def test(url):
    """Test CAPTCHA bypass"""
    api = ScraperAPI()
    content = api.get_content(url)
    click.echo(f"Success! Content length: {len(content)}")

if __name__ == "__main__":
    cli()