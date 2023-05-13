# uncomment this code.

"""
from fastapi.responses import Response
from fastapi.testclient import TestClient

from api.main import app


def test_process_name_should_create_column_name_lenght():

    # Given
    client = TestClient(app)

    # add test_url: an url example of a call api
    test_url = "/predict/..."

    # When
    response: Response = client.get(test_url)  # noqa

    # Then

    # make sure the api returns a success: response.status_code == 200
    # make sure the api returns a given value in the response content, available as "response.text"
    assert True

# Warning: The api requires the processing class and model pickles in order to run.
# In order to run these tests on the github CI you developped, the pickle files must be included to the repository.
# Your package must also be installed on the github test instance during CI configuration.
"""