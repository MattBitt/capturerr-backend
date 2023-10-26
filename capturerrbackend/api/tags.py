from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, status

from capturerrbackend.api.custom_error_route_handler import CustomErrorRouteHandler
from capturerrbackend.app.infrastructure.dependencies import (
    get_current_active_super_user,
    get_current_active_user,
    tag_command_usecase,
    tag_query_usecase,
)
from capturerrbackend.app.usecase.tag import (
    TagCommandUseCase,
    TagCreateModel,
    TagQueryUseCase,
    TagReadModel,
    TagUpdateModel,
)
from capturerrbackend.app.usecase.user import UserReadModel

router = APIRouter(route_class=CustomErrorRouteHandler)

##### Super User Routes #####


@router.get(
    "/tags",
    response_model=List[TagReadModel],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_active_super_user)],
)
async def get_tags(
    tag_query_usecase: TagQueryUseCase = Depends(tag_query_usecase),
) -> List[TagReadModel]:
    """Get a list of tags."""
    return tag_query_usecase.fetch_tags()


@router.delete(
    "/tags/{tag_id}",
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(get_current_active_super_user)],
)
async def delete_a_tag(
    tag_id: str,
    tag_command_usecase: TagCommandUseCase = Depends(tag_command_usecase),
) -> None:
    """Delete a tag."""
    tag_command_usecase.delete_tag_by_id(tag_id)


### Query Routes ###
@router.get(
    "/me/tags",
    response_model=List[TagReadModel],
    status_code=status.HTTP_200_OK,
)
async def get_my_tags(
    current_user: UserReadModel = Depends(get_current_active_user),
    tag_query_usecase: TagQueryUseCase = Depends(tag_query_usecase),
) -> List[TagReadModel]:
    """Get a list of tags."""
    return tag_query_usecase.fetch_tags_for_user(current_user.id)


@router.get(
    "/me/tags/{tag_id}",
    response_model=TagReadModel,
    status_code=status.HTTP_200_OK,
)
async def get_my_tag(
    tag_id: str,
    current_user: Annotated[UserReadModel, Depends(get_current_active_user)],
    tag_query_usecase: Annotated[
        TagQueryUseCase,
        Depends(tag_query_usecase),
    ],
) -> Optional[TagReadModel]:
    """Get a tag."""
    cap = tag_query_usecase.fetch_tag_by_id(tag_id)
    if cap.user_id != current_user.id:
        return None
    return cap


### Command Routes ###
@router.post(
    "/me/tags",
    response_model=TagReadModel,
    status_code=status.HTTP_201_CREATED,
)
def create_tag(
    data: TagCreateModel,
    current_user: Annotated[UserReadModel, Depends(get_current_active_user)],
    tag_command_usecase: Annotated[
        TagCommandUseCase,
        Depends(tag_command_usecase),
    ],
) -> Optional[TagReadModel]:
    """Get the user and create a tag."""
    data.user_id = current_user.id
    tag = tag_command_usecase.create_tag(data)
    return tag


@router.put(
    "/me/tags/{tag_id}",
    response_model=TagReadModel,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_my_tag(
    tag_id: str,
    data: TagUpdateModel,
    current_user: Annotated[UserReadModel, Depends(get_current_active_user)],
    tag_command_usecase: Annotated[
        TagCommandUseCase,
        Depends(tag_command_usecase),
    ],
    tag_query_usecase: Annotated[
        TagQueryUseCase,
        Depends(tag_query_usecase),
    ],
) -> Optional[TagReadModel]:
    """Update a tag."""
    tag = tag_query_usecase.fetch_tag_by_id(tag_id)
    if tag.user_id != current_user.id:
        return None
    return tag_command_usecase.update_tag(tag_id, data)


@router.delete(
    "/me/tags/{tag_id}",
    status_code=status.HTTP_202_ACCEPTED,
)
async def delete_my_tag(
    tag_id: str,
    current_user: Annotated[UserReadModel, Depends(get_current_active_user)],
    tag_command_usecase: Annotated[
        TagCommandUseCase,
        Depends(tag_command_usecase),
    ],
    tag_query_usecase: Annotated[
        TagQueryUseCase,
        Depends(tag_query_usecase),
    ],
) -> None:
    """Delete a tag."""
    tag = tag_query_usecase.fetch_tag_by_id(tag_id)
    if tag.user_id != current_user.id:
        return None
    tag_command_usecase.delete_tag_by_id(tag_id)


# @router.post(
#     "/tags",
#     response_model=TagReadModel,
#     status_code=status.HTTP_201_CREATED,
# )
# def create_tag(
#     data: TagCreateModel,
#     current_user: Annotated[UserReadModel, Depends(get_current_active_user)],
#     user_query_usecase: Annotated[UserQueryUseCase, Depends(user_query_usecase)],
#     tag_command_usecase: Annotated[TagCommandUseCase, Depends(tag_command_usecase)],
# ) -> Optional[TagReadModel]:
#     """Get the user and create a tag."""
#     data.user_id = current_user.id
#     tag = tag_command_usecase.create_tag(data)
#     return tag


# @router.get(
#     "/tags",
#     response_model=List[TagReadModel],
#     status_code=status.HTTP_200_OK,
# )
# #
# async def get_tags(
#     tag_query_usecase: TagQueryUseCase = Depends(tag_query_usecase),
# ) -> List[TagReadModel]:
#     """Get a list of tags."""
#     return tag_query_usecase.fetch_tags()


# @router.get(
#     "/tags/{tag_id}",
#     response_model=TagReadModel,
#     status_code=status.HTTP_200_OK,
# )
# async def get_tag(
#     tag_id: str,
#     tag_query_usecase: TagQueryUseCase = Depends(tag_query_usecase),
# ) -> Optional[TagReadModel]:
#     """Get a tag."""
#     return tag_query_usecase.fetch_tag_by_id(tag_id)


# @router.put(
#     "/tags/{tag_id}",
#     response_model=TagReadModel,
#     status_code=status.HTTP_202_ACCEPTED,
# )
# async def update_tag(
#     tag_id: str,
#     data: TagUpdateModel,
#     tag_command_usecase: TagCommandUseCase = Depends(tag_command_usecase),
# ) -> Optional[TagReadModel]:
#     """Update a tag."""
#     return tag_command_usecase.update_tag(tag_id, data)


# @router.delete(
#     "/tags/{tag_id}",
#     status_code=status.HTTP_202_ACCEPTED,
# )
# async def delete_tag(
#     tag_id: str,
#     tag_command_usecase: TagCommandUseCase = Depends(tag_command_usecase),
# ) -> None:
#     """Delete a tag."""
#     tag_command_usecase.delete_tag_by_id(tag_id)
