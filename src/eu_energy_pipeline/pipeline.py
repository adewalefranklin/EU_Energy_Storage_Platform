from eu_energy_pipeline.extract import Extractor

extractor = Extractor()

data = extractor.fetch_storage_data(
    country="AT",
    company="25X-OMVGASSTORA5",
    facility="21W000000000081Y",
    start_date="2026-05-01",
    end_date="2026-05-05",
)

print(data)
