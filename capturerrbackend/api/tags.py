from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, status

from capturerrbackend.api.custom_error_route_handler import CustomErrorRouteHandler
from capturerrbackend.app.infrastructure.dependencies import (
    get_current_active_user,
    tag_command_usecase,
    tag_query_usecase,
    user_query_usecase,
)
from capturerrbackend.app.usecase.tag import (
    TagCommandUseCase,
    TagCreateModel,
    TagQueryUseCase,
    TagReadModel,
    TagUpdateModel,
)
from capturerrbackend.app.usecase.user import UserQueryUseCase, UserReadModel

router = APIRouter(route_class=CustomErrorRouteHandler)


@router.post(
    "/tags",
    response_model=TagReadModel,
    status_code=status.HTTP_201_CREATED,
)
def create_tag(
    data: TagCreateModel,
    current_user: Annotated[UserReadModel, Depends(get_current_active_user)],
    user_query_usecase: Annotated[UserQueryUseCase, Depends(user_query_usecase)],
    tag_command_usecase: Annotated[TagCommandUseCase, Depends(tag_command_usecase)],
) -> Optional[TagReadModel]:
    """Get the user and create a tag."""
    # user = user_query_usecase.fetch_user_by_id(current_user.id)
    data.user_id = current_user.id
    tag = tag_command_usecase.create_tag(data)
    return tag


@router.get(
    "/tags",
    response_model=List[TagReadModel],
    status_code=status.HTTP_200_OK,
)
#
async def get_tags(
    tag_query_usecase: TagQueryUseCase = Depends(tag_query_usecase),
) -> List[TagReadModel]:
    """Get a list of tags."""
    return tag_query_usecase.fetch_tags()


@router.get(
    "/tags/{tag_id}",
    response_model=TagReadModel,
    status_code=status.HTTP_200_OK,
)
async def get_tag(
    tag_id: str,
    tag_query_usecase: TagQueryUseCase = Depends(tag_query_usecase),
) -> Optional[TagReadModel]:
    """Get a tag."""
    return tag_query_usecase.fetch_tag_by_id(tag_id)


@router.put(
    "/tags/{tag_id}",
    response_model=TagReadModel,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_tag(
    tag_id: str,
    data: TagUpdateModel,
    tag_command_usecase: TagCommandUseCase = Depends(tag_command_usecase),
) -> Optional[TagReadModel]:
    """Update a tag."""
    return tag_command_usecase.update_tag(tag_id, data)


@router.delete(
    "/tags/{tag_id}",
    status_code=status.HTTP_202_ACCEPTED,
)
async def delete_tag(
    tag_id: str,
    tag_command_usecase: TagCommandUseCase = Depends(tag_command_usecase),
) -> None:
    """Delete a tag."""
    tag_command_usecase.delete_tag_by_id(tag_id)
