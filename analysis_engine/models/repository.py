from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Repository(Base):
    __tablename__ = "repositories_repository"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    user_id: Mapped[int] = mapped_column(
        nullable=False,
    )

    github_repo_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    github_owner: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    repository_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    default_branch: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )