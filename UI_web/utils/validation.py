import datetime
from utils.logging_web import log_web

# Setup logger
logger = log_web()

def form_val(user_data):
    validation = False
    selected_date = datetime.date.fromisoformat(user_data['birthday'])
    today = datetime.date.today()
    diff_date = selected_date - today
    
    logger.debug('Initiate the validation')
    if len(user_data['first_name']) == 1 or user_data['first_name'] == None:
        issue = 'First name empty'  
    elif len(user_data['last_name']) == 1 or user_data['last_name'] == None:
        issue = 'Last name empty'
    elif user_data['document_id'] == None:
        issue = 'Document ID empty'
    elif user_data['type'] == None:
        issue = 'Type empty'
    elif 360*8 > diff_date.days:
        issue = "Your aren't an adult"
    elif len(user_data['country']) == 1 or user_data['country'] == None:
        issue = 'Country is empty'
    elif len(user_data['city']) == 1 or user_data['city'] == None:
        issue = 'City is empty'
    elif len(user_data['address']) == 1 or user_data['address'] == None:
        issue = 'Address is empty'
    elif len(user_data['email']) == 1 or user_data['email'] == None:
        issue = 'Email is empty' 
    elif user_data['phone_number'] == None:
        issue = 'Phone_number ID empty'
    else:
        logger.debug('Successfull validation')
        validation = True
        issue = ''
    return validation, issue 
    