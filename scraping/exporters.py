import csv

from scrapy.exporters import CsvItemExporter


class CustomCsvItemExporter(CsvItemExporter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        writer_options = self._kwargs.copy()
        writer_options.update(
            delimiter=',',
            quotechar='"',
            quoting=csv.QUOTE_ALL,
            lineterminator='\n'
        )

        self.csv_writer = csv.writer(self.stream, **writer_options)
