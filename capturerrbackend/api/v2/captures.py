from fastapi import APIRouter, Depends, HTTPException, status, Body
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any

# from capturerrbackend.app.repos.tags import TagRepository
from capturerrbackend.app.schemas.capture import CapturePayload, CaptureSchema
from capturerrbackend.app.services.captures import CaptureService
from capturerrbackend.app.services.tags import TagService
from capturerrbackend.core.db.dependencies import get_db_session

router = APIRouter(prefix="/v2", tags=["v2"])


@router.post("/captures", status_code=status.HTTP_201_CREATED)
async def create_capture(
    data: dict[str, str] = Body(..., embed=True),
    db_session: AsyncSession = Depends(get_db_session),
) -> CaptureSchema:
    # data_dict = data.model_dump()

    cap_service = CaptureService(db_session)
    tag_service = TagService(db_session)

    tags = data.pop("tags")
    tags_list = []
    for tag in tags:
        t = await tag_service.get_or_create(tag)
        tags_list.append(t)

    try:
        await cap_service.add(**data)
        return await cap_service.get_by_text(data["text"])
    except Exception as e:
        logger.error(f"Error creating capture: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating capture",
        )


@router.get("/captures", response_model=CaptureSchema, status_code=status.HTTP_200_OK)
async def get_captures(
    db_session: AsyncSession = Depends(get_db_session),
) -> list[CaptureSchema]:
    service = CaptureService(db_session)
    captures = await service.get_all()
    if len(captures) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Capture does not exist",
        )
    return captures


@router.get("/captures/{pk}", status_code=status.HTTP_200_OK)
async def get_capture(
    pk: int,
    db_session: AsyncSession = Depends(get_db_session),
) -> CaptureSchema:
    service = CaptureService(db_session)
    capture = service.get_by_id(pk)
    if capture is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Capture does not exist",
        )
    return capture
