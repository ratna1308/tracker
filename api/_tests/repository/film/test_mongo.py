import secrets

import pytest

# noinspection PyUnresolvedReferences
from api.repository.film.mongo import MongoFilmRepository
from api.entities.film import Film
from api.repository.film.abstractions import RepositoryException


@pytest.mark.asyncio
async def test_create():

    repo = MongoFilmRepository(
        connection_string="mongodb://localhost:27017",
        database="my-database"
    )

    await repo.create(
        film=Film(
            film_id="first",
            title="My Film",
            description="My Film Description",
            release_year=2022,
            watched=True,
        )
    )
    film: Film = await repo.get_by_id("first")
    assert film == Film(
        film_id="first",
        title="My Film",
        description="My Film Description",
        release_year=2022,
        watched=True,
    )
    await repo.delete("first")


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
    initial_films, film_id, expected_result
):
    for film in initial_films:
        await repo.create(film)
    film: Film = await repo.get_by_id(film_id)
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
    initial_films, searched_title, expected_films
):
    for film in initial_films:
        await repo.create(film)
    films = await repo.get_by_title(title=searched_title)
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
    skip, limit, expected_results
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
        await repo.create(film)
    results = await repo.get_by_title(
        title="My Film", skip=skip, limit=limit
    )
    assert results == expected_results


@pytest.mark.asyncio
async def test_update():
    initial_film = Film(
        film_id="first",
        title="My Film",
        description="My Film Description",
        release_year=2022,
        watched=True,
    )
    await repo.create(initial_film)
    await repo.update(
        film_id="first", update_parameters={"title": "My M0vie"}
    )
    updated_film = await repo.get_by_id("first")
    assert updated_film == Film(
        film_id="first",
        title="My M0vie",
        description="My Film Description",
        release_year=2022,
        watched=True,
    )


@pytest.mark.asyncio
async def test_update_fail():
    initial_film = Film(
        film_id="first",
        title="My Film",
        description="My Film Description",
        release_year=2022,
        watched=True,
    )
    await repo.create(initial_film)
    with pytest.raises(RepositoryException):
        await repo.update(
            film_id="first", update_parameters={"id": "second"}
        )


@pytest.mark.asyncio
async def test_delete():
    # Setup
    initial_film = Film(
        film_id="first",
        title="My Film",
        description="My Film Description",
        release_year=2022,
        watched=True,
    )
    await repo.create(initial_film)
    # Test
    await repo.delete(film_id="first")
    await repo.delete(film_id=secrets.token_hex(10))
    # Assert
    assert await repo.get_by_id(film_id="first") is None
