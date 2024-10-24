import sqlite3
from contextlib import closing
from datetime import date, datetime
from scr.storage_strategy import StorageStrategy

class SQLiteStorage(StorageStrategy):
    """ SQLiteStorage class.
    
        Attributes:

        DB_NAME = "scr/habits.db"
    """

    DB_NAME = "scr/habits.db"


    def __init__(self):
        """Initialize a new instance of the SQLiteStorage class.
            Create the tables in the database, if not exists:
            
            habit (habit (id INTEGER PRIMARY KEY, name TEXT NOT NULL,
            description TEXT NOT NULL, frequency INT NOT NULL)

            tracking (ID INTEGER PRIMARY KEY, habit_id INTEGER, completed_dates TEXT,
             FOREIGN KEY(habit_id) REFERENCES habit (id))
        """
        with sqlite3.connect(self.DB_NAME) as connect:
            with closing(connect.cursor()) as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS habit (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        description TEXT NOT NULL,
                        frequency INT NOT NULL,
                        creation_time TEXT NOT NULL
                    )
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS tracking (
                        ID INTEGER PRIMARY KEY,
                        habit_id INTEGER,
                        completed_dates TEXT,
                        FOREIGN KEY(habit_id) REFERENCES habit (id)
                    )"""
                )
            connect.commit()

    def save(self, habit):
        """Save the habit data to the database.
            Returns: None"""
        with sqlite3.connect(self.DB_NAME) as connect:
            with closing(connect.cursor()) as cursor:
                if habit.habit_id:
                    #Update existing habit data
                    cursor.execute("""
                        UPDATE habit SET name = ?, description = ? WHERE id = ?
                    """,(habit.name, habit.description, habit.habit_id))


                else:
                    #Insert new habit data
                    cursor.execute("""
                        INSERT INTO habit (name, description, frequency, creation_time) VALUES (?, ?, ?, ?)
                    """, (habit.name, habit.description, habit.completion.frequency,
                          habit.completion.creation_time.isoformat()))
                    habit.habit_id = cursor.lastrowid

                #get existing completions
                cursor.execute("""
                    SELECT completed_dates FROM tracking WHERE habit_id = ?
                """, (habit.habit_id,))
                existing_dates = {row[0] for row in cursor.fetchall()}

                #Insert new completions in the database
                for date_value in [d for d in habit.completion.completed_dates
                                   if d not in self.isoformat_to_datetime(existing_dates)\
                                     and isinstance(d, date)]:
                    cursor.execute("""
                        INSERT INTO tracking (habit_id, completed_dates) VALUES (?, ?)
                    """, (habit.habit_id, date_value.isoformat()))

            connect.commit()


    def load(self, habit_id):
        """
        Load the data from the database.

        Returns:
            dictionary: {"name":, "description":, "frequency": , "completed_dates": , "habit_id": }
        """
        with sqlite3.connect(self.DB_NAME) as connect:
            with closing(connect.cursor()) as cursor:
                #fetch habit data
                cursor.execute("""
                    SELECT name, description, frequency, creation_time FROM habit WHERE id = ?
                """, (habit_id,))
                result = cursor.fetchone()
                if not result:
                    return None

                cursor.execute("""
                    SELECT completed_dates FROM tracking WHERE habit_id = ?
                """, (habit_id,))
                completed_dates = self.isoformat_to_datetime([row[0] for row in cursor.fetchall()])
                return {"name" : result[0],
                        "description" : result[1],
                        "frequency" : result[2],
                        "completed_dates" : completed_dates,
                        "creation_time" : datetime.fromisoformat(result[3]),
                        "habit_id" : habit_id
                        }


    def delete(self, habit_id):
        """
        Delete the data with this habit_id
        """
        with sqlite3.connect(self.DB_NAME) as connect:
            with closing(connect.cursor()) as cursor:
                cursor.execute("""
                    DELETE FROM tracking WHERE habit_id = ?
                """, (habit_id,))
                cursor.execute("""
                    DELETE FROM habit WHERE id = ?
                """, (habit_id,))
            connect.commit()

    def isoformat_to_datetime(self, completed_dates):
        """
        Transform the dates of the list from iso-format into datetime.date-format.

        Returns:
            [datetime.date]: The dates in datetime.date-format
        """
        transformed_dates = []
        for date_value in completed_dates:
            try:
                transformed_dates.append(date.fromisoformat(date_value))
            except (TypeError, ValueError):
                continue
        return transformed_dates


    def get_all_id(self):
        """
        Get the list of all habit_ids of the saved habits.

        Returns:
            [int]: List of the habit_ids
        """
        with sqlite3.connect(self.DB_NAME) as connect:
            with closing(connect.cursor()) as cursor:
                cursor.execute("""
                    SELECT id FROM habit
                """)
                return [row[0] for row in cursor.fetchall()]
