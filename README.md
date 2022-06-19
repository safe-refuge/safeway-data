[![CI](https://github.com/safe-refuge/safeway-data/actions/workflows/test.yml/badge.svg)](https://github.com/safe-refuge/safeway-data/actions/workflows/test.yml)

# safeway-data

Data mining tools for Safeway app.

## Overview

A team of volunteers is building an app for refugees to find help in Europe and avoid human trafficking. It's a project that will have a big impact and save lives. 🇺🇦

The app development is done, we need to load more data about helping points into the app.
Volunteers collected a lot of points into a spreadsheet and we've written a tool in Python to convert it into a CSV format suitable for importing into the app database.
But there are still some enhancements to the data pipeline and new web scraping spiders needed.

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
Saved 272 results into data/output.csv
```

If you have any questions, contact @littlepea

## Data flow

Where are two main ways this CLI tool gets used:

### 1) Converting data from a Google Sheet to CSV

```shell
❯ poetry run python main.py --spreadsheet-id 1Y1QLbJ6gvPvz8UI-TTIUUWv5bDpSNeUVY3h-7OV6tj0
```

This will run the [convert_spreadsheet](usecases/convert_data.py#L45) 
method with the following steps:

* Fetch list of [spreadsheet rows](models/spreadsheet_row.py) from a Google Sheet
* Transform list of spreadsheet rows to list of [Points of Interest](models/point_of_interest.py)
* Optionally, sanitize addresses
* Find missing coordinates by geocoding addresses
* Translate city names to English
* Validate the final list of points
* Save points to a CSV file

### 2) Enhancing CSV data (scraped via spiders)

When we scrape points of interests using spiders (see below) we save results in CSV (as points of interest) 
and then we need to enhance them similar to step 1 above. 

```shell
❯ poetry run python main.py --input-file data/france_red_cross.csv
```

This will run the [convert_file](usecases/convert_data.py#L78) 
method with the following steps:

* Fetch list of points of interest from the input CSV file
* Optionally, sanitize addresses
* Find missing coordinates by geocoding addresses
* Translate city names to English
* Validate the final list of points
* Save points to a CSV file

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

## Using VS Code

VS Code does not immediately recognize the virtual environment location

to make it work (and so imports are properly recognized)

click Run => add configuration  and select Python from the list

this will add a configuration launch.json

you will need to add one line to this configuration

```
"env": {"PYTHONPATH": "${workspaceRoot}"}
```

it should look something like this

```
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "env": {"PYTHONPATH": "${workspaceRoot}"},
            "console": "integratedTerminal",
            "justMyCode": true
        }
    ]
}
```
