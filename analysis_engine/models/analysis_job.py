from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


if TYPE_CHECKING:
    from .repository import Repository


class AnalysisJob(Base):
    __tablename__ = "analysis_analysisjob"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    repository_id: Mapped[int] = mapped_column(
        ForeignKey("repositories_repository.id"),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    branch: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    commit_sha: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
    )

    analysis_version: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    error_message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    repository: Mapped["Repository"] = relationship()