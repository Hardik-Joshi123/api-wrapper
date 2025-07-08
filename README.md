# Free API Wrapper

[![Build Status](https://img.shields.io/github/workflow/status/yourusername/api-wrapper/CI)](https://github.com/yourusername/api-wrapper/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)

> **A production-ready, modular Python framework for extracting structured data from non-API websites.**

---

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [CLI](#cli)
  - [Python API](#python-api)
- [Adapters](#adapters)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Features
- 🚀 **Automatic site type detection and adapter selection**
- 🧠 **Robust HTML parsing and structured data extraction**
- 🛡️ **CAPTCHA bypass** (FlareSolverr, Playwright)
- 🕵️ **Rate limiting, proxy rotation, and caching**
- 🖥️ **CLI and Python API**
- 🧩 **Extensible adapter system**
- 📋 **Production-grade logging and error handling**

---

## Installation
```bash
# Clone the repo
$ git clone https://github.com/yourusername/api-wrapper.git
$ cd api-wrapper

# Install dependencies
$ pip install -r requirements.txt

# (Optional) Install Playwright for CAPTCHA bypass
$ pip install playwright
$ playwright install
```

---

## Configuration
- Copy `.env.example` to `.env` and adjust as needed (timeouts, proxies, FlareSolverr, etc.)
- See `config/settings.py` for all available options.
- Environment variables are supported for all major settings.

---

## Usage
### CLI
```bash
python cli.py scrape --url "https://example.com" --output data.json
python cli.py products --url "https://shop.com/products"
python cli.py test --url "https://site-with-captcha.com"
```

### Python API
```python
from main import ScraperAPI
api = ScraperAPI()
data = api.extract_data("https://example.com")
print(data)
```

---

## Adapters
| Domain         | Supported Sites/Types                        |
|---------------|----------------------------------------------|
| E-commerce    | Amazon, Shopify, eBay, etc.                  |
| Social Media  | Twitter, Instagram, Reddit, Facebook          |
| News          | News sites, blogs                            |
| Forums        | Discourse, phpBB, Reddit threads             |
| Job Boards    | Indeed, LinkedIn Jobs                        |
| Real Estate   | Zillow, Realtor.com                          |
| Financial     | Yahoo Finance, SEC filings                   |
| Government    | Data.gov, public records                     |
| Academic      | Research papers, journals                    |
| Travel        | Booking.com, TripAdvisor                     |
| Generic       | Fallback for all other sites                 |

---

## Testing
Run all tests with:
```bash
pytest tests/
```

---

## Contributing
We welcome contributions! To get started:
1. Fork the repo and create your branch from `main`.
2. Add your feature or bugfix with tests.
3. Run `pytest` to ensure all tests pass.
4. Submit a pull request with a clear description.

Please follow the existing code style and add docstrings to new functions/classes.

---

## License

This project is licensed under the [MIT License](./LICENSE)  
Copyright (c) 2025 Hardik-Joshi123
