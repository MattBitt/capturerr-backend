import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from capturerrbackend.app.dao.bar_dao import BarDAO
from capturerrbackend.app.dao.foo_dao import FooDAO
from capturerrbackend.core.factory import create_fake_bar, create_fake_foo


@pytest.mark.anyio
async def test_foobar(
    fastapi_app: FastAPI,
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    dao1 = FooDAO(db_session)
    test_name = create_fake_foo()["name"]
    await dao1.create_foo_model(name=test_name)
    test_name = create_fake_foo()["name"]
    await dao1.create_foo_model(name=test_name)
    await db_session.commit()
    foos = await dao1.get_all_foos(limit=10, offset=0)
    assert len(foos) == 2

    dao2 = BarDAO(db_session)
    test_title = create_fake_bar()["title"]
    await dao2.create_bar_model(title=test_title)
    test_title = create_fake_bar()["title"]
    await dao2.create_bar_model(title=test_title)
    await db_session.commit()
    bars = await dao2.get_all_bars(limit=10, offset=0)
    assert len(bars) == 2
