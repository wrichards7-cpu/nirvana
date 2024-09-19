## Wesley Richards Nirvana Take Home Assignment

### Solution Overview 

For this assignment, to be creative, I decided to implement compond sort solution where a user can rank the columns ( oop_max, remaining_oop_max, copay ) they care most about and sort the returned results by it. Currently the sorting only supports sorting by the values in the column. I wanted to also support sorting the column by frequency ( How many times the value appears in all the returned API ) but had to leave for vacation.

Example payload to the endpoint looks like so -

```
curl --location 'http://0.0.0.0:5007/api/v1/coalesce' \
--header 'Content-Type: application/json' \
--data '{
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
    },
    "urlList": [
        "http://0.0.0.0:5007/api/v1/api1?memberId={}",
        "http://0.0.0.0:5007/api/v1/api2?memberId={}"
    ]
}'


```

Where the primary column is the first column to sort by where you specify ASC or DESC. The secondary is the second column to sort by if the first sort has identitical values. The third one is probably not neccessary since you know there is only one more possible choice but for now you need to specify it. 

To me this simulates a more granular way users could decide against different policies. Another way to do it would be to have tags or set configurations that could abstract down to a configuration like above. Example - "you could have a selection of Lowest Co-pay in a UI that would abstract down to an above definition"

At a high level the solution will asynchoronusly call to the URLs provided in the url_list and call the coalesce function with the compound sorting to choose a single policy. The URL list is optional and has a default value for the three main external API simulating API1, API2, API3 specified in assignement definition.

The main focus of the buisness logic in the code is to asynchronsly schedule the requests to the external endpoints and handle the cases where an external endpoint call fails or timeouts. In the implementation if an async call to an external endpoint fails or timesout the request is ignored, while the others that did succeed are returned and fed to the coalesce function. There are also checks if none of the endpoints return us any data or if only one returns where in that case we dont need to sort.

#### Implementation Overview

##### Frameworks

- FastAPI / uvicorn - Web framework
- Asyncio - concurrency model utilizing coroutines to schedules the external calls concurrently
- Httpx - async rest client that works nicely with Asyncio and it's coroutines
- SQLLite - Simple file database that stores the policies for the members

##### Files overview

- main.py - main entrypoint that creates our app object created in factory.py
- factory.py - definition of our FastAPI app object that sets start up and shutdown triggers that handle bootstraping our SQLLite database with default data and deleting the database file once we shut down
- config.py - just a basic example of a config file that is imported to the web framesworks config ( not really used in the basic application )
- integrations_tests.py - integrations tests that simulate rest requests to the main endpoint testing the corner cases. I did not have time to adapt a testing framework like pytest but each function does a basic assert to test conditions and will fail if they are not met. How to run these tests is specified in the run section below. 
- unit_tests.py - unit test file that only has one unit tests but shows how you can import the functions directly and test their input and output. How to run specificed in run section.
- Makefile - Makefile to automate bringing up the application and testing against it. How to use specified in run secion.
- requirements.txt - dependency definition. dependency as automatically installed when running the application via Makefile.
- app/resources/config/logging.yaml - logger configuration file.
- app/models/external.py - SQLLite table schema definitions for the different external endpoints API1, API2, API3. These are applied to the database during app startup.
- app/api/external_apis.py - Route endpoints for the external endpoints that simulate real world external endpoints. Each endpoint has their own database table. The two last endpoint /apiTimeout and /exceptionEndpoint are just meant to simulate responses from external endpoints with out having to mock them ( time limits i had with this implementation )
- app/api/coalesce.py - main route for our application /coalesce
that takes in the payload above, queries the external APIs specificed in the URL_LIST, and calls the coalesce function to pick a policy from the returned values.

#### Running the application

To run this application we will use the targets hosted in the Make file. The two main commands are `make run` and `make tests`. As a side note all this building and running of the application and tests should be done using docker but not possible for me to do in the time I had. 

Requirements - You need to have Python installed. Note on my machine I have my python interpreter alias'd as `python3` . If you have it as just `python` you will need to switch it in the Makefile.

`make run` - This command will first install the requirements in the requirements.txt file and run the main application / webserver

`make tests` - This command depends on `make run` where you need to have the application running successfully to work since the integration tests depend on that. ( The proper path would be to bring up an instance of the application specificly for these tests but time constraints again ) Once you run this command it will try to python run the two test files and if either fail it will cancel and display an error. 

#### Testing

Look in the test files where I have added comments describing the tests being performed.
