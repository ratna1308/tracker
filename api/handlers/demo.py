"""
How to add new sub-applications to main `FastAPI` application?

Refer -
https://fastapi.tiangolo.com/tutorial/bigger-applications/#an-example-file-structure

GET
POST
PUT
PATCH
DELETE
"""

from fastapi import APIRouter, Body, Path, Query
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from starlette.responses import JSONResponse

from api.responses.detail import DetailResponse


class NameIn(BaseModel):
    name: str
    prefix: str = "Mr. "


router = APIRouter(prefix="/api/v1/demo")


@router.get("/", response_model=DetailResponse)
def hello_world():
    return DetailResponse(message="hello world")


############################################
# How to set query parameter for swagger?  #
############################################
@router.get("/hello", response_model=DetailResponse)
def send_data_query(name: str = Query(title="Name", description="The name")):
    """
    TODO
    from fastapi import Query
    This `Query` class can be used for additional validations on query params
    https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#import-query

    Args:
        name:

    Returns:

    """

    return DetailResponse(message=f"Hello {name}")


@router.post("/hello/name", response_model=DetailResponse)
def send_data_body(
    name: NameIn = Body(title="RequestBody", description="The Body of send data")
):
    """
    Response with hello name, where name is user provided

    TODO
    # We use response Body class from fastapi for following reasons.
    https://fastapi.tiangolo.com/tutorial/schema-extra-example/?h=import+body#body-with-example

    Args:
        name:

    Returns:

    """

    return DetailResponse(message=f"Hello {name.prefix} {name.name}")


@router.post("/hello/{name}", response_model=DetailResponse)
def send_data_body(name: str = Path(title="Name")):
    """
    Response with `hello name`, where name is the value from path param

    TODO
    Refer
    https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/#import-path

    Args:
        name:

    Returns:

    """

    return DetailResponse(message=f"Hello..... {name}")


@router.delete("/delete", response_model=DetailResponse)
def delete_data():
    # ADD DELETE LOGIC HERE
    return DetailResponse(message="data has been deleted")


@router.delete(
    "/delete/{name}",
    response_model=DetailResponse,
    responses={404: {"model": DetailResponse}},
)
def delete_data(name: str):
    """

    TODO
    refer
    https://fastapi.tiangolo.com/tutorial/encoder/#json-compatible-encoder


    Args:
        name:

    Returns:

    """
    if name == "admin":
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(
                DetailResponse(message="cannot delete admin data")
            ),
        )

    return DetailResponse(message=f"data has been deleted for - {name}")
