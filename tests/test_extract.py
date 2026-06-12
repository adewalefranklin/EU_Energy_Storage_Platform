from eu_energy_pipeline.extract import Extractor
from eu_energy_pipeline.exceptions import ExtractError
import pytest



def test_extract_data_success(mocker):
    fake_response = mocker.Mock()
    fake_response.raise_for_status.return_value = None
    fake_response.json.return_value = {"data": "test_data"}

    mocker.patch(
        "eu_energy_pipeline.extract.Config.get",
        side_effect=lambda key: {
            "AGSI_BASE_URL": "https://agsi.gie.eu/api",
            "AGSI_API_KEY": "fake_api_key",
        }[key],
    )

    mocker.patch(
        "eu_energy_pipeline.extract.requests.get",
        return_value=fake_response,
    )

    extractor = Extractor()
    result = extractor.fetch_data("test_endpoint", {"param1": "value1"})

    assert result == {"data": "test_data"}

def test_extract_data_failure(mocker):

    mocker.patch(
        "eu_energy_pipeline.extract.Config.get",
        side_effect=lambda key: {
            "AGSI_API_KEY": "fake_api_key",
            "AGSI_BASE_URL": "https://fake-url.com"
        }[key]
    )

    mocker.patch(
        "eu_energy_pipeline.extract.requests.get",
        side_effect=Exception("API failed")
    )

    extractor = Extractor()

    with pytest.raises(Exception, match="API failed"):
        extractor.extract_data(
            endpoint="storage",
            params={"country": "DE"}
        )