from pydantic import BaseModel, ConfigDict, EmailStr


class UserSchema(BaseModel):
    user_email: EmailStr
    user_password: str
    user_name: str


class UserPublic(BaseModel):
    id: int
    user_email: EmailStr
    user_name: str
    model_config = ConfigDict(from_attributes=True)


class UsersList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class ProjectSchema(BaseModel):
    user_id: str
    project_name: str
    project_domain: str
    project_type: str
    project_category: str
    project_description: str


class ProjectDB(ProjectSchema):
    id: int


class ProjectPublic(BaseModel):
    id: int
    project_name: str
    project_domain: str
    project_type: str
    project_category: str
    project_description: str


class ProjectsList(BaseModel):
    projects: list[ProjectPublic]
