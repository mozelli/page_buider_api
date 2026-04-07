from http import HTTPStatus

from page_builder_api.schemas import UserPublic


def test_create_project(client):
    response = client.post(
        '/projects',
        json={
            'user_id': '1',
            'project_name': 'Projeto 01',
            'project_domain': 'project01.com.br',
            'project_type': 'Landing Page',
            'project_category': 'Marketing',
            'project_description': 'Descrição do Projeto 01',
        },
    )

    assert response.status_code == HTTPStatus.CREATED


def test_create_project_error_domain_alread_exist(client, project):
    response = client.post(
        '/projects',
        json={
            'user_id': '1',
            'project_name': 'Projeto 01',
            'project_domain': 'project01.com.br',
            'project_type': 'Landing Page',
            'project_category': 'Marketing',
            'project_description': 'Descrição do Projeto 01',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_read_projects(client):
    response = client.get('/projects')

    assert response.status_code == HTTPStatus.OK


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
            'user_email': 'joaomozelli@gmail.com',
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


def test_update_user_error_user_not_foud(client, user, token):
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

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK


def test_delete_user_error_user_not_found(client, user, token):
    response = client.delete('/users/100', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_get_token(client, user):
    response = client.post(
        '/token', data={'username': user.user_email, 'password': user.clean_password}
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_get_token_error_user_not_found(client, user):
    response = client.post(
        '/token', data={'username': user.user_email, 'password': '000000'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND

