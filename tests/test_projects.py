from http import HTTPStatus


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
