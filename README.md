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

```shell
❯ poetry run python main.py --help
Usage: main.py [OPTIONS]

Options:
  --output TEXT                   [default: data/result.csv]
  --spreadsheet TEXT              [default: 1Y1QLbJ6gvPvz8UI-
                                  TTIUUWv5bDpSNeUVY3h-7OV6tj0]
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.
```