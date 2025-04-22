import mysql.connector
from dotenv import load_dotenv
import os

class DatabaseConnection:

    __db = None

    @staticmethod
    def startConnection():
        """
        Initializes the database connection using the credentials stored in the .env file.
        """
        if DatabaseConnection.__db is not None:
            return
        
        load_dotenv()
        DatabaseConnection.__db = mysql.connector.connect(
            host = os.getenv("HOST"),
            user = os.getenv("USER"),
            password = os.getenv("PASSWORD"),
            port = 3306,
            database = os.getenv("DATABASE"),
            use_pure = True
        )
        DatabaseConnection.__db.autocommit = True

    @staticmethod
    def getConnection():
        """
        Returns the database connection object. If the connection is not established,
        it initializes the connection first.
        """
        if DatabaseConnection.__db is None:
            DatabaseConnection.startConnection()
        return DatabaseConnection.__db

    @staticmethod
    def closeConnection():
        """
        Closes the database connection if it is open.
        """
        if DatabaseConnection.__db is None:
            return
        if DatabaseConnection.__db.is_connected():
            DatabaseConnection.__db.close()