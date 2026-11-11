import importlib

import pytest
from fastapi.testclient import TestClient

import api.main
from api.main import app


def test_predict_should_return_probabilities():
    # Given
    client = TestClient(app)
    test_url = "/predict/3/Braund,%20Mr.%20Owen%20Harris/male/?age=23"

    # When
    response = client.get(test_url)

    # Then
    assert response.status_code == 200
    probabilities = response.json()["input_proba"]
    assert len(probabilities) == 2
    assert sum(probabilities) == pytest.approx(1)


def test_api_should_load_models_from_any_working_directory(tmp_path, monkeypatch):

    # Given
    monkeypatch.chdir(tmp_path)

    # When
    reloaded_api = importlib.reload(api.main)

    # Then
    assert reloaded_api.model is not None
    assert reloaded_api.preprocessor is not None
