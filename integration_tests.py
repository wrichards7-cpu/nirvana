import sys
from app.api.external_apis import PolicyResponse
import requests

def checkSortByPrimary():

    url = 'http://0.0.0.0:5007/api/v1/coalesce'
    myobj = {
        "memberId": 1,
        "postAlgoBody": {
            "primary": {
                "column": "oop_max",
                "sort_body": {
                    "sort_direction": "DESC",
                    "sort_type": "value"
                }
            },
            "secondary": {
                "column": "remaining_oop_max",
                "sort_body": {
                    "sort_direction": "ASC",
                    "sort_type": "value"
                }
            },
            "third": {
                "column": "copay",
                "sort_body": {
                    "sort_direction": "DESC",
                    "sort_type": "value"
                }
            }
        }
    }
    #validate response serializes to PolicyResponse
    policy = PolicyResponse(**requests.post(
        url, json = myobj
    ).json())
    assert policy.oop_max == 20000
    assert policy.remaining_oop_max == 9000
    assert policy.copay == 50000

def checkSortBySecondary():

    url = 'http://0.0.0.0:5007/api/v1/coalesce'
    myobj = {
        "memberId": 2,
        "postAlgoBody": {
            "primary": {
                "column": "oop_max",
                "sort_body": {
                    "sort_direction": "DESC",
                    "sort_type": "value"
                }
            },
            "secondary": {
                "column": "remaining_oop_max",
                "sort_body": {
                    "sort_direction": "ASC",
                    "sort_type": "value"
                }
            },
            "third": {
                "column": "copay",
                "sort_body": {
                    "sort_direction": "DESC",
                    "sort_type": "value"
                }
            }
        }
    }
    #validate response serializes to PolicyResponse
    policy = PolicyResponse(**requests.post(
        url, json = myobj
    ).json())

    assert policy.oop_max == 80000
    assert policy.remaining_oop_max == 6000
    assert policy.copay == 5000

def checkSortByThird():

    url = 'http://0.0.0.0:5007/api/v1/coalesce'
    myobj = {
        "memberId": 3,
        "postAlgoBody": {
            "primary": {
                "column": "oop_max",
                "sort_body": {
                    "sort_direction": "DESC",
                    "sort_type": "value"
                }
            },
            "secondary": {
                "column": "remaining_oop_max",
                "sort_body": {
                    "sort_direction": "ASC",
                    "sort_type": "value"
                }
            },
            "third": {
                "column": "copay",
                "sort_body": {
                    "sort_direction": "DESC",
                    "sort_type": "value"
                }
            }
        }
    }
    #validate response serializes to PolicyResponse
    policy = PolicyResponse(**requests.post(
        url, json = myobj
    ).json())

    assert policy.oop_max == 10000
    assert policy.remaining_oop_max == 9000
    assert policy.copay == 3000

def checkTimeoutEndpointDoesNotAddToResultList():
    url = 'http://0.0.0.0:5007/api/v1/coalesce'
    myobj = {
       "memberId": 3,
        "postAlgoBody": {
            "primary": {
                "column": "oop_max",
                "sort_body": {
                    "sort_direction": "DESC",
                    "sort_type": "value"
                }
            },
            "secondary": {
                "column": "remaining_oop_max",
                "sort_body": {
                    "sort_direction": "DESC",
                    "sort_type": "value"
                }
            },
            "third": {
                "column": "copay",
                "sort_body": {
                    "sort_direction": "DESC",
                    "sort_type": "value"
                }
            }
        }, 
        "urlList": [
        "http://0.0.0.0:5007/api/v1/api1?memberId={}",
        "http://0.0.0.0:5007/api/v1/api2?memberId={}",
        "http://0.0.0.0:5007/api/v1/apiTimeout?memberId={}"
        ]
    }
    policy = PolicyResponse(**requests.post(
        url, json = myobj
    ).json())
    assert policy.oop_max != 9999999

def check404EndpointDoesNotBreakLogic():
    url = 'http://0.0.0.0:5007/api/v1/coalesce'
    myobj = {
       "memberId": 1,
        "postAlgoBody": {
            "primary": {
                "column": "oop_max",
                "sort_body": {
                    "sort_direction": "ASC",
                    "sort_type": "value"
                }
            },
            "secondary": {
                "column": "remaining_oop_max",
                "sort_body": {
                    "sort_direction": "DESC",
                    "sort_type": "value"
                }
            },
            "third": {
                "column": "copay",
                "sort_body": {
                    "sort_direction": "ASC",
                    "sort_type": "value"
                }
            }
        }, 
        "urlList": [
        "http://0.0.0.0:5007/api/v1/api1?memberId={}",
        "http://0.0.0.0:5007/api/v1/api2?memberId={}",
        "http://0.0.0.0:5007/api/v1/exceptionEndpoint?memberId={}",
        ]
    }
    policy = PolicyResponse(**requests.post(
        url, json = myobj
    ).json())
    assert policy.oop_max == 10000
 

checkSortByPrimary()
checkSortBySecondary()
checkSortByThird()
checkTimeoutEndpointDoesNotAddToResultList()
check404EndpointDoesNotBreakLogic()

print("All Tests Passed")