from typing import Annotated, List

from fastapi import APIRouter
from fastapi.param_functions import Depends
from loguru import logger

from capturerrbackend.app.dao.capture_dao import CaptureDAO
from capturerrbackend.app.dao.tag_dao import TagDAO
from capturerrbackend.app.models.capture_model import CaptureModel
from capturerrbackend.app.schemas.requests.captures import CaptureRequest
from capturerrbackend.app.schemas.responses.captures import CaptureResponse
from capturerrbackend.app.schemas.user import UserRequest
from capturerrbackend.app.services.users import get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[CaptureResponse])
async def get_capture_models(
    current_user: Annotated[UserRequest, Depends(get_current_active_user)],
    capture_dao: CaptureDAO = Depends(),
    limit: int = 10,
    offset: int = 0,
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
    current_user: Annotated[UserRequest, Depends(get_current_active_user)],
    new_capture_object: CaptureRequest,
    capture_dao: CaptureDAO = Depends(),
) -> CaptureResponse:
    """
    Creates capture model in the database.

    :param new_capture_object: new capture model item.
    :param capture_dao: DAO for capture models.
    """

    await capture_dao.create_capture_model(
        text=new_capture_object.text,
        user=current_user,
    )
    new_capture = await capture_dao.filter(text=new_capture_object.text)
    return new_capture[0]  # type: ignore


@router.put("/{capture_id}/{tag_name}", response_model=CaptureResponse)
async def add_tag_to_capture(
    capture_id: int,
    tag_name: str,
    capture_dao: CaptureDAO = Depends(),
    tag_dao: TagDAO = Depends(),
) -> CaptureResponse:
    capture = await capture_dao.get_by_id(id=capture_id)
    tag = await tag_dao.get_or_create(name=tag_name)
    capture.tags.append(tag)  # type: ignore

    return capture  # type: ignore
