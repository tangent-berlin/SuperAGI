"""renamed_tokens_calls

Revision ID: 35e47f20475b
Revises: 598cfb37292a
Create Date: 2023-06-06 04:34:15.101672

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "35e47f20475b"
down_revision = "598cfb37292a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "agent_executions", sa.Column("num_of_calls", sa.Integer(), nullable=True)
    )
    op.add_column(
        "agent_executions", sa.Column("num_of_tokens", sa.Integer(), nullable=True)
    )
    op.drop_column("agent_executions", "calls")
    op.drop_column("agent_executions", "tokens")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "agent_executions",
        sa.Column("tokens", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "agent_executions",
        sa.Column("calls", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.drop_column("agent_executions", "num_of_tokens")
    op.drop_column("agent_executions", "num_of_calls")
    # ### end Alembic commands ###
