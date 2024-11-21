import pytest
from src.infra.db.settings.connection import DBConnectionHandler

@pytest.mark.skip(reason="DB connection test")
def test_create_database_engine():
    connection = DBConnectionHandler()
    engine = connection.get_engine()

    assert engine is not None