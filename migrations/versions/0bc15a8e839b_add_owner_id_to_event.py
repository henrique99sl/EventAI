"""Add owner_id to Event

Revision ID: 0bc15a8e839b
Revises: 7b444549c1a2
Create Date: 2025-08-11 01:24:18.671145

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0bc15a8e839b"
down_revision = "acf34b048ac1"
branch_labels = None
depends_on = None


def upgrade():
    # Passo 1: Adiciona a coluna como nullable
    with op.batch_alter_table("events", schema=None) as batch_op:
        batch_op.add_column(sa.Column("owner_id", sa.Integer(), nullable=True))
        batch_op.alter_column("date", existing_type=sa.DATE(), nullable=False)
        batch_op.alter_column("venue_id", existing_type=sa.INTEGER(), nullable=False)
        batch_op.create_foreign_key("fk_owner_id", "users", ["owner_id"], ["id"])

    # Passo 2: Atualiza todos os registros antigos para owner_id = 1
    op.execute("UPDATE events SET owner_id = 1 WHERE owner_id IS NULL")

    # Passo 3: Torna a coluna NOT NULL
    with op.batch_alter_table("events", schema=None) as batch_op:
        batch_op.alter_column("owner_id", nullable=False)


def downgrade():
    with op.batch_alter_table("events", schema=None) as batch_op:
        batch_op.drop_constraint("fk_owner_id", type_="foreignkey")
        batch_op.alter_column("venue_id", existing_type=sa.INTEGER(), nullable=True)
        batch_op.alter_column("date", existing_type=sa.DATE(), nullable=True)
        batch_op.drop_column("owner_id")
