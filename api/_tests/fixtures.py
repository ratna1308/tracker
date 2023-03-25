import asyncio
import secrets

import pytest

from starlette.testclient import TestClient

from api.api import create_app
from api.repository.film.memory import MemoryFilmRepository
from api.repository.film.mongo import MongoFilmRepository
from api.settings import Settings, settings_instance


@pytest.fixture()
def test_client():
    settings: Settings = settings_instance()
    settings.enable_metrics = False
    return TestClient(app=create_app())


@pytest.fixture()
def memory_film_repo_fixture():
    return MemoryFilmRepository()


@pytest.fixture()
def mongo_film_repo_fixture():
    random_database_name = secrets.token_hex(5)
    repo = MongoFilmRepository(
        connection_string="mongodb://localhost:27017",
        database=random_database_name
    )
    yield repo

    # NOTE - fixture completes its execution until yield statement
    # once fixture has been used (repo yielded to tests) and tests are completed
    # we get the event loop and DB clean up activity is done.

    # noinspection PyProtectedMember
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(repo._client.drop_database(random_database_name))
