import gspread
import pandas as pd
import re
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
def write_in_sheet(x):

    # x="DcHm14"
    # index=0
    # for word in x.split():
    #    if word.isdigit():
    #        index=int(word)-1
    # print(index)
    index=(re.findall(r"\d+", x))
    print(index[0])
    final=int(index[0])+1
    print(final)

    # add credentials to the accountF:\Covid_vare\Covidvare\Covidvare\covid
    creds = ServiceAccountCredentials.from_json_keyfile_name('F:/Covid_vare/Covidvare/Covidvare/covid/COVIDCRISIS-a81cd4c8997e.json', scope)

    # authorize the clientsheet
    client = gspread.authorize(creds)

    # get the instance of the Spreadsheet
    sheet = client.open('CovidPatientregistration (Responses)')

    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(0)
    sheet_instance.update_cell(final, 37, 'Yes')
    dr_name=sheet_instance.cell(final, 36).value

    #records_data = sheet_instance.get_all_records()
    # view the data
    return dr_name



