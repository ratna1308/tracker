import secrets

import pytest

# noinspection PyUnresolvedReferences
from api._tests.fixtures import mongo_film_repo_fixture
from api.repository.film.mongo import MongoFilmRepository
from api.entities.film import Film
from api.repository.film.abstractions import RepositoryException


async def test_create(mongo_film_repo_fixture):
    await mongo_film_repo_fixture.create(
        film=Film(
            film_id="first",
            title="My Film",
            description="My Film Description",
            release_year=2022,
            watched=True,
        )
    )

    film: Film = await mongo_film_repo_fixture.get_by_id("first")
    assert film == Film(
        film_id="first",
        title="My Film",
        description="My Film Description",
        release_year=2022,
        watched=True,
    )
    await mongo_film_repo_fixture.delete("first")


@pytest.mark.parametrize(
    "initial_films, film_id, expected_result",
    [
        pytest.param([], "any", None, id="empty-case"),
        pytest.param(
            [
                Film(
                    film_id="first",
                    title="My Film",
                    description="My Film Description",
                    release_year=2022,
                    watched=True,
                ),
                Film(
                    film_id="second",
                    title="My Second Film",
                    description="My Second Film Description",
                    release_year=2023,
                    watched=False,
                ),
            ],
            "second",
            Film(
                film_id="second",
                title="My Second Film",
                description="My Second Film Description",
                release_year=2023,
                watched=False,
            ),
            id="film-found",
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_by_id(
    mongo_film_repo_fixture, initial_films, film_id, expected_result
):
    for film in initial_films:
        await mongo_film_repo_fixture.create(film)
    film: Film = await mongo_film_repo_fixture.get_by_id(film_id)
    assert film == expected_result


@pytest.mark.parametrize(
    "initial_films,searched_title,expected_films",
    [
        pytest.param([], "random title", [], id="empty-case"),
        pytest.param(
            [
                Film(
                    film_id="first",
                    title="My Film",
                    description="My Film Description",
                    release_year=2022,
                    watched=True,
                ),
                Film(
                    film_id="second",
                    title="My Second Film",
                    description="My Second Film Description",
                    release_year=2023,
                    watched=False,
                ),
                Film(
                    film_id="first_remake",
                    title="My Film",
                    description="My Film Description remake of the first film from 2022",
                    release_year=2025,
                    watched=True,
                ),
            ],
            "My Film",
            [
                Film(
                    film_id="first",
                    title="My Film",
                    description="My Film Description",
                    release_year=2022,
                    watched=True,
                ),
                Film(
                    film_id="first_remake",
                    title="My Film",
                    description="My Film Description remake of the first film from 2022",
                    release_year=2025,
                    watched=True,
                ),
            ],
            id="found-films",
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_by_title(
    mongo_film_repo_fixture, initial_films, searched_title, expected_films
):
    for film in initial_films:
        await mongo_film_repo_fixture.create(film)
    films = await mongo_film_repo_fixture.get_by_title(title=searched_title)
    assert films == expected_films


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "skip,limit,expected_results",
    [
        pytest.param(
            0,
            0,
            [
                Film(
                    film_id="my-id",
                    title="My Film",
                    description="My description",
                    release_year=1990,
                ),
                Film(
                    film_id="my-id-2",
                    title="My Film",
                    description="My description",
                    release_year=1990,
                ),
                Film(
                    film_id="my-id-3",
                    title="My Film",
                    description="My description",
                    release_year=1990,
                ),
            ],
        ),
        pytest.param(
            0,
            1,
            [
                Film(
                    film_id="my-id",
                    title="My Film",
                    description="My description",
                    release_year=1990,
                )
            ],
        ),
        pytest.param(
            1,
            1,
            [
                Film(
                    film_id="my-id-2",
                    title="My Film",
                    description="My description",
                    release_year=1990,
                )
            ],
        ),
    ],
)
async def test_get_by_title_pagination(
    mongo_film_repo_fixture, skip, limit, expected_results
):
    film_seed = [
        Film(
            film_id="my-id",
            title="My Film",
            description="My description",
            release_year=1990,
        ),
        Film(
            film_id="my-id-2",
            title="My Film",
            description="My description",
            release_year=1990,
        ),
        Film(
            film_id="my-id-3",
            title="My Film",
            description="My description",
            release_year=1990,
        ),
    ]
    for film in film_seed:
        await mongo_film_repo_fixture.create(film)
    results = await mongo_film_repo_fixture.get_by_title(
        title="My Film", skip=skip, limit=limit
    )
    assert results == expected_results


@pytest.mark.asyncio
async def test_update(mongo_film_repo_fixture):
    initial_film = Film(
        film_id="first",
        title="My Film",
        description="My Film Description",
        release_year=2022,
        watched=True,
    )
    await mongo_film_repo_fixture.create(initial_film)
    await mongo_film_repo_fixture.update(
        film_id="first", update_parameters={"title": "My M0vie"}
    )
    updated_film = await mongo_film_repo_fixture.get_by_id("first")
    assert updated_film == Film(
        film_id="first",
        title="My M0vie",
        description="My Film Description",
        release_year=2022,
        watched=True,
    )


@pytest.mark.asyncio
async def test_update_fail(mongo_film_repo_fixture):
    initial_film = Film(
        film_id="first",
        title="My Film",
        description="My Film Description",
        release_year=2022,
        watched=True,
    )
    await mongo_film_repo_fixture.create(initial_film)
    with pytest.raises(RepositoryException):
        await mongo_film_repo_fixture.update(
            film_id="first", update_parameters={"id": "second"}
        )


@pytest.mark.asyncio
async def test_delete(mongo_film_repo_fixture):
    # Setup
    initial_film = Film(
        film_id="first",
        title="My Film",
        description="My Film Description",
        release_year=2022,
        watched=True,
    )
    await mongo_film_repo_fixture.create(initial_film)
    # Test
    await mongo_film_repo_fixture.delete(film_id="first")
    await mongo_film_repo_fixture.delete(film_id=secrets.token_hex(10))
    # Assert
    assert await mongo_film_repo_fixture.get_by_id(film_id="first") is None
