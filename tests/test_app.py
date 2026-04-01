from http import HTTPStatus

from fastapi.testclient import TestClient

from page_builder_api.app import app


def test_read_root_must_return_ok_e_user_data():
    client = TestClient(app)  # Arrange (organização)

    response = client.get('/')  # Act (ação)

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Olá Mundo!'}
