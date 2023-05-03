# noinspection PyPackageRequirements
import pytest

# noinspection PyUnresolvedReferences
from api.entities.film import Film

# from api.repository.film.abstractions import RepositoryException
from api.repository.film.abstractions import RepositoryException
from api.repository.film.memory import MemoryFilmRepository


@pytest.mark.asyncio
async def test_create():
    repo = MemoryFilmRepository()

    film = Film(
        film_id="test",
        title="My Film",
        description="My description",
        release_year=1990,
    )
    await repo.create(film)
    assert await repo.get_by_id("test") is film


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "films_seed,film_id,expected_result",
    [
        pytest.param([], "my-id", None, id="empty"),
        pytest.param(
            [
                Film(
                    film_id="my-id",
                    title="My Film",
                    description="My description",
                    release_year=1990,
                )
            ],
            "my-id",
            Film(
                film_id="my-id",
                title="My Film",
                description="My description",
                release_year=1990,
            ),
            id="actual-film",
        ),
    ],
)
async def test_get_by_id(films_seed, film_id, expected_result):
    repo = MemoryFilmRepository()
    for film in films_seed:
        await repo.create(film)
    film = await repo.get_by_id(film_id=film_id)
    assert film == expected_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "films_seed,film_title,expected_results",
    [
        pytest.param([], "some-title", [], id="empty-results"),
        pytest.param(
            [
                Film(
                    film_id="my-id",
                    title="My Film",
                    description="My description",
                    release_year=1990,
                )
            ],
            "some-title",
            [],
            id="empty-results-2",
        ),
        pytest.param(
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
            ],
            "My Film",
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
            ],
            id="results",
        ),
    ],
)
async def test_get_by_title(films_seed, film_title, expected_results):
    repo = MemoryFilmRepository()
    for film in films_seed:
        await repo.create(film)

    # noinspection PyTypeChecker
    result = await repo.get_by_title(title=film_title)
    assert result == expected_results


@pytest.mark.asyncio
async def test_update_fail():
    repo = MemoryFilmRepository()
    await repo.create(
        Film(
            film_id="my-id-2",
            title="My Film",
            description="My description",
            release_year=1990,
        )
    )
    with pytest.raises(RepositoryException):
        await repo.update(film_id="my-id-2", update_parameters={"id": "fail"})


@pytest.mark.asyncio
async def test_delete():
    repo = MemoryFilmRepository()
    await repo.create(
        Film(
            film_id="my-id-2",
            title="My Film",
            description="My description",
            release_year=1990,
        )
    )
    await repo.delete("my-id-2")
    assert await repo.get_by_id("my-id-2") is None


@pytest.mark.asyncio
async def test_update():
    repo = MemoryFilmRepository()
    await repo.create(
        Film(
            film_id="my-id-2",
            title="My Film",
            description="My description",
            release_year=1990,
        )
    )
    await repo.update(
        film_id="my-id-2",
        update_parameters={
            "title": "My updated Film",
            "description": "My updated description",
            "release_year": 2010,
            "watched": True,
        },
    )
    film = await repo.get_by_id("my-id-2")
    assert film == Film(
        film_id="my-id-2",
        title="My updated Film",
        description="My updated description",
        release_year=2010,
        watched=True,
    )
