from PyQt6 import QtWidgets as qw
from PyQt6.QtWidgets import QTableWidgetItem
from tableForm import Ui_MainWindow
import sys
from PyQt6.QtCore import pyqtSignal, pyqtSlot
import mysql.connector

class Window(qw.QMainWindow):
    day_changed = pyqtSignal(int) # signals for @pyqSlor() to execute item_changed() when any item is changed in interface
    hour_changed = pyqtSignal(int)
    text_changed = pyqtSignal(str)

    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.hour = None
        self.day = None
        self.text = None
        self.loadTable()
        self.connect_to_database()
        self.load_data_from_database()
        self.ui.tableList.itemChanged.connect(self.item_changed)  # Connect the signal here


    def connect_to_database(self):
        # Your database connection parameters
        host = ''
        user = ''
        password = ''
        database = ''

        self.db_connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

    def loadTable(self):
        self.ui.tableList.setRowCount(7)
        self.ui.tableList.setColumnCount(14)
        self.ui.tableList.setVerticalHeaderLabels(('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'))
        self.ui.tableList.setHorizontalHeaderLabels(('9:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00','21:00','22:00','23:00'))

    def load_data_from_database(self):
        # Retrieve data from the database and populate your interface
        cursor = self.db_connection.cursor()

        # Execute a SELECT query to retrieve data
        query = "SELECT * FROM list_table"
        cursor.execute(query)

        # Fetch the data from the database
        datas = cursor.fetchall()

        for data in datas:
            print(data)


        # Populate the interface with data
        for hour in range(14):
            for day in range(1, 8):  # Skip the first column (ID)
                item = datas[hour][day]
                if item is not None:
                    self.ui.tableList.setItem(day-1, hour, QTableWidgetItem(item)) # The database is setted as columns represent the days and rows represent the hours. oposite of the interface

    @pyqtSlot(QTableWidgetItem)
    def item_changed(self, item):
        try:
            print("Item changed slot called")  # Add this line

            day = item.row() + 1 # you dont have to add one, just did it to read easily like first day of the week. 
            hour = item.column() + 9 # the rows of hours in database start with 9 o'clock
            text = item.text() # get the text 
            print(f"day: {day}, hour: {hour}, Text: {text}")

            if day == 1: # column names in database
                day = 'Monday'
            elif day == 2:
                day = 'Tuesday'
            elif day == 3:
                day = 'Wednesday'
            elif day == 4:
                day = 'Thursday'
            elif day == 5:
                day = 'Friday'
            elif day == 6:
                day = 'Saturday'
            elif day == 7:
                day = 'Sunday'

            print()
            # Update the database with the new value
            cursor = self.db_connection.cursor()
            query = f"UPDATE list_table SET {day} = %s WHERE id = %s"
            values = (text, hour)
            cursor.execute(query, values)
            self.db_connection.commit()
            cursor.close()
        except Exception as e:
            print("Error :  ", e)

def app():
    app = qw.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())

app()
