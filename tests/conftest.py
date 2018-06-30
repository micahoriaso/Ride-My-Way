import pytest

from flaskr import create_app
from flaskr.db import create_db_tables

@pytest.fixture
def app():
    app = create_app()
    yield app


@pytest.fixture()
def client(app, setup):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture(scope='module')
def setup(request):
    create_db_tables()

    def teardown():
        create_db_tables()
    request.addfinalizer(teardown)
