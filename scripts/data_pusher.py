import pandas as pd
import psycopg2, uuid

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

    def execute_query(self, query: str):
        """
        Executes a SQL query on the connected PostgreSQL database.

        This method takes a SQL query as input, executes it, and returns the result as a pandas DataFrame.

        Args:
            query (str): The SQL query to be executed.

        Returns:
            pandas.DataFrame: A DataFrame containing the query result if successful.
            None: Returns `None` if the query execution fails.
        
        Raises:
            Exception: If there is an error while executing the query.
        """
        try:
            self.cursor.execute(query=query)
            self.connection.commit()
            return None
        except Exception as e:
            print(f"Failed to execute query: {e}")
            return None

    def add_channel(self, username: str, title: str):
        """
        A method that adds a new telegram to the channel table.

        Args:
            username(str): the username of the channel
            title(str): the title of the channel

        Returns:
            uuid(UUID): the uuid of the newly added telegram channel
        """
        # generate a uuid
        id = uuid.uuid4()

        # create the sql query
        query = f"INSERT INTO channel (id, username, title) VALUES ('{id}', '{username}', '{title}')"

        # execute the query
        self.execute_query(query=query)

        return id

    def add_messages(self, channel_id: str, telegram_id_col: str, message_col: str, media_path_col: str, date_col:str, data: pd.DataFrame):
        """
        A method that inserts messages into the message table.

        Args:
            channel_id_col(str): the id of the telegram channel we want the messages to be added to.
            telegram_id_col(str): the name of the column that contains the telegram_id values.
            message_col(str): the name of the column that contains the message values.
            media_path_col(str): the name of the column that contains the media_path values.
            date_col(str): the name of the column that contains the date values.
            data(pd.DataFrame): the dataframe that contains the data to be inserted.

        Returns: 
        """

        # obtain the columns of interest
        data = data[[telegram_id_col, message_col, media_path_col, date_col]]

        # first half of the query, the one that declares the table and the types of values to be passed
        first_half = f"INSERT INTO message (id, channel_id, telegram_id, message, date, media_path) VALUES"
        
        # generate the values to add to the second half of the query
        values = []
        for index, row in data.iterrows():
            # generate uuid for every entry
            id = uuid.uuid4()

            # create the sql query
            query = f" ('{id}', '{channel_id}', '{row[telegram_id_col]}', '{row[message_col]}', '{row[date_col]}', '{row[media_path_col]}'),"

            # add to the values list
            values.append(query)
        
        # create the second half of the query
        second_half = ''.join(values)
        
        # obtain the query
        query = first_half + second_half

        # remove the last ','
        query = query[:-1]

        # execute the command
        self.execute_query(query=query)

    def push_data(self, data: pd.DataFrame):
        """
        A method that pushes the cleaned data to a postgress database

        Args:
            data(pd.DataFrame): the cleaned data frame
        """

        # group the data by username and title
        grouping = data.groupby(by=['channel_username', 'channel_title'])

        # obtain the channels with their channel_usernames and channel_titles
        channels = list(grouping.groups.keys())

        # add the channel to the tabel and also add all the related messages
        for channel in channels:
            # obtain the channel username and title
            username = channel[0]
            title = channel[1]

            # add the channel to channel table
            channel_id = self.add_channel(username=username, title=title)
            print(f"Channel {title}({username}) has been added with the UUID {channel_id}.")

            # add the messages of that channel to the message channel
            channel_messages = grouping.get_group(name=channel)
            self.add_messages(channel_id=channel_id, telegram_id_col="id", message_col="message", media_path_col="media_path", date_col='date', data=channel_messages)
            print(f"{channel_messages.shape[0]} messages add for channel {title}({username}).\n")
            
        print("Finished pushing data!")

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

    # create a database client
    client = DB_Client(
        host=host,
        port=port,
        user_name=username,
        password=password,
        database_name=db_name
    )

    # read the 
    data = pd.read_csv(data_path)

    # push the data to postgress
    client.push_data(data=data)