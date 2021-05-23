import pytest

from bot.farm import farm_bot


@pytest.mark.asyncio
async def test_smoke():
    res = await farm_bot()
    # todo impl
    assert True
