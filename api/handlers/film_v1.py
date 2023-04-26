import dataclasses
import typing
import uuid
from collections import namedtuple
from functools import lru_cache

from fastapi import APIRouter, Body, Depends, Query, Path, Header, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.datastructures import Headers
from starlette.responses import JSONResponse, Response
from fastapi.security import HTTPBasicCredentials, HTTPBasic

from jose import jwt

from api.dto.film import (
    CreateFilmBody,
    FilmCreatedResponse,
    FilmResponse,
    FilmUpdateBody,
)
from api.entities.film import Film
from api.repository.film.abstractions import FilmRepository, RepositoryException
from api.repository.film.mongo import MongoFilmRepository
from api.dto.detail import DetailResponse
from api.settings import Settings, settings_instance


http_basic = HTTPBasic()


def basic_authentication(
        credentials: HTTPBasicCredentials = Depends(http_basic)
):
    if (
            credentials.username == "prashant"
            and credentials.password == "password@321"
    ):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid credentials"
    )


# router = APIRouter(
#     prefix="/api/v1/films",
#     tags=["films"],
#     dependencies=[Depends(basic_authentication)]
# )
router = APIRouter(
    prefix="/api/v1/films",
    tags=["films"]
)


@lru_cache()
def film_repository(settings: Settings = Depends(settings_instance)):
    """
    Film repository instance to be used as a Fast API dependency.
    """
    return MongoFilmRepository(
        connection_string=settings.mongo_connection_string,
        database=settings.mongo_database_name,
    )


def pagination_params(
    skip: int = Query(0, title="Skip", description="The number of items to skip", ge=0),
    limit: int = Query(
        1000,
        title="Limit",
        description="The limit of the number of items returned",
        le=1000,
    ),
):
    Pagination = namedtuple("Pagination", ["skip", "limit"])
    return Pagination(skip=skip, limit=limit)


@router.post("/", status_code=201, response_model=FilmCreatedResponse)
async def post_create_film(
    film: CreateFilmBody = Body(..., title="Film", description="The film details"),
    repo: FilmRepository = Depends(film_repository),
):
    """
    Creates a film.
    """
    film_id = str(uuid.uuid4())

    await repo.create(
        film=Film(
            film_id=film_id,
            title=film.title,
            description=film.description,
            release_year=film.release_year,
            watched=film.watched,
        )
    )
    return FilmCreatedResponse(id=film_id)


@router.get(
    "/{film_id}",
    responses={200: {"model": FilmResponse}, 404: {"model": DetailResponse}},
)
async def get_film_by_id(
    film_id: str, repo: FilmRepository = Depends(film_repository)
):
    """
    Returns a Film if found, None otherwise.
    """

    film = await repo.get_by_id(film_id=film_id)
    if film is None:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(
                DetailResponse(message=f"Film with id {film_id} is not found.")
            ),
        )
    return FilmResponse(
        id=film.id,
        title=film.title,
        description=film.description,
        release_year=film.release_year,
        watched=film.watched,
    )


@dataclasses.dataclass
class Token:
    name: str
    admin: bool


def authenticate_jwt(
        authorization: typing.Union[str, None] = Header(default=None)
):
    """

    Bearer <token>

    Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.31Fj99vu4Nh5pOECE07DGMcm9tE2IdiLy9MTr2uS-aA

    TODO - refer
    https://jwt.io/
    https://python-jose.readthedocs.io/en/latest/jws/index.html#examples
    https://pypi.org/project/python-jose/

    Args:
        authorization:

    Returns:

    """

    token_secret = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAu1SU1LfVLPHCozMxH2Mo
4lgOEePzNm0tRgeLezV6ffAt0gunVTLw7onLRnrq0/IzW7yWR7QkrmBL7jTKEn5u
+qKhbwKfBstIs+bMY2Zkp18gnTxKLxoS2tFczGkPLPgizskuemMghRniWaoLcyeh
kd3qqGElvW/VDL5AaWTg0nLVkjRo9z+40RQzuVaE8AkAFmxZzow3x+VJYKdjykkJ
0iT9wCS0DRTXu269V264Vf/3jvredZiKRkgwlL9xNAwxXFg0x/XFw005UWVRIkdg
cKWTjpBP2dPwVZ4WWC+9aGVd+Gyn1o0CLelf4rEjGoXbAAEgAqeGUxrcIlbjXfbc
mwIDAQAB
-----END PUBLIC KEY-----"""

    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token"
        )

    token = authorization.split(" ")[1]
    token_payload = jwt.decode(token, token_secret, algorithms=['RS256'])
    return Token(
        name=token_payload.get("name"),
        admin=token_payload.get("admin", False)
    )


@router.get("/", response_model=typing.List[FilmResponse])
async def get_films_by_title(
    title: str = Query(
        ..., title="Title", description="The title of the film.", min_length=3
    ),
    pagination=Depends(pagination_params),
    repo: FilmRepository = Depends(film_repository),
    _=Depends(authenticate_jwt)
):
    """
        This handler returns films by filtering their title.
    """

    films = await repo.get_by_title(
        title, skip=pagination.skip, limit=pagination.limit
    )
    films_return_value = []
    for film in films:
        films_return_value.append(
            FilmResponse(
                id=film.id,
                title=film.title,
                description=film.description,
                release_year=film.release_year,
                watched=film.watched,
            )
        )
    return films_return_value


# Assignment: Create an endpoint which returns all the films.


@router.patch(
    "/{film_id}",
    responses={
        200: {"model": DetailResponse},
        400: {"model": DetailResponse},
    },
)
async def patch_update_film(
    film_id: str = Path(..., title="Film ID", description="The id of the film."),
    update_parameters: FilmUpdateBody = Body(
        ...,
        title="Update Body",
        description="The parameters of the film to be updated.",
    ),
    repo: FilmRepository = Depends(film_repository),
):
    """
    Updates a film.
    """
    try:
        await repo.update(
            film_id=film_id,
            update_parameters=update_parameters.dict(
                exclude_unset=True, exclude_none=True
            ),
        )
        return DetailResponse(message="Film updated.")
    except RepositoryException as e:
        return JSONResponse(
            status_code=400, content=jsonable_encoder(DetailResponse(message=str(e)))
        )


@router.delete("/{film_id}", status_code=204)
async def delete_film(
    film_id: str = Path(..., title="Film ID", description="The id of the film."),
    repo: FilmRepository = Depends(film_repository),
):
    await repo.delete(film_id=film_id)
    return Response(status_code=204)
