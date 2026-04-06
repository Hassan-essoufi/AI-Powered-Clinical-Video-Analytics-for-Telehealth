from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.dependencies import get_evm_service

router = APIRouter(prefix="/evm", tags=["EVM"])


class EVMConfigUpdate(BaseModel):
    alpha: Optional[float] = Field(default=None, gt=0)
    freq_min: Optional[float] = Field(default=None, gt=0)
    freq_max: Optional[float] = Field(default=None, gt=0)
    fps: Optional[int] = Field(default=None, gt=0)
    pyr_levels: Optional[int] = Field(default=None, ge=1)


@router.get("/status")
async def evm_status():
    return {
        "status": "ok",
        "evm": get_evm_service().status(),
    }


@router.post("/enable")
async def enable_evm():
    return {
        "status": "ok",
        "evm": get_evm_service().enable(),
    }


@router.post("/disable")
async def disable_evm():
    return {
        "status": "ok",
        "evm": get_evm_service().disable(),
    }


@router.patch("/config")
async def update_evm_config(payload: EVMConfigUpdate):
    try:
        return {
            "status": "ok",
            "evm": get_evm_service().update_config(
                alpha=payload.alpha,
                freq_min=payload.freq_min,
                freq_max=payload.freq_max,
                fps=payload.fps,
                pyr_levels=payload.pyr_levels,
            ),
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
