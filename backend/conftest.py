import pytest
from django.db import connections

@pytest.fixture(autouse=True, scope='session')
def clean_db_connections():
    yield
    for conn in connections.all():
        conn.close()
