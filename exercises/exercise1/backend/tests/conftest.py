import os
import pytest

from app import create_app
from db import get_db


TEST_DB = 'db/test.db'


@pytest.fixture(scope='session')
def client():
    app = create_app(TEST_DB)
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['DEBUG'] = False
    app.config['DB_NAME'] = TEST_DB
    cl = app.test_client()
    with app.app_context():
        db = get_db()
        with app.open_resource('db/install.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        with app.open_resource('db/data.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
    assert not app.debug
    yield cl
    os.remove(TEST_DB)

