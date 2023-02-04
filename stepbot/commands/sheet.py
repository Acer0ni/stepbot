import gspread

gc = gspread.service_account(filename='credentials.json')
def get_empty_row(worksheet,spreadsheet):
    # Authenticate and access the Google Spreadsheet
    sh = gc.open(worksheet)
    spreadsheet_name = sh.worksheet(spreadsheet)

    # Get the data from the worksheet as a list of rows
    data = spreadsheet_name.get_all_values()

    # Find the first empty row
    empty_row = None
    for i, row in enumerate(data):
        if all(cell == '' for cell in row):
            empty_row = i + 1
            break

    return empty_row if empty_row else len(data) + 1

def insert_to_sheet(dictionary, worksheet,spreadsheet):
    sh = gc.open(worksheet)
    waitlist = sh.worksheet(spreadsheet)
    column = 1  

    empty_row = get_empty_row(worksheet,spreadsheet)

    for key, value in dictionary.items():
        try:
            values = value.strip().split(',')
        except AttributeError:
            pass
        else:
            if waitlist.find(key) is None:
                pass
            else:
                column = waitlist.find(key).col
                
            for v in values:
                while waitlist.cell(empty_row, column).value is not None:
                    column += 1
                waitlist.update_cell(empty_row, column, v)
                print(f'Inserted {v} to {key} column \t')