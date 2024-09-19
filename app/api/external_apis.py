import logging
import asyncio
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.factory import SessionLocal
from app.factory import get_db
from app.models.external import Api1, Api2, Api3
from fastapi import APIRouter, Depends, HTTPException

logger = logging.getLogger(__name__)

class PolicyResponse(BaseModel):
    memberid: int
    oop_max: int
    remaining_oop_max: int
    copay: int

router = APIRouter(
    prefix="/api/v1",
    tags=["external"]
)
# simple external endpoint that queries it's own DB table to pull policy data 
@router.get("/api1", response_model=PolicyResponse)
async def getCurrentPolicy(memberId: int, db: Session = Depends(get_db)):
    member = db.query(Api1).filter(Api1.memberid == memberId).first()
    if member is None:
        raise HTTPException(status_code=404, detail="User not found")
    return member
# simple external endpoint that queries it's own DB table to pull policy data 
@router.get("/api2", response_model=PolicyResponse)
async def getCurrentPolicy1(memberId: int, db: Session = Depends(get_db)):
    member = db.query(Api2).filter(Api2.memberid == memberId).first()
    if member is None:
        raise HTTPException(status_code=404, detail="User not found")
    return member

# simple external endpoint that queries it's own DB table to pull policy data 
@router.get("/api3", response_model=PolicyResponse)
async def getCurrentPolicy2(memberId: int, db: Session = Depends(get_db)):
    member = db.query(Api3).filter(Api3.memberid == memberId).first()
    if member is None:
        raise HTTPException(status_code=404, detail="User not found")
    return member

## endpoint with sleep at 20 seconds that is past our max 10 seconds. Should not get added to list
@router.get("/apiTimeout", response_model=PolicyResponse)
async def timeOutEndpoint(memberId: int, db: Session = Depends(get_db)):
    member = db.query(Api1).filter(Api1.memberid == memberId).first()
    if member is None:
        raise HTTPException(status_code=404, detail="User not found")
    await asyncio.sleep(20)
    member.oop_max = 9999999
    return member
## endpoint that just throws a 404 to simulate a failed external call
@router.get("/exceptionEndpoint", response_model=PolicyResponse)
async def throwException404(memberId: int, db: Session = Depends(get_db)):
    raise HTTPException(status_code=404, detail="404 exception")