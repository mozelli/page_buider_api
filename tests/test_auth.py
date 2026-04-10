from http import HTTPStatus


def test_get_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.user_email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_get_token_error_user_not_found(client, user):
    response = client.post(
        '/auth', data={'username': user.user_email, 'password': '000000'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
