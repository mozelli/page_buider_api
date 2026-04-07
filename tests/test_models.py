from sqlalchemy import select

from page_builder_api.models import Project, User


def test_create_project(session):
    project = Project(
        user_id='1',
        project_name='project_01',
        project_domain='project01.com.br',
        project_type='type_01',
        project_category='category_01',
        project_description='Project 01 description.',
    )

    session.add(project)
    session.commit()
    session.scalar(select(Project).where(Project.id == 1))

    assert project.project_name == 'project_01'


def test_create_user(session):
    user = User(
        user_email='joaomozelli@gmail.com',
        user_password='12345',
        user_name='João Mozelli Neto',
    )

    session.add(user)
    session.commit()
    session.scalar(select(User).where(User.id == 1))

    assert user.id == 1
