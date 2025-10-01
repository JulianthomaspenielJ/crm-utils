import requests
from bs4 import BeautifulSoup

# Initialize global variables
url = ""
inputName = ""
csrfName = ""
status = ""

# Set URL, input field name, and CSRF token field name
def set(URL, input_field, csrf_field):
    global url, inputName, csrfName
    url = URL
    inputName = input_field
    csrfName = csrf_field

# Set URL
def seturl(URL):
    global url
    url = URL

# Set input field name
def setinput(input_field):
    global inputName
    inputName = input_field

# Set CSRF token field name
def setcsrf(csrf_field):
    global csrfName
    csrfName = csrf_field

# Perform GST number check
def check(gstin):
    global url, inputName, csrfName, status
    if not url:
        url = "https://www.knowyourgst.com/gst-number-search/"
    if not inputName:
        inputName = "gstnum"
    if not csrfName:
        csrfName = "csrfmiddlewaretoken"

    client = requests.session()
    status = ""
    client.get(url)
    if client.get(url).status_code != 200:
        status += "[GET URL Failure]"

    csrftoken = client.cookies.get('csrftoken') or client.cookies.get('csrf')
    data = {inputName: gstin, csrfName: csrftoken}
    r = client.post(url, data=data, headers=dict(Referer=url))

    if not r.content:
        status += "[Content Retrieval Failure]"
        # Reset data if content retrieval fails
        reset_data()
        return

    try:
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.find('table', class_="striped highlight questionlist").find_all('tr')
        if not table:
            status += "[Parsing Failure]"
            # Reset data if no table is found
            reset_data()
            return

        data = [[td.text for td in tr.find_all('td')] for tr in table]
        reqData = [row[1] for row in data]

        global name, pan, person, gst_type, add, date
        name = str(reqData[2])
        pan = str(reqData[1])
        person = str(reqData[2])
        gst_type = str(reqData[4])
        add = str(reqData[6].split(",")[0])
        date = str(reqData[8].split("T")[0])
        status += "[No Errors]"
    except Exception as e:
        status += "[Parsing Failure]"
        print(f"Error: {e}")
        # Reset data on parsing failure
        reset_data()

def reset_data():
    global name, pan, person, gst_type, add, date
    name = ""
    pan = ""
    person = ""
    gst_type = ""
    add = ""
    date = ""

def disp(input_data):
    print(input_data)

def printall():
    print(name, pan, person, gst_type, add, date)

def printwith(spacer):
    print(name, spacer, pan, spacer, person, spacer, gst_type, spacer, add, spacer, date)

def checkstatus():
    global status
    if not status:
        status = "[Offline]"
    print(status)
