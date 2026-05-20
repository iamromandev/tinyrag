from tortoise import fields

from src.core.base import Base


class Document(Base):
    filename = fields.CharField(max_length=512)
    content_type = fields.CharField(max_length=128)
    size_bytes = fields.IntField()
    chunk_count = fields.IntField(default=0)

    class Meta:
        table = "document"
