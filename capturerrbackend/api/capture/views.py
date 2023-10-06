from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends
from loguru import logger

from capturerrbackend.api.capture.schema import CaptureModelDTO, CaptureModelInputDTO
from capturerrbackend.db.dao.capture_dao import CaptureDAO
from capturerrbackend.db.dao.tag_dao import TagDAO
from capturerrbackend.db.models.capture_model import CaptureModel
from capturerrbackend.db.models.users import (  # type: ignore
    UserRead,
    current_active_user,
)

router = APIRouter()


@router.get("/", response_model=List[CaptureModelDTO])
async def get_capture_models(
    limit: int = 10,
    offset: int = 0,
    capture_dao: CaptureDAO = Depends(),
) -> List[CaptureModel]:
    """
    Retrieve all capture objects from the database.

    :param limit: limit of capture objects, defaults to 10.
    :param offset: offset of capture objects, defaults to 0.
    :param capture_dao: DAO for capture models.
    :return: list of capture objects from database.
    """

    logger.debug("Getting all capture models.")
    return await capture_dao.get_all_captures(limit=limit, offset=offset)


@router.put("/")
async def create_capture_model(
    new_capture_object: CaptureModelInputDTO,
    capture_dao: CaptureDAO = Depends(),
    user: UserRead = Depends(current_active_user),
) -> CaptureModelDTO:
    """
    Creates capture model in the database.

    :param new_capture_object: new capture model item.
    :param capture_dao: DAO for capture models.
    """
    await capture_dao.create_capture_model(text=new_capture_object.text, user=user)
    new_capture = await capture_dao.filter(text=new_capture_object.text)
    return new_capture[0]  # type: ignore


@router.put("/{capture_id}/{tag_name}", response_model=CaptureModelDTO)
async def add_tag_to_capture(
    capture_id: int,
    tag_name: str,
    capture_dao: CaptureDAO = Depends(),
    tag_dao: TagDAO = Depends(),
) -> CaptureModelDTO:
    capture = await capture_dao.get_by_id(id=capture_id)
    tag = await tag_dao.get_or_create(name=tag_name)
    capture.tags.append(tag)  # type: ignore

    return capture  # type: ignore
