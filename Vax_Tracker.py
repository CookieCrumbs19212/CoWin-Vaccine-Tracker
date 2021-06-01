import requests

def getCowinData(STATE, DISTRICT, REQUEST_DATE, VACCINE):
    # variables to store the CoWin API assigned State ID and District ID.
    STATE_ID = None
    DISTRICT_ID = None

    # will store the vaccine availability search results.
    RESULTS = ""

    HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36", 
                        "accept": "application/json", "Accept-Language": "en_EN"}


    # get the state_id for STATE_NAME.
    response = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/states", headers=HEADERS)

    # status codes greater than 200 indicate a failed API request.
    if(response.status_code > 200):
        raise Exception(f"Request 1 failed with Status Code {response.status_code} (request for list of states).")
    else:
        print(f"Request 1 Completed with Status Code {response.status_code} (Successful request).")
    
    # finding the state id.
    states = response.json()["states"]
    for state in states:
        if ((state["state_name"]).lower() == STATE.lower()):
            STATE_ID = state["state_id"]
            break
    
    # if STATE_NAME did not match with any of the states in the list.
    if (STATE_ID == None):
        raise Exception(f"State {STATE} not found.")

    #------------------------------------------------------------------------------------------------------------------

    # get the district_id for DISTRICT_NAME.
    response = requests.get(f"https://cdn-api.co-vin.in/api/v2/admin/location/districts/{STATE_ID}", headers=HEADERS)

    # status codes greater than 200 indicate a failed API request.
    if(response.status_code > 200):
        raise Exception(f"Request 2 failed with Status Code {response.status_code} (request for list of districts).")
    else:
        print(f"Request 2 Completed with Status Code {response.status_code} (Successful request).")

    # finding district id.
    districts = response.json()["districts"]
    for district in districts:
        if ((district["district_name"]).lower() == DISTRICT.lower()):
            DISTRICT_ID = district["district_id"]
            break
    
    # if STATE_ID did not match with any of the districts in the list
    if (DISTRICT_ID == None):
        raise Exception(f"No Vaccine information for District {DISTRICT}.")

    #------------------------------------------------------------------------------------------------------------------

    # get the vaccine information for the district
    response = requests.get(f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={DISTRICT_ID}&date={REQUEST_DATE}", headers=HEADERS)

    # status codes greater than 200 indicate a failed API request.
    if(response.status_code > 200):
        raise Exception(f"Request 3 failed with Status Code {response.status_code} (request for vaccine information by district).")
    else:
        print(f"Request 3 Completed with Status Code {response.status_code} (Successful request).")

    sessions = response.json()["sessions"]
    res_number = 1 # result number to display for each result
    for session in sessions:
        if ((session["vaccine"]).lower() == VACCINE.lower()):
            RESULTS+=f"""\n{res_number}.
                        \nCenter Name            : {session["name"]}
                        \nCenter Address         : {session["address"]}
                        \nVaccine Offered        : {session["vaccine"]}
                        \nMinimum Age Limit      : {session["min_age_limit"]}
                        \nNo. of Doses Available : {session["available_capacity"]}
                        \nPaid or Free Vaccine?  : {session["fee_type"]}, INR {session["fee"]}
                        \nVaccine Center Open from {(session["from"])[0:5]} to {(session["to"][0:5])}.
                        \n
                        """
            res_number += 1 # incrementing result number

    # returning the string containing all the vaccine availability information.
    return RESULTS

# set the date.
#day = "01"
#mon = "06"
#year = "2021"
#date = f"{day}-{mon}-{year}"

# get parameters.
state = input("\n\nEnter State: ") # eg. Maharashtra
district = input("\nEnter District: ") # eg. Pune
vaccine = input("\nEnter Vaccine name: ") # eg. Covishield or Covaxin
date = input("\nEnter search date (DD-MM-YYYY): ") # the date for when user wants to check for vaccine availability

# getting the vaccine availability results.
vax_info = getCowinData(state, district, date, vaccine)
if (vax_info == ""):
    print(f"No Vaccine Information avaiable for {district} on {date}")
else:
    print(f"Vaccine Information for Date: {date}")
    print(vax_info)