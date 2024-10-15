import pandas as pd
import psycopg2

class DB_Client:
    """
    A client for interacting with a PostgreSQL database.

    This class establishes a connection to a PostgreSQL database and can be used to execute queries
    and interact with the database. It uses `psycopg2` to handle the database connection.

    Attributes:
        host (str): The hostname or IP address of the database server.
        user_name (str): The username used to authenticate to the database.
        password (str): The password used to authenticate to the database.
        port (str): The port number the database is listening on.
        database_name (str): The name of the specific database to connect to.
    """

    def __init__(self, host: str, user_name: str, password: str, port: str, database_name: str):
        """
        Initializes the DB_Client with the given connection details.

        Args:
            host (str): The hostname or IP address of the database server.
            user_name (str): The username used to authenticate to the database.
            password (str): The password used to authenticate to the database.
            port (str): The port number the database is listening on.
            database_name (str): The name of the database to connect to.
        """
        self.host = host
        self.user_name = user_name
        self.password = password
        self.port = port
        self.database_name = database_name
        self.connection = self.__establish_connection()
        self.cursor = self.connection.cursor()
    
    def __establish_connection(self):
        """
        Establishes a connection to the PostgreSQL database.

        This method attempts to establish a connection to the database using the provided
        connection details. It uses `psycopg2.connect` to create the connection. If the
        connection fails, the method returns `None`.

        Returns:
            connection: A `psycopg2` connection object if successful, or `None` if the connection
                        fails.
        
        Raises:
            Exception: If there is an error in establishing the connection.
        """
        try:
            connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database_name,
                user=self.user_name,
                password=self.password
            )
            return connection
        except Exception as e:
            print(f"Failed to establish connection: {e}")
            return None


if __name__ == "__main__":
    from dotenv import load_dotenv
    import argparse, os

    # define argument for providing the path to .env file and also the cleaned data
    parser = argparse.ArgumentParser(
        prog="Data Pusher",
        description="A script that pushed cleaned telegram messages to a postgres database."
    )

    parser.add_argument('--env_path', default='.env') # the path to the .env file which contains connection params
    parser.add_argument('--data_path', default='./data/preprocessed.csv') # the path to the cleaned/preprocessed telegram data

    args = parser.parse_args()
    
    # obtain the parsed args
    env_path = args.env_path
    data_path = args.data_path

    # load the database connection params from the .env
    load_dotenv(dotenv_path=env_path)
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    connection = DB_Client(
        host=host,
        port=port,
        user_name=username,
        password=password,
        database_name=db_name
    )