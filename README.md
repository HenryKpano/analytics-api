Welcome to my FAST API analytics-api project

### Using the starter project

Below are the steps to follow to replicate this project

1. Create a .env file in the analytics-api folder with the below credntials if you are using Redshift

        REDSHIFT_HOST=my-aws.redshift.amazonaws.com
        REDSHIFT_USER=username
        REDSHIFT_PASSWORD=yourpassword
        REDSHIFT_PORT=port_number
        REDSHIFT_DB=dbname
        # REDSHIFT_SCHEMA=schema_name
        API_KEY=you_can_build_key_with_python3
        REDIS_HOST=redis

2. Open your desktop docker to enable smooth initialization

3. cd into the location of this project(analytics-api)

4. run docker-compose build on your terminal to build the image na dcontainers

5. run docker-compose up on your terminal

6. open your postman to test the api

7. enter the API Key you generated into the postman authorization with Key name as X-API-KEY

8. enter the value of the API as the API_KEY you generated

9. test API locally using http://localhost:8000/api/v1/analytics/revenue?start=2025-06-01&end=2025-06-06&product=US&page=1