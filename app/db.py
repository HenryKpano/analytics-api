import psycopg2
from os import getenv

def get_db_connection():
    """
    Establish a connection to the Redshift database using environment variables.
    Returns:
        A psycopg2 connection object
    """
    return psycopg2.connect(
        dbname=getenv("REDSHIFT_DB", "analyticsdb"),
        user=getenv("REDSHIFT_USER", "your_user"),
        password=getenv("REDSHIFT_PASSWORD", "your_pass"),
        host=getenv("REDSHIFT_HOST", "your-cluster.region.redshift.amazonaws.com"),
        port=5439
    )