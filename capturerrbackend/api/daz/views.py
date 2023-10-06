from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends

from capturerrbackend.api.daz.schema import DazModelDTO, DazModelInputDTO
from capturerrbackend.app.dao.daz_dao import DazDAO
from capturerrbackend.app.models.daz_model import DazModel

router = APIRouter()


@router.get("/", response_model=List[DazModelDTO])
async def get_daz_models(
    limit: int = 10,
    offset: int = 0,
    daz_dao: DazDAO = Depends(),
) -> List[DazModel]:
    """
    Retrieve all daz objects from the database.

    :param limit: limit of daz objects, defaults to 10.
    :param offset: offset of daz objects, defaults to 0.
    :param daz_dao: DAO for daz models.
    :return: list of daz objects from database.
    """
    return await daz_dao.get_all_dazs(limit=limit, offset=offset)


@router.put("/")
async def create_daz_model(
    new_daz_object: DazModelInputDTO,
    daz_dao: DazDAO = Depends(),
) -> None:
    """
    Creates daz model in the database.

    :param new_daz_object: new daz model item.
    :param daz_dao: DAO for daz models.
    """
    await daz_dao.create_daz_model(comment=new_daz_object.comment)
