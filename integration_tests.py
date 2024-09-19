import sys
from app.api.external_apis import PolicyResponse
import requests

# intergration tests that test different corner cases of the program.

# 1) Tests the results from the external APIs are first sorted by primary column passed
# 2) Tests the results from the external APIs are sorted by the secondary column second after the first sort
# 3) Tests the results from the external APIs are sorted by the third column after the first two columns
# 4) Tests that when we hit an external API that times out ( sleeps for 20 seconds while we have a 10 second time out ) does not break the request
# or have the results ( timeout didnt work ) from the API in the result
# 5) Tests, by adding a url to urllist for an endpoint that will instantly return 404, does not break the request
# 6) Tests passing an invalid Request Body will throw a 500 status error
# 7) If empty URL list is passed to body should return status_code 500



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
 

def checkInvalidBodyPayloadReturnStatusCode500():
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
                "column": "oop_max",
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
    res = requests.post(
        url, json = myobj
    )

    assert res.status_code == 500


def checkErrorIsReturnedWhenEmptyUrlListPassed():
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
        "urlList": []
    }
    res = requests.post(
        url, json = myobj
    )

    assert res.status_code == 500


checkSortByPrimary()
checkSortBySecondary()
checkSortByThird()
checkTimeoutEndpointDoesNotAddToResultList()
check404EndpointDoesNotBreakLogic()
checkInvalidBodyPayloadReturnStatusCode500()
checkErrorIsReturnedWhenEmptyUrlListPassed()

print("All Integration Tests Passed")