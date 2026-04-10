import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from page_builder_api.app import app
from page_builder_api.database import get_session
from page_builder_api.models import Project, User, table_registry
from page_builder_api.security import get_password_hash


class UserFactory(factory.Factory):
    class Meta:
        model = User

    user_name = factory.Sequence(
        lambda n: f'teste{n}'
        )
    user_email = factory.LazyAttribute(
        lambda obj: f'{obj.user_name}@test.com'
        )
    user_password = factory.LazyAttribute(
        lambda obj: f'{obj.user_name}+password'
        )


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override

        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    password = '12345'

    user = UserFactory(user_password=get_password_hash(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password

    return user


@pytest.fixture
def project(session):
    project = Project(
        user_id='1',
        project_name='Projeto 01',
        project_domain='project01.com.br',
        project_type='Landing Page',
        project_category='Marketing',
        project_description='Descrição do Projeto 01',
    )

    session.add(project)
    session.commit()
    session.refresh(project)

    return project


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.user_email, 'password': user.clean_password},
    )

    return response.json()['access_token']
