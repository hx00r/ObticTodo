import pymongo
import random
import array

from pymongo.message import query
try:
    from sec_conf import sec_settings
    mongo_server = sec_settings.MONGO_SERVER
    mongo_port = sec_settings.MONGO_PORT
except:
    print('secure config not found \n using defualt settings')
    mongo_server = 'localhost'
    mongo_port = 27019

myclient = pymongo.MongoClient(mongo_server, mongo_port) # use your own settings to connect to mongoDB
mydb = myclient['obticToDo']
# mycol = mydb[Sec_conf.MONGO_COLLECTION]
mycol = mydb['to_do_lists']

def data_key():
    MAX_LEN = 15
    DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] 
#     COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS
    COMBINED_LIST = DIGITS
    rand_digit = random.choice(DIGITS)
#     temp_key = rand_digit + rand_upper + rand_lower + rand_symbol
    temp_key = rand_digit
    for x in range(MAX_LEN - 4):
        temp_key = temp_key + random.choice(COMBINED_LIST)
        temp_pass_list = array.array('u', temp_key)
        random.shuffle(temp_pass_list)
    dataKey = ""
    for x in temp_pass_list:
            dataKey = dataKey + x    
    return dataKey

def register_v2(userID,usernameINP): # this will register a new user to the db
    query = {
    "_id": userID,
    "username":usernameINP,
    "to_do_list":[],
    }
    try:
        mycol.insert_one(query)
        return True
    except pymongo.errors.DuplicateKeyError as userExisted:
        return 'user_is_already_exists'

def find_(userID): # this is for find data from the db 
    query = {"_id":userID} # this is the query syntax
    result = mycol.find(query) # here we pass the query for the find method for the mongo db
    for i in result: # this will return the 'i' var that contains the dict of the user data
        if result: # if there any user with the same username and password then it will came true then the for loop will be true
            return i # here we will return the user data and the result var to check if its true
        else:
            return False

def find_data(userID, dataidprov, from_where): # this is for find data from the db 
    # db.users.find({'_id':19},{'data':{$elemMatch:{'dataID':'505518870'}}})
    
    query_user = {'_id':userID}
    query_array_id = {f'{from_where}':{'$elemMatch':{'dataID':dataidprov}}}
    result = mycol.find(query_user,query_array_id) # here we pass the query for the find method for the mongo db
    for i in result:
        if result:
            return i
            
def update_data(userID, DataID, array_data_to_update, **data_keys):
    """
    This function works with kwargs
    1 - you pass the dict of the keys to triger to update with value with every key
    - Example
    `
       >>> data_triger = {
        ... 'username':'username_string',
        ... 'dataName':'dataName_string',
        ... 'webUrl':'web_url_string'
        ... }
    `
    the function will loop into that dict and if the keys are correct it will update.
    """
    for key, value in data_keys.items(): # this will loop into the dict keys and values 
        query = {"_id":userID} # this for the select for the update using the user id
        newValues = { # this will set the newValues in every loop session
            "$set":
            {
                f"{array_data_to_update}.$[elem].{key}":value,
                }
            }
        filterForArray = [ # this is filtering for the ip 
            {
                "elem.dataID":DataID
            }
        ]
        mycol.update_one(query,newValues,array_filters=filterForArray) # this is the update method and it will update for every time the loop runs

def remove_data(userID,dataID, from_where):
    query = {"_id":userID} # this for the select for the update using the user id
    newValues = {"$pull":{f"{from_where}":{"dataID":dataID}}} # this is the query that we want to pass 
    mycol.update_one(query,newValues) # this is the update method

def add_to_do(userID,dataName,to_do_list_str):
    dataIdGen = data_key()
    query = {"_id":userID} # this for the select for the update using the user id
    newValues = {
        "$push":{
            "to_do_list":{
                "dataID":dataIdGen,
                "dataName":dataName,
                "isFinished":False,
                "list":to_do_list_str
            }
        }
    }
    mycol.update_one(query,newValues) # this is the update method
    return dataIdGen
def delteAccount(userID):
    query = {"_id":userID} # this for the select for the update using the user id
    mycol.delete_one(query)