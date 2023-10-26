from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, status

from capturerrbackend.api.custom_error_route_handler import CustomErrorRouteHandler
from capturerrbackend.app.infrastructure.dependencies import (
    capture_command_usecase,
    capture_query_usecase,
    get_current_active_super_user,
    get_current_active_user,
    tag_command_usecase,
    tag_query_usecase,
)
from capturerrbackend.app.usecase.capture import (
    CaptureCommandUseCase,
    CaptureCreateModel,
    CaptureQueryUseCase,
    CaptureReadModel,
    CaptureUpdateModel,
)
from capturerrbackend.app.usecase.tag import (
    TagCommandUseCase,
    TagCreateModel,
    TagQueryUseCase,
)
from capturerrbackend.app.usecase.user import UserReadModel

router = APIRouter(route_class=CustomErrorRouteHandler)


##### Super User Routes #####


@router.get(
    "/captures",
    response_model=List[CaptureReadModel],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_active_super_user)],
)
async def get_captures(
    capture_query_usecase: Annotated[
        CaptureQueryUseCase,
        Depends(capture_query_usecase),
    ],
    tag_query_usecase: Annotated[
        TagQueryUseCase,
        Depends(tag_query_usecase),
    ],
) -> List[CaptureReadModel]:
    """Get a list of captures."""
    caps = capture_query_usecase.fetch_captures()

    for cap in caps:
        tags = tag_query_usecase.fetch_tags_for_capture(cap.id)
        cap.tags = [tag for tag in tags]

    return caps


@router.delete(
    "/captures/{capture_id}",
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(get_current_active_super_user)],
)
async def delete_a_capture(
    capture_id: str,
    capture_command_usecase: CaptureCommandUseCase = Depends(capture_command_usecase),
) -> None:
    """Delete a capture."""
    capture_command_usecase.delete_capture_by_id(capture_id)


### User Routes ###
### They should all start with /me/ and need the current user id ###


### Query Routes ###
@router.get(
    "/me/captures",
    response_model=List[CaptureReadModel],
    status_code=status.HTTP_200_OK,
)
async def get_my_captures(
    current_user: Annotated[UserReadModel, Depends(get_current_active_user)],
    tag_query_usecase: Annotated[
        TagQueryUseCase,
        Depends(tag_query_usecase),
    ],
    capture_query_usecase: Annotated[
        CaptureQueryUseCase,
        Depends(capture_query_usecase),
    ],
) -> List[CaptureReadModel]:
    """Get a list of captures."""
    caps = capture_query_usecase.fetch_captures_for_user(current_user.id)

    for cap in caps:
        tags = tag_query_usecase.fetch_tags_for_capture(cap.id)
        cap.tags = [tag for tag in tags]

    return caps


@router.get(
    "/me/captures/{capture_id}",
    response_model=CaptureReadModel,
    status_code=status.HTTP_200_OK,
)
async def get_my_capture(
    capture_id: str,
    current_user: Annotated[UserReadModel, Depends(get_current_active_user)],
    capture_query_usecase: Annotated[
        CaptureQueryUseCase,
        Depends(capture_query_usecase),
    ],
) -> Optional[CaptureReadModel]:
    """Get a capture."""
    cap = capture_query_usecase.fetch_capture_by_id(capture_id)
    if cap.user_id != current_user.id:
        return None
    return cap


### Command Routes ###
@router.post(
    "/me/captures",
    response_model=CaptureReadModel,
    status_code=status.HTTP_201_CREATED,
)
def create_capture(
    data: CaptureCreateModel,
    current_user: Annotated[UserReadModel, Depends(get_current_active_user)],
    capture_command_usecase: Annotated[
        CaptureCommandUseCase,
        Depends(capture_command_usecase),
    ],
) -> Optional[CaptureReadModel]:
    """Get the user and create a capture."""
    data.user_id = current_user.id
    capture = capture_command_usecase.create_capture(data)
    return capture


@router.put(
    "/me/captures/{capture_id}",
    response_model=CaptureReadModel,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_my_capture(
    capture_id: str,
    data: CaptureUpdateModel,
    current_user: Annotated[UserReadModel, Depends(get_current_active_user)],
    capture_command_usecase: Annotated[
        CaptureCommandUseCase,
        Depends(capture_command_usecase),
    ],
    capture_query_usecase: Annotated[
        CaptureQueryUseCase,
        Depends(capture_query_usecase),
    ],
) -> Optional[CaptureReadModel]:
    """Update a capture."""
    cap = capture_query_usecase.fetch_capture_by_id(capture_id)
    if cap.user_id != current_user.id:
        return None
    return capture_command_usecase.update_capture(capture_id, data)


@router.delete(
    "/me/captures/{capture_id}",
    status_code=status.HTTP_202_ACCEPTED,
)
async def delete_capture(
    capture_id: str,
    current_user: Annotated[UserReadModel, Depends(get_current_active_user)],
    capture_command_usecase: Annotated[
        CaptureCommandUseCase,
        Depends(capture_command_usecase),
    ],
    capture_query_usecase: Annotated[
        CaptureQueryUseCase,
        Depends(capture_query_usecase),
    ],
) -> None:
    """Delete a capture."""
    cap = capture_query_usecase.fetch_capture_by_id(capture_id)
    if cap.user_id != current_user.id:
        return None
    capture_command_usecase.delete_capture_by_id(capture_id)


@router.post(
    "/me/captures/{capture_id}/tags",
    response_model=CaptureReadModel,
    status_code=status.HTTP_201_CREATED,
)
def add_tag_to_capture(
    capture_id: str,
    data: TagCreateModel,
    current_user: Annotated[UserReadModel, Depends(get_current_active_user)],
    capture_command_usecase: Annotated[
        CaptureCommandUseCase,
        Depends(capture_command_usecase),
    ],
    tag_command_usecase: Annotated[
        TagCommandUseCase,
        Depends(tag_command_usecase),
    ],
    tag_query_usecase: Annotated[
        TagQueryUseCase,
        Depends(tag_query_usecase),
    ],
) -> Optional[CaptureReadModel]:
    """Get the user and create a capture."""
    data.user_id = current_user.id
    existing_tag = tag_command_usecase.get_or_create_tag(data)
    capture = capture_command_usecase.add_tag_to_capture(capture_id, existing_tag.id)
    return capture
