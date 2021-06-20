import numpy as np
import gspread
import gspread_dataframe
from oauth2client.service_account import ServiceAccountCredentials


CREDENTIALS_FILE = 'name of your .json file with credentials'

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive.file',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)  # open credentials file for
# google sheets

# Initialize the client, and open the sheet by name:
client = gspread.authorize(credentials)
sh = client.open('TelegramBot Database')


def get_row(user_name):  # getter for next empty row to fill
    sheet = sh.worksheet(user_name)
    return next_available_row(sheet)


def next_available_row(worksheet):  # function that finds first empty row
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)


def check_user(user_id):  # check if user is on list
    sheet = sh.sheet1
    user_id = float(user_id)
    # Get data from the sheet:
    data = gspread_dataframe.get_as_dataframe(sheet)
    for i in range(len(data)):
        if data.at[i, 'telegram id'] == np.NaN:
            return 'none'
        elif data.at[i, 'telegram id'] == user_id:
            return data.at[i, 'name']
    return 'none'


def create_worksheet(user_id, user_name):  # create worksheet for a new user
    sheet = sh.sheet1
    next_row = next_available_row(sheet)
    sheet.update_acell('A{}'.format(next_row), user_id)
    sheet.update_acell('B{}'.format(next_row), user_name)
    new_sheet = sh.add_worksheet(title=user_name, rows=100, cols=9)
    # set columns names
    cell_list = new_sheet.range('A1:I1')
    cell_values = ['Дата и время', 'Ситуация', 'Физиологический ответ', 'Автоматические мысли', 'Эмоции',
                   'Когнитивное искажение', 'Адаптивный ответ', 'Результат', 'Действие']
    for i, val in enumerate(cell_values):  # gives us a tuple of an index and value
        cell_list[i].value = val  # use the index on cell_list and the val from cell_values
    new_sheet.update_cells(cell_list)
    # color black for styles
    black = {
        "red": 0,
        "green": 0,
        "blue": 0,
        "alpha": 1
    }
    # set table style
    new_sheet.format('A1:I1', {
            'textFormat': {'bold': True},
            "horizontalAlignment": "CENTER",
            "borders": {
                "top": {"style": "SOLID",
                        "color": black},
                "bottom": {"style": "SOLID",
                           "color": black},
                "left": {"style": "SOLID",
                         "color": black},
                "right": {"style": "SOLID",
                          "color": black}
            }
        })
    new_sheet.format('A2:I100', {
        "horizontalAlignment": "CENTER",
        "borders": {
                "top": {"style": "SOLID",
                        "color": black},
                "bottom": {"style": "SOLID",
                           "color": black},
                "left": {"style": "SOLID",
                         "color": black},
                "right": {"style": "SOLID",
                          "color": black}
            }
    })
    sheetId = sh.worksheet(user_name)._properties['sheetId']
    body = {
        "requests": [
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": sheetId,
                        "dimension": "COLUMNS",
                        "startIndex": 0,
                        "endIndex": 8
                    },
                    "properties": {
                        "pixelSize": 200
                    },
                    "fields": "pixelSize"
                }
            }
        ]
    }
    res = sh.batch_update(body)


def add_date(user_name, date):  # add date to the database and get a current row number
    sheet = sh.worksheet(user_name)
    next_row = next_available_row(sheet)
    sheet.update_acell('A{}'.format(next_row), date)
    return next_row


def add_info(user_name, row, column, text):  # add data to the database
    sheet = sh.worksheet(user_name)
    sheet.update_cell(row, column, text)

