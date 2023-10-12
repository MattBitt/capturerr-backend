# from typing import List

# from fastapi import APIRouter
# from fastapi.param_functions import Depends

# from capturerrbackend.app.dao.tag_dao import TagDAO
# from capturerrbackend.app.models.tag import Tag as TagModel

# # from capturerrbackend.app.schemas.tag import Tag
# from capturerrbackend.app.schemas.responses.tags import TagResponse

# router = APIRouter()


# @router.get("/", response_model=List[TagResponse])
# async def get_tag_models(
#     limit: int = 10,
#     offset: int = 0,
#     tag_dao: TagDAO = Depends(),
# ) -> List[TagModel]:
#     """
#     Retrieve all tag objects from the database.

#     :param limit: limit of tag objects, defaults to 10.
#     :param offset: offset of tag objects, defaults to 0.
#     :param tag_dao: DAO for tag models.
#     :return: list of tag objects from database.
#     """
#     return await tag_dao.get_all_tags(limit=limit, offset=offset)


# @router.put("/")
# async def create_tag_model(
#     new_tag_object: TagRequest,
#     tag_dao: TagDAO = Depends(),
# ) -> None:
#     """
#     Creates tag model in the database.

#     :param new_tag_object: new tag model item.
#     :param tag_dao: DAO for tag models.
#     """
#     await tag_dao.create_tag_model(title=new_tag_object.title)
