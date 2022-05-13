from typing import Optional

import typer

import implemented

DEFAULT_SPREADSHEET_ID = "1Y1QLbJ6gvPvz8UI-TTIUUWv5bDpSNeUVY3h-7OV6tj0"


def main(output: Optional[str] = "data/result.csv", spreadsheet: Optional[str] = DEFAULT_SPREADSHEET_ID):
    typer.echo(f"Loading records from spreadsheet: {spreadsheet}")

    usecase = implemented.ConvertSpreadsheetData.usecase
    usecase.convert(output)

    typer.echo(f"Saved results into {output}")


if __name__ == "__main__":
    typer.run(main)
