from os import stat
import requests 
from datetime import datetime as dt
import json
import smtplib
import time

def send_email(data):
    URL = "https://www.cowin.gov.in/home"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('hraj2661999@gmail.com', 'RaNdOm PaSsWoRd')

    subject = "COVID-19 Vaccine Available!!"
    body = '''Vaacine is available book your slot here: ''' + URL + '''\n\n''' + data

    msg = f"Subject:{subject}\n\n{body}"
    server.sendmail(
        'hraj2661999@gmail.com',
        'hraj2661999@gmail.com',
        msg
    )
    print('HEY! MAIL HAS BEEN SENT')

    server.quit()

def check_available_sessions():
    today = str(dt.today().strftime("%d-%m-%Y"))

    # filepath = "./meta_state_id.json"
    # states = None
    # with open(filepath, "r") as f_obj:
    #     states = json.load(f_obj)
    #     states = states["states"]

    filepath = "./settings.json"
    f_obj = open(filepath)
    user = json.load(f_obj)
        

    # for state in states:
    #     print(str(state["state_id"])+". "+state["state_name"])

    # selected_state_id = int(input("Select State index: "))

    header = {"User-Agent": "Mozilla/5.0 (Macintosh Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15"}

    # districts_request_obj = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/districts/" + str(selected_state_id), headers=header)

    # districts = json.loads(str(districts_request_obj.content)[2:-1])
    # districts = districts["districts"]

    # print("\n")
    # for district in districts:
    #     print(str(district["district_id"]) + ". " + str(district["district_name"]))

    # selected_district_id = int(input("Select District index: "))
    
    selected_district_id = user["district_id"]

    centers_request_obj = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id="+str(selected_district_id)+"&date="+ today, headers=header)

    centers = json.loads(str(centers_request_obj.content)[2:-1])
    centers = centers["centers"]

    centers_sorted_by_date = {}

    for center in centers:
        for session in center["sessions"]:
            if session["available_capacity"] > 0:
                slot_list_as_str = ""
                for slot in session["slots"]:
                    slot_list_as_str += slot + "\n"
                if session["date"] in centers_sorted_by_date.keys():
                    centers_sorted_by_date[session["date"]] += ''''''+ center["fee_type"] + ''' '''+ session["vaccine"] + ''' available at ''' + center["name"]+ '''.\n'''  + '''The available capacity is ''' + str(session["available_capacity"]) + ''' with a age limit of '''+ str(session["min_age_limit"]) + '''\n '''+'''Here is the list of available slots: \n'''+slot_list_as_str + '''\n'''
                else:
                    centers_sorted_by_date[session["date"]] = '''''' + center["fee_type"] + ''' ''' + session["vaccine"] + ''' available at ''' + center["name"] + '''.\n''' + '''The available capacity is ''' + str(
                    session["available_capacity"]) + ''' with a age limit of ''' + str(session["min_age_limit"]) + '''\n '''+'''Here is the list of available slots: \n'''+slot_list_as_str + '''\n'''

    if len(centers_sorted_by_date.keys()) == 0:
        print("No centers available")
    else:
        for date, sessions in centers_sorted_by_date.items(): 
            data = '''On ''' + date + ''': \n''' + sessions
            send_email(data)
            
        
while(True):
  check_available_sessions()
  time.sleep(60*60*24)
