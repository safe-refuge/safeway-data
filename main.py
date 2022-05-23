from typing import Optional, List

import typer

import implemented
from config.settings import Settings
from models.point_of_interest import PointOfInterest
from repositories.dumy import DummyWriter


def main(
        dry_run: Optional[bool] = False,
        spreadsheet_id: Optional[str] = None,
        input_file: Optional[str] = None,
):
    settings = Settings(_env_file="config/.env")

    spreadsheet_id = spreadsheet_id or settings.spreadsheet_id
    source = "file" if input_file else "spreadsheet"

    typer.echo(f"Loading records from {source} {input_file or spreadsheet_id}")

    overrides = {"settings": settings, "log": typer.echo}
    if dry_run:
        overrides["writer"] = DummyWriter

    component = implemented.ConvertSpreadsheetData(**overrides)
    results: List[PointOfInterest] = \
        component.usecase.convert_file(input_file) \
        if input_file \
        else component.usecase.convert_spreadsheet(spreadsheet_id)

    typer.echo(f"Saved {len(results)} results into {settings.output_file}")


if __name__ == "__main__":
    typer.run(main)
