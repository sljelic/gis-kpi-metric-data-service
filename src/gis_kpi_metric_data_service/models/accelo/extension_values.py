from sqlalchemy import BigInteger, JSON, String
from sqlalchemy.orm import mapped_column
from ..base import Base


class ExtensionValue(Base):
    __tablename__ = "extension_values"
    __table_args__ = {"schema": "accelo"}
    id = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    field_type = mapped_column(String, nullable=False)
    file_name = mapped_column(String, nullable=False)
    value = mapped_column(JSON(), nullable=False)
    link_id = mapped_column(BigInteger, nullable=True)
    link_type = mapped_column(String, nullable=True)
    field_name = mapped_column(String, nullable=True)
