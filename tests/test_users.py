from http import HTTPStatus

from page_builder_api.schemas import UserPublic


def test_create_user(client):
    response = client.post(
        '/users',
        json={
            'user_name': 'João Mozelli Neto',
            'user_email': 'joaomozelli@gmail.com',
            'user_password': '12345',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'user_email': 'joaomozelli@gmail.com',
        'user_name': 'João Mozelli Neto',
    }


def test_create_user_error_email_already_exist(client, user):
    response = client.post(
        '/users',
        json={
            'user_name': 'João Mozelli Neto',
            'user_email': user.user_email,
            'user_password': '12345',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_read_users(client):
    response = client.get('/users')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get('/users')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):

    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'id': user.id,
            'user_name': 'João Mozelli Neto',
            'user_email': 'joaomozelli@gmail.com',
            'user_password': '12345',
        },
    )

    assert response.json() == {
        'id': user.id,
        'user_name': 'João Mozelli Neto',
        'user_email': 'joaomozelli@gmail.com',
    }


def test_update_user_error_user_not_allowed(client, user, token):
    response = client.put(
        '/users/100',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'id': user.id,
            'user_name': 'João Mozelli Neto',
            'user_email': 'joaomozelli@gmail.com',
            'user_password': '12345',
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK


def test_delete_user_error_user_not_allowed(client, user, token):
    response = client.delete(
        '/users/100', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
