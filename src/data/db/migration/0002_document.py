from typing import ClassVar

from tortoise import migrations
from tortoise.migrations import operations as ops, Operation
from tortoise.fields.db_defaults import Now
from uuid import uuid4
from tortoise import fields

class Migration(migrations.Migration):
    dependencies: ClassVar[list[tuple[str, str]]] = [('model', '0001_initial')]

    initial:ClassVar[bool] = False

    operations: ClassVar[list[Operation]] = [
        ops.CreateModel(
            name='Document',
            fields=[
                ('id', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('created_at', fields.DatetimeField(db_index=True, auto_now=False, auto_now_add=True)),
                ('updated_at', fields.DatetimeField(db_index=True, db_default=Now(), auto_now=True, auto_now_add=False)),
                ('deleted_at', fields.DatetimeField(null=True, db_index=True, auto_now=False, auto_now_add=False)),
                ('filename', fields.CharField(max_length=512)),
                ('content_type', fields.CharField(max_length=128)),
                ('size_bytes', fields.IntField()),
                ('chunk_count', fields.IntField(default=0)),
            ],
            options={'table': 'document', 'app': 'model', 'pk_attr': 'id'},
            bases=['Base'],
        ),
    ]
