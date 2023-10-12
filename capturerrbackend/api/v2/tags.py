from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from capturerrbackend.app.schemas.tag import TagPayload, TagSchema
from capturerrbackend.app.services.tags import TagService
from capturerrbackend.core.db.dependencies import get_db_session

router = APIRouter(prefix="/v2", tags=["v2"])


@router.post("/tags", status_code=status.HTTP_201_CREATED)
async def create_tag(
    data: TagPayload,
    db_session: AsyncSession = Depends(get_db_session),
) -> Any:
    service = TagService(db_session)
    try:
        await service.add(**data.model_dump())
        return await service.get_all()
    except Exception as e:
        logger.error(f"Error creating tag: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating tag",
        )


@router.get("/tags", response_model=TagSchema, status_code=status.HTTP_200_OK)
async def get_tags(
    db_session: AsyncSession = Depends(get_db_session),
) -> list[TagSchema]:
    service = TagService(db_session)
    tags = await service.get_all()
    if len(tags) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag does not exist",
        )
    return tags


@router.get(
    "/tags/name/{name}",
    response_model=TagSchema,
    status_code=status.HTTP_200_OK,
)
async def get_tag_by_name(
    name: str,
    db_session: AsyncSession = Depends(get_db_session),
) -> TagSchema:
    service = TagService(db_session)
    tags = await service.get_tag_by_name(name=name)
    return tags


@router.get("/tags/{pk}", status_code=status.HTTP_200_OK)
async def get_tag(
    pk: int,
    db_session: AsyncSession = Depends(get_db_session),
) -> TagSchema:
    service = TagService(db_session)
    tag = service.get_by_id(pk)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag does not exist",
        )
    return tag
