# A sample web app

This web app simulates an inventory management system to manage item records

## Specifications

- Language: Python
- API Framework: FastApi
- Deployment method: AWS Lambda/ AWS API Gateway
- Database: AWS DynamoDB

## Demo APIs

1. `POST {baseUrl}/items`. Inserts a new item

    Request body

    ```text
    {
        "name": "Notebook",
        "category": "Stationary",
        "price": 5.5
    }
    ```

    Response

    ```text
    {
        "id": 43640066224263851205823615220508082409
    }
    ```

2. `GET {baseUrl}/items?dt_from=...&dt_to=...`. To query for items with `last_updated_dt` within the datetime range

    Query parameters

    ```text
    "dt_from": "2022-01-01 10:00:00"
    "dt_to": "2022-01-25 10:00:00"
    ```

    Response

    ```text
    {
        "items": [
            {
                "id": 135,
                "name": "Notebook",
                "category": "Stationary",
                "price": 5.5
            },
            {
                "id": 136,
                "name": "Key Chain",
                "category": "Gift",
                "price": 3
            },
            {
                "id": 137,
                "name": "Baggage Cover",
                "category": "Gift",
                "price": 15
            }
        ],
        "total_price": 23.5
    }
    ```

3. `GET {baseUrl}/items/statistics?category=...`. Performs aggregation on the data. By passing in a category, the total price and number of items will be returned. If category: “all” is passed, it should return the data for all categories.

    Query parameters

    ```text
    "category": "all"
    OR
    "category": "Gift"
    ```

    Response (if `"category": "all"`)

    ```text
    {
        "items": [
            {
                "category": "Stationary",
                "total_price": 5.5,
                "count": 1
            },
            {
                "category": "Gift",
                "total_price": 18,
                "count": 2
            }
        ]
    }
    ```

## Local deployment methods

The base url used to test the APIs for each method is shown below.

1. Deploy with docker-compose. Base url is `http://localhost:8001`

    ```sh
    docker-compose up --build
    ```

2. Deploy with AWS SAM. This emulates a deployment with AWS Lambda/AWS API Gateway. Base url is `http://localhost:3000`

    Build database

    ```sh
    docker-compose up --build dynamodb
    ```

    Build docker image to be used by AWS Lambda

    ```sh
    docker build -t my-fastapi-app:latest -f Dockerfile.lambda .
    ```

    Start app that uses AWS Lambda/AWS API Gateway and connect it to docker network to access Dynamodb database

    ```sh
    sam local start-api --template aws/template.yaml --docker-network local-network
    ```

## Tests

There are unit tests and integrations tests located in `app/tests` folder. To run the tests:

 ```sh
 docker-compose -f docker-compose-test.yml up --build
 docker exec -it fastapi-apigateway-lambda-dynamodb_app-test_1 /bin/bash
 pytest
 ```
