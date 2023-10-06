from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends
from loguru import logger

from capturerrbackend.api.foo.schema import FooModelDTO, FooModelInputDTO
from capturerrbackend.db.dao.bar_dao import BarDAO
from capturerrbackend.db.dao.foo_dao import FooDAO
from capturerrbackend.db.models.foo_model import FooModel

router = APIRouter()


@router.get("/", response_model=List[FooModelDTO])
async def get_foo_models(
    limit: int = 10,
    offset: int = 0,
    foo_dao: FooDAO = Depends(),
) -> List[FooModel]:
    """
    Retrieve all foo objects from the database.

    :param limit: limit of foo objects, defaults to 10.
    :param offset: offset of foo objects, defaults to 0.
    :param foo_dao: DAO for foo models.
    :return: list of foo objects from database.
    """
    logger.debug("Getting all foo models")
    return await foo_dao.get_all_foos(limit=limit, offset=offset)


@router.put("/")
async def create_foo_model(
    new_foo_object: FooModelInputDTO,
    foo_dao: FooDAO = Depends(),
) -> FooModelDTO:
    """
    Creates foo model in the database.

    :param new_foo_object: new foo model item.
    :param foo_dao: DAO for foo models.
    """
    await foo_dao.create_foo_model(name=new_foo_object.name)
    new_foo = await foo_dao.filter(name=new_foo_object.name)
    return new_foo[0]  # type: ignore


@router.put("/{foo_id}/{bar_title}", response_model=FooModelDTO)
async def add_bar_to_foo(
    foo_id: int,
    bar_title: str,
    foo_dao: FooDAO = Depends(),
    bar_dao: BarDAO = Depends(),
) -> FooModelDTO:
    foo = await foo_dao.get_by_id(id=foo_id)
    if foo is None:
        raise FileNotFoundError

    bar = await bar_dao.filter(title=bar_title)
    if bar is None or bar == []:
        await bar_dao.create_bar_model(title=bar_title)
        bar = await bar_dao.filter(title=bar_title)
    foo.bars.append(bar[0])

    return foo  # type: ignore
