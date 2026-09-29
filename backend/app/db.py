from sqlalchemy import create_engine, Text, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
from pgvector.sqlalchemy import Vector
from .settings import DATABASE_URL

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
Session = sessionmaker(engine)

class Base(DeclarativeBase):
    pass

class Document(Base):
    __tablename__ = "documents"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    version: Mapped[str] = mapped_column(String)
    title: Mapped[str] = mapped_column(String)
    content_hash: Mapped[str] = mapped_column(String)
    markdown: Mapped[str] = mapped_column(Text)
    chunks: Mapped[list["Chunk"]] = relationship(cascade="all, delete-orphan", back_populates="document")

class Chunk(Base):
    __tablename__ = "chunks"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    document_id: Mapped[str] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE"), index=True)
    version: Mapped[str] = mapped_column(String)
    heading: Mapped[str] = mapped_column(String)
    section_id: Mapped[str] = mapped_column(String)
    text: Mapped[str] = mapped_column(Text)
    content_hash: Mapped[str] = mapped_column(String)
    embedding: Mapped[list[float]] = mapped_column(Vector(384))
    document: Mapped[Document] = relationship(back_populates="chunks")
