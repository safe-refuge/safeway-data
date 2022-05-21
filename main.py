from typing import Optional, List

import typer

import implemented
from config.settings import Settings
from models.point_of_interest import PointOfInterest
from repositories.dumy import DummyWriter


def main(dry_run: Optional[bool] = False):
    settings = Settings(_env_file="config/.env")

    typer.echo(f"Loading records from spreadsheet {settings.spreadsheet_id}")

    overrides = {"settings": settings}
    if dry_run:
        overrides["writer"] = DummyWriter

    component = implemented.ConvertSpreadsheetData(**overrides)
    results: List[PointOfInterest] = component.usecase.convert_spreadsheet(settings.spreadsheet_id)

    typer.echo(f"Saved {len(results)} results into {settings.output_file}")


if __name__ == "__main__":
    typer.run(main)
