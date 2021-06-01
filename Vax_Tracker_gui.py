from tkinter import *
from tkinter import ttk
import requests

root = Tk()
root.geometry("1300x750")
root.resizable(0,0)

# Initialization
root.title("CoWin Vaccine Tracker")

# custom settings
heading_font = ('Courier New', 25)
output_font = ('Courier New', 18)

label_options = {"font":('Courier New', 20), 
                "width":25,
                "height":2,
                "justify":"center", 
                "borderwidth":3}
label_pack_options = {"padx":5, "pady":(10,0), "anchor":W}

entry_options = {"font":('Courier New', 20), 
                "width":25, 
                "justify":"center", 
                "borderwidth":3}
entry_pack_options = {"padx":20, "pady":(0,30)}

# Packing Heading
Label(root, text="CoWin Vaccine Tracker", height=2, font=heading_font, bg = "#313131", fg = "#FFFFFF").pack(fill = X)

#Create Panedwindow  
panedwindow = ttk.Panedwindow(root, orient=HORIZONTAL)
panedwindow.pack(fill=BOTH, expand=True)  

#Create Frames  
input_frame = Frame(panedwindow,width=500,height=750, relief=SUNKEN, bg = "#FFFFFF")  
output_frame = Frame(panedwindow,width=800,height=750, relief=SUNKEN, bg = "#FFFFFF")

panedwindow.add(input_frame, weight=2)  
panedwindow.add(output_frame, weight=3)

#Filling Frame1
# State Input
state_label = Label(input_frame, label_options, text = "Enter State",)
state_input = Entry(input_frame, entry_options)

state_label.pack(label_pack_options)
state_input.pack(entry_pack_options)

# District Input
dist_label = Label(input_frame, label_options, text = "Enter District")
dist_input = Entry(input_frame,  entry_options)

dist_label.pack(label_pack_options)
dist_input.pack(entry_pack_options)

# Vaccine Name Input
vacc_label = Label(input_frame, label_options, text = "Vaccine Name")
vacc_input = Entry(input_frame, entry_options)

vacc_label.pack(label_pack_options)
vacc_input.pack(entry_pack_options)

# Date Input
date_label = Label(input_frame, label_options, text = "Search Date (DD-MM-YYYY)")
date_input = Entry(input_frame, entry_options)

date_label.pack(label_pack_options)
date_input.pack(entry_pack_options)

# setting up scrollbar for textbox to display results
scroll_bar = Scrollbar(output_frame)
scroll_bar.pack(side = RIGHT, fill = Y)

# setting up textbox for results
result = Text(output_frame, background="#272727", foreground="#FFFFFF", relief="flat", padx=20, 
                yscrollcommand = scroll_bar.set, font = output_font, state = "disabled")
result.pack(fill=BOTH)

def getCowinData(STATE, DISTRICT, REQUEST_DATE, VACCINE):
    STATE_ID = None
    DISTRICT_ID = None

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
                        \nCenter Name            :  {session["name"]}
                        \nCenter Address         :  {session["address"]}
                        \nVaccine Offered        :  {session["vaccine"]}
                        \nMinimum Age Limit      :  {session["min_age_limit"]}
                        \nNo. of Doses Available :  {session["available_capacity"]}
                        \nPaid or Free Vaccine?  :  {session["fee_type"]}, INR {session["fee"]}
                        \nVaccine Center Open from {(session["from"])[0:5]} to {(session["to"][0:5])}.
                        \n
                        """
            res_number += 1 # incrementing result number

    # returning the string containing all the vaccine availability information.
    return RESULTS

def displayResults():
    result["state"] = "normal"
    result.delete(1.0, END)
    result.insert(1.0,getCowinData(state_input.get(), dist_input.get(), date_input.get(), vacc_input.get()))
    result["state"] = "disabled"
    result.pack()
    scroll_bar.config(command = result.yview)

buttonStyle = ttk.Style(input_frame)
buttonStyle.configure('TButton', 
                font = ('Courier New', 20, 'bold'),
                height = 3,
                background = '#29F6AD',
                foreground = '#FFFFFF')

action_button = ttk.Button(input_frame, text="Get Vaccine Information",
                        style = buttonStyle, 
                        width = 29)
action_button.pack(padx=20, pady=20, side=BOTTOM)


#Calling Main()  
root.mainloop() 
