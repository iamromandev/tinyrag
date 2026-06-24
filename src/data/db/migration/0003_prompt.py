from typing import ClassVar

from tortoise import migrations
from tortoise.migrations import operations as ops, Operation
from orjson import loads
from tortoise.fields.base import OnDelete
from tortoise.fields.data import JSON_DUMPS
from tortoise.fields.db_defaults import Now
from uuid import uuid4
from tortoise import fields

class Migration(migrations.Migration):
    dependencies: ClassVar[list[tuple[str, str]]] = [('model', '0002_document')]

    initial:ClassVar[bool] = False

    operations: ClassVar[list[Operation]] = [
        ops.CreateModel(
            name='Prompt',
            fields=[
                ('id', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('created_at', fields.DatetimeField(db_index=True, auto_now=False, auto_now_add=True)),
                ('updated_at', fields.DatetimeField(db_index=True, db_default=Now(), auto_now=True, auto_now_add=False)),
                ('deleted_at', fields.DatetimeField(null=True, db_index=True, auto_now=False, auto_now_add=False)),
                ('key', fields.CharField(unique=True, db_index=True, max_length=128)),
                ('name', fields.CharField(max_length=255)),
                ('description', fields.TextField(null=True, unique=False)),
            ],
            options={'table': 'prompt', 'app': 'model', 'pk_attr': 'id'},
            bases=['Base'],
        ),
        ops.CreateModel(
            name='PromptVersion',
            fields=[
                ('id', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('created_at', fields.DatetimeField(db_index=True, auto_now=False, auto_now_add=True)),
                ('updated_at', fields.DatetimeField(db_index=True, db_default=Now(), auto_now=True, auto_now_add=False)),
                ('prompt', fields.ForeignKeyField('model.Prompt', source_field='prompt_id', db_constraint=True, to_field='id', related_name='versions', on_delete=OnDelete.CASCADE)),
                ('version', fields.IntField()),
                ('config', fields.JSONField(default=dict, encoder=JSON_DUMPS, decoder=loads)),
            ],
            options={'table': 'prompt_version', 'app': 'model', 'unique_together': (('prompt', 'version'),), 'pk_attr': 'id', 'table_description': 'Immutable snapshot. Edits create a new version, never mutate one.'},
            bases=['LinkBase'],
        ),
    ]
