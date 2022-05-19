from typing import List

from pydantic import BaseSettings, Field


DEFAULT_SPREADSHEET_ID = "1Y1QLbJ6gvPvz8UI-TTIUUWv5bDpSNeUVY3h-7OV6tj0"
DEFAULT_RANGE = 'A:L'


class Settings(BaseSettings):
    developer_key: str = Field("", env="DEVELOPER_KEY")
    spreadsheet_id: str = Field(DEFAULT_SPREADSHEET_ID, env="SPREADSHEET_ID")
    cells_range: str = Field(DEFAULT_RANGE, env="CELLS_RANGE")
    countries: List[str] = ["ALL"]
    output_file: str = "data/output.csv"

    class Config:
        env_file = "config/.env"
        env_file_encoding = "utf-8"
