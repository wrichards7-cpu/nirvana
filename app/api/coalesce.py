import logging
import os
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker, Session
from app.factory import SessionLocal
from app.models.members import Members
from app.factory import get_db
import httpx
from enum import Enum
from typing import Type, Optional, List
from app.api.external_apis import PolicyResponse
import asyncio
import async_timeout
from urllib.error import HTTPError
import time
import json


from fastapi import APIRouter, Depends

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1",
    tags=["Members"]
)

# right now we only support sorting by value but we could extend this to sort
# by a certain frequency that we see a certain value amoung responses from the APIs
class SortType(str, Enum):
    frequency = 'frequency'
    value = 'value'

class SortDirection(str, Enum):
    desc = 'DESC'
    asc = 'ASC'

class Columns(str, Enum):
    oop_max = 'oop_max'
    remaining_oop_max = 'remaining_oop_max'
    copay = 'copay'

class SortBody(BaseModel):
    sort_type: SortType
    sort_direction: SortDirection

class ColumnSortBody(BaseModel):
    column: Columns
    sort_body: SortBody

class PostAlgoBody(BaseModel):
    primary: ColumnSortBody
    secondary: ColumnSortBody
    third: ColumnSortBody

class RequestBody(BaseModel):
    memberId: int
    postAlgoBody: PostAlgoBody
    urlList: Optional[List[str]] = [
                "http://0.0.0.0:5007/api/v1/api1?memberId={}",
                "http://0.0.0.0:5007/api/v1/api2?memberId={}",
                "http://0.0.0.0:5007/api/v1/api3?memberId={}",
            ]


# httpx library that returns coroutines. Timeoutset to 10 seconds for each request. 
async def call_url(memberId, url, client):
    url = url.format(memberId)
    res = await client.get(url, timeout=10)
    if res.status_code != 200:
        raise Exception('Got back a non 200 error from ' + url + ' with status code ' + str(res.status_code))
    return res.json()
       
columnToId = {
    "oop_max": 0,
    "remaining_oop_max": 1,
    "copay": 2
}

@router.post("/coalesce", response_model=PolicyResponse)             ## hacky but i added a default list of URLs to hit for test bc of time limit i had
async def getCurrentPolicy(request: RequestBody):
    returned_list = []
    async with httpx.AsyncClient() as client:
        tasks = [call_url(request.memberId, url, client) for url in request.urlList]
        # spin off all tasks in a asyn manner allowing for exceptions and timeouts ( timeouts will throw an exception ) to happen
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        logger.info('Values returned in gather = ' + str(responses))
        returned_list = []
        for i in range(len(responses)):
            # filter out exceptions 
            if not isinstance(responses[i], Exception):
                returned_list.append([responses[i]['oop_max'], responses[i]['remaining_oop_max'], responses[i]['copay']])

        logger.info('Values from list that are not exceptions = ' + str(returned_list))
        # If none of the API returned anything return error
        if not returned_list:
            raise HTTPError("None of the APIs endpoint returned a value")
        # Only one api returned so no need to sort
        if len(returned_list) == 1:
            return PolicyResponse(memberid=request.memberId, oop_max=returned_list[0], remaining_oop_max=returned_list[1], copay=returned_list[2])
        response = coalescing(returned_list, request.postAlgoBody)
        return PolicyResponse(memberid=request.memberId, oop_max=response[0], remaining_oop_max=response[1], copay=response[2])


columnToId = {
    "oop_max": 0,
    "remaining_oop_max": 1,
    "copay": 2
}


def coalescing(input_list, coalesAlgo):
    match (coalesAlgo.primary.sort_body.sort_direction, coalesAlgo.secondary.sort_body.sort_direction, coalesAlgo.third.sort_body.sort_direction):
        case ('DESC', 'ASC', 'ASC'):
            return [x for x in sorted(input_list, key=lambda x:
                    (-x[columnToId[coalesAlgo.primary.column]],
                         x[columnToId[coalesAlgo.secondary.column]], 
                            x[columnToId[coalesAlgo.third.column]])
                    )][0]
        case ('DESC', 'DESC', 'ASC'):
            return [x for x in sorted(input_list, key=lambda x:
                    (-x[columnToId[coalesAlgo.primary.column]], 
                        -x[columnToId[coalesAlgo.secondary.column]], 
                            x[columnToId[coalesAlgo.third.column]])
                    )][0]
        case ('DESC', 'DESC', 'DESC'):
            return [x for x in sorted(input_list, key=lambda x:
                    (-x[columnToId[coalesAlgo.primary.column]], 
                        -x[columnToId[coalesAlgo.secondary.column]],
                         -x[columnToId[coalesAlgo.third.column]])
                    )][0]
        case ('DESC', 'ASC', 'DESC'):
            return [x for x in sorted(input_list, key=lambda x:

                    (-(x[columnToId[coalesAlgo.primary.column]]), 
                        x[columnToId[coalesAlgo.secondary.column]], 
                         -x[columnToId[coalesAlgo.third.column]])
                    )][0]
        case ('ASC', 'ASC', 'ASC'):
            return [x for x in sorted(input_list, key=lambda x:
                    (x[columnToId[coalesAlgo.primary.column]], 
                        x[columnToId[coalesAlgo.secondary.column]],
                         x[columnToId[coalesAlgo.third.column]])
                    )][0]
        case ('ASC', 'ASC', 'DESC'):
            return [x for x in sorted(input_list, key=lambda x:
                    (x[columnToId[coalesAlgo.primary.column]], 
                        x[columnToId[coalesAlgo.secondary.column]], 
                        -x[columnToId[coalesAlgo.third.column]])
                    )][0]
        case ('ASC', 'DESC', 'DESC'):
            return [x for x in sorted(input_list, key=lambda x:
                    (x[columnToId[coalesAlgo.primary.column]], 
                        -x[columnToId[coalesAlgo.secondary.column]], 
                        -x[columnToId[coalesAlgo.third.column]])
                    )][0]
        case ('ASC', 'DESC', 'ASC'):
            return [x for x in sorted(input_list, key=lambda x:
                    (x[columnToId[coalesAlgo.primary.column]], 
                        -x[columnToId[coalesAlgo.secondary.column]], 
                            x[columnToId[coalesAlgo.third.column]])
                    )][0]

