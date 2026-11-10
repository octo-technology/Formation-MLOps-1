import importlib

import pytest
from fastapi.testclient import TestClient
from httpx2 import Response

import api.main
from api.main import app


def test_predict_should_return_probabilities():

    # Given
    client = TestClient(app)
    test_url = "/predict/2/Nasser,%20Mrs.%20Nicholas%20(Adele%20Achem)/female/?age=14.0&sib_sp=1&parch=0&ticket=237736"

    # When
    response: Response = client.get(test_url)

    # Then
    assert response.status_code == 200
    assert response.json() == {"input_proba": pytest.approx([0.052635613, 0.947364387])}


def test_api_should_load_models_from_any_working_directory(tmp_path, monkeypatch):

    # Given
    monkeypatch.chdir(tmp_path)

    # When
    reloaded_api = importlib.reload(api.main)

    # Then
    assert reloaded_api.model is not None
    assert reloaded_api.preprocessor is not None
