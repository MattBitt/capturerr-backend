# 💥💥💥💥💥 This should be used as a go-by for the custom response class.


# from typing import Generic, TypeVar, List, Optional
# from pydantic import Field, AnyHttpUrl

# # from pydantic.BaseModel import GenericModel
# from pydantic import BaseModel
# from fastapi import Query
# from sqlalchemy import select, func, Select
# from sqlalchemy.orm import Session

# M = TypeVar("M")


# class PaginatedResponse(BaseModel, Generic[M]):
#     count: int = Field(description="Number of items returned in the response")
#     items: List[M] = Field(description="List of items
# returned in a paginated response")
#     next_page: Optional[AnyHttpUrl] = Field(
#         None, description="url of the next page if it exists"
#     )
#     previous_page: Optional[AnyHttpUrl] = Field(
#         None, description="url of the previous page if it exists"
#     )


# class PaginatedParams:
#     def __init__(self, page: int = Query(1, ge=1), per_page: int = Query(100, ge=0)):
#         self.limit = per_page * page
#         self.offset = (page - 1) * per_page


# ...


# def paginate(session: Session, query: Select, limit: int, offset: int) -> dict:
#     return {
#         "count": session.scalar(select(func.count()).select_from(query.subquery())),
#         "items": [
#             capture for capture in session.scalars(query.limit(limit).offset(offset))
#         ],
#     }
