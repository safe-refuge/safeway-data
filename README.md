# safeway-data

Data mining tools for Safeway app.

## Installation

Make sure you have Python 3.9+ and [Poetry](https://python-poetry.org/docs/) installed:

```shell
pip install poetry
```

Then, clone and init the project:

```shell
git clone git@github.com:littlepea/safeway-data.git
cd safeway-data
poetry install
```

## Preparation

In order to access Google Sheets, you'll need to prepare some secrets such as `DEVELOPER_KEY`.

You can place them in `config/.env` file menually or ask @littlepea to provide you a file with secrets.

If you want to fill out the secrets manually you can start from this template:

```shell
cp config/.env.example config/.env
```

## Usage

Check the `--help` for the CLI:

```shell
❯ poetry run python main.py --help
Usage: main.py [OPTIONS]

Options:
  --dry-run / --no-dry-run        [default: no-dry-run]
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.
```

Run the actual conversion script:

```shell
❯ poetry run python main.py          
Loading records from spreadsheet 1Y1QLbJ6gvPvz8UI-TTIUUWv5bDpSNeUVY3h-7OV6tj0
Saved 272 results into data/output.example.csv
```

If you have any questions, contact @littlepea

## Running tests

```shell
❯ poetry run pytest
Test session starts (platform: darwin, Python 3.9.12, pytest 7.1.2, pytest-sugar 0.9.4)
collecting ... 
 tests/test_spreadsheet_adapter.py ✓                                                                                                                                                                      50% █████     
 tests/test_convert_data.py ✓                                                                                                                                                                            100% ██████████

Results (0.34s):
       2 passed
```

## Running web scrapers

All the [Scrapy](https://docs.scrapy.org/) spiders are in the `scraping` directory.

You can run a specific spider by supplying the name and output file:

```shell
poetry run scrapy crawl dopomoga -o data/dopomoga.csv
```

## Creating new spiders

You can place your new spiders into `scraping/spiders` directory and implement according 
to the [Scrapy tutorial](https://docs.scrapy.org/en/latest/intro/tutorial.html).

It's highly recommended to add unit tests for your spider's `parse` method.
