from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class Project:
    __tablename__ = 'projects'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[str]
    project_name: Mapped[str]
    project_domain: Mapped[str] = mapped_column(unique=True)
    project_type: Mapped[str]
    project_category: Mapped[str]
    project_description: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_name: Mapped[str]
    user_email: Mapped[str] = mapped_column(unique=True)
    user_password: Mapped[str]
