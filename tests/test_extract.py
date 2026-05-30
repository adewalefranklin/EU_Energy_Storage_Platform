from eu_energy_pipeline.extract import Extractor


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