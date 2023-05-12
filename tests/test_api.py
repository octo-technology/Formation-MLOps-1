from fastapi.responses import Response
from fastapi.testclient import TestClient

from api.main import app


def test_process_name_should_create_column_name_lenght():

    # Given
    client = TestClient(app)
    test_url = "/predict/2/Nasser,%20Mrs.%20Nicholas%20(Adele%20Achem)/female/?&age=14.0&sibSp=1&parch=0&ticket=237736"

    # When
    response: Response = client.get(test_url)

    # Then
    assert 200 == response.status_code
    assert '{"input_proba":[0.2148865583,0.7851134417]}' == response.text
