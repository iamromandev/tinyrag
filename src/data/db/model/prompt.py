from tortoise import fields

from src.core.base import Base, LinkBase


class Prompt(Base):
    key = fields.CharField(max_length=128, unique=True, db_index=True)
    name = fields.CharField(max_length=255)
    description = fields.TextField(null=True)

    @property
    def is_active(self) -> bool:
        return self.deleted_at is None

    class Meta:
        table = "prompt"


class PromptVersion(LinkBase):
    """Immutable snapshot. Edits create a new version, never mutate one."""

    prompt = fields.ForeignKeyField(
        to="model.Prompt",
        related_name="versions",
        on_delete=fields.CASCADE,
    )
    version = fields.IntField()
    # Generation params: {"model", "temperature", "max_tokens", "top_p", ...}
    config = fields.JSONField(default=dict)

    class Meta:
        table = "prompt_version"
        unique_together = (("prompt", "version"),)
