from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, status

from capturerrbackend.api.custom_error_route_handler import CustomErrorRouteHandler
from capturerrbackend.app.infrastructure.dependencies import (
    capture_command_usecase,
    capture_query_usecase,
    get_current_active_super_user,
    get_current_active_user,
    user_query_usecase,
)
from capturerrbackend.app.usecase.capture import (
    CaptureCommandUseCase,
    CaptureCreateModel,
    CaptureQueryUseCase,
    CaptureReadModel,
    CaptureUpdateModel,
)
from capturerrbackend.app.usecase.user import UserQueryUseCase, UserReadModel

router = APIRouter(route_class=CustomErrorRouteHandler)


@router.post(
    "/me/captures",
    response_model=CaptureReadModel,
    status_code=status.HTTP_201_CREATED,
)
def create_capture(
    data: CaptureCreateModel,
    current_user: Annotated[UserReadModel, Depends(get_current_active_user)],
    user_query_usecase: Annotated[UserQueryUseCase, Depends(user_query_usecase)],
    capture_command_usecase: Annotated[
        CaptureCommandUseCase, Depends(capture_command_usecase)
    ],
) -> Optional[CaptureReadModel]:
    """Get the user and create a capture."""
    # user = user_query_usecase.fetch_user_by_id(current_user.id)
    data.user_id = current_user.id
    capture = capture_command_usecase.create_capture(data)
    return capture


@router.get(
    "/captures",
    response_model=List[CaptureReadModel],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_active_super_user)],
)
#
async def get_captures(
    capture_query_usecase: CaptureQueryUseCase = Depends(capture_query_usecase),
) -> List[CaptureReadModel]:
    """Get a list of captures."""
    return capture_query_usecase.fetch_captures()


@router.get(
    "/me/captures",
    response_model=List[CaptureReadModel],
    status_code=status.HTTP_200_OK,
)
#
async def get_my_captures(
    current_user: UserReadModel = Depends(get_current_active_user),
    capture_query_usecase: CaptureQueryUseCase = Depends(capture_query_usecase),
) -> List[CaptureReadModel]:
    """Get a list of captures."""
    return capture_query_usecase.fetch_captures_for_user(current_user.id)


@router.get(
    "/me/captures/{capture_id}",
    response_model=CaptureReadModel,
    status_code=status.HTTP_200_OK,
)
async def get_capture(
    capture_id: str,
    current_user: Annotated[UserReadModel, Depends(get_current_active_user)],
    capture_query_usecase: Annotated[
        CaptureQueryUseCase, Depends(capture_query_usecase)
    ],
) -> Optional[CaptureReadModel]:
    """Get a capture."""
    cap = capture_query_usecase.fetch_capture_by_id(capture_id)
    if cap.user_id != current_user.id:
        if current_user.is_superuser is False:
            return None
    return cap


# async def get_captures_for_user(
#     capture_id: str,
#     capture_query_usecase: CaptureQueryUseCase = Depends(capture_query_usecase),
# ) -> Optional[CaptureReadModel]:
#     """Get a capture."""
#     return capture_query_usecase.fetch_capture_by_id(capture_id)


@router.put(
    "/me/captures/{capture_id}",
    response_model=CaptureReadModel,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_capture(
    capture_id: str,
    data: CaptureUpdateModel,
    capture_command_usecase: CaptureCommandUseCase = Depends(capture_command_usecase),
) -> Optional[CaptureReadModel]:
    """Update a capture."""
    return capture_command_usecase.update_capture(capture_id, data)


@router.delete(
    "/me/captures/{capture_id}",
    status_code=status.HTTP_202_ACCEPTED,
)
async def delete_capture(
    capture_id: str,
    capture_command_usecase: CaptureCommandUseCase = Depends(capture_command_usecase),
) -> None:
    """Delete a capture."""
    capture_command_usecase.delete_capture_by_id(capture_id)
