import pytest
from fastapi.testclient import TestClient
from httpx2 import Response

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
