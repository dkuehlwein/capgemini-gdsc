__author__ = "Gondal, Saad Abdullah"
__version__ = "0.1"
__email__ = "saad-abdullah.gondal@capgemini.com"

import xlrd
import sqlite3

book = xlrd.open_workbook('data/summaries/Summaries.xlsx')
sheet = book.sheet_by_index(0)

database = sqlite3.connect('website/db.sqlite3')

cursor = database.cursor()

query = """INSERT INTO evaluation_summaries (ppt_file_names, file_summary) VALUES (?, ?)"""

for item in range(1, sheet.nrows):
    file_name = sheet.cell(item, 0).value
    summary = sheet.cell(item, 1).value
    values = (file_name, summary)
    print(file_name)
    cursor.execute(query, values)

cursor.close()
database.commit()
database.close()
