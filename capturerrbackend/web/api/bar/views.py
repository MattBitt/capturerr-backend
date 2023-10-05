from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends

from capturerrbackend.db.dao.bar_dao import BarDAO
from capturerrbackend.db.models.bar_model import BarModel
from capturerrbackend.web.api.bar.schema import BarModelDTO, BarModelInputDTO

router = APIRouter()


@router.get("/", response_model=List[BarModelDTO])
async def get_bar_models(
    limit: int = 10,
    offset: int = 0,
    bar_dao: BarDAO = Depends(),
) -> List[BarModel]:
    """
    Retrieve all bar objects from the database.

    :param limit: limit of bar objects, defaults to 10.
    :param offset: offset of bar objects, defaults to 0.
    :param bar_dao: DAO for bar models.
    :return: list of bar objects from database.
    """
    return await bar_dao.get_all_bars(limit=limit, offset=offset)


@router.put("/")
async def create_bar_model(
    new_bar_object: BarModelInputDTO,
    bar_dao: BarDAO = Depends(),
) -> None:
    """
    Creates bar model in the database.

    :param new_bar_object: new bar model item.
    :param bar_dao: DAO for bar models.
    """
    await bar_dao.create_bar_model(title=new_bar_object.title)
