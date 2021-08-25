from cerberus import Validator
import json
import os, errno

while True:
    try:
        app_id = int(input("Enter the App ID for which you are validating this data: "))
    except ValueError: 
        print("Please input an integer value")
    else:
        break

file_path = input("Enter the file name (with extension) which contains historic data: ")

schema = {
'timestamp': { 'type': 'integer', 'required': True},
'app_id': { 'type': 'integer', 'required': True, 'allowed': [app_id]},
'idfa': {'type': 'string', 'regex': '[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'},
'idfv': {'type': 'string', 'regex': '[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'},
'gaid': {'type': 'string', 'regex': '[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'},
'android_id': {'type': 'string', 'regex': '[0-9a-fA-F]{16}'},
'windows_aid': {'type': 'string', 'regex': '^[a-zA-Z0-9]+$'},
'kindle_aid': {'type': 'string'},
'developer_id': {'type': 'string'},
'touch_type': {'type': 'string', 'allowed': ['click', 'impression']},
'os_version': {'type': 'string'},
'sdk_version': {'type': 'string'},
'country_code': {'type': 'string'},
'region_name': {'type': 'string'}
}


idfa_c=0; gaid_c=0; idfv_c=0; android_id_c=0; windows_aid_c=0; kindle_aid_c=0; developer_id_c=0;
def count_devices(input):
    global idfa_c, gaid_c, idfv_c, android_id_c, windows_aid_c, kindle_aid_c, developer_id_c
    if('idfa' in input and input['idfa'] != ''):
        idfa_c += 1
    if('idfv' in input and input['idfv'] != ''):
        idfv_c += 1
    if('gaid' in input and input['gaid'] != ''):
        gaid_c += 1
    if('android_id' in input and input['android_id'] != ''):
        android_id_c += 1
    if('windows_aid' in input and input['windows_aid'] != ''):
        windows_aid_c += 1
    if('kindle_aid' in input and input['kindle_aid'] != ''):
        kindle_aid_c += 1
    if('developer_id' in input and input['developer_id'] != ''):
        developer_id_c += 1


v = Validator(schema)
file = open(file_path, 'r')
lines = file.readlines()
line_c = 0
failed_to_read_line = 0
incorrectJsonLines_c = 0
nonJsonLines = open('nonJsonLines.csv','w')
incorrectJsonLines = open('incorrectJsonLines.csv','w')


for line in lines:
    line_c += 1
    try:
        input = json.loads(line)
    except ValueError: 
        failed_to_read_line += 1
        nonJsonLines.write(line)
        nonJsonLines.write('\n')
        continue
    result = v.validate(input)
    if(result is False):
        incorrectJsonLines_c += 1
        if len(v.errors) > 0: incorrectJsonLines.write(str(v.errors))
        incorrectJsonLines.write(',')
        incorrectJsonLines.write(line)
        incorrectJsonLines.write('\n')
    if(result is True):
        count_devices(input)

        
file.close()
nonJsonLines.close()
incorrectJsonLines.close()
        
    
print("------------START OF VALIDATION------------")    

print("Total Records=", line_c)
 

if failed_to_read_line > 0: print("\nFailed to read: ", failed_to_read_line , "lines \nPlease check the file nonJsonLines.csv and check if they are in correct JSON format.")
else:
    try:
        os.remove('nonJsonLines.csv')
    except OSError:
        pass
    
if incorrectJsonLines_c > 0: print("\nA Record validation failed: ", incorrectJsonLines_c , "records \nPlease check the file incorrectJsonLines.csv and check if they are in correct format.")
else:
    try:
        os.remove('incorrectJsonLines.csv')
    except OSError:
        pass


print("\nFollowing are the valid record counts \n")
    
if (idfa_c > 0) : print("idfa =", idfa_c)
if (idfv_c > 0) : print("idfv =", idfv_c)
if (gaid_c > 0) : print("gaid =", gaid_c)
if (android_id_c > 0) : print("androidId =", android_id_c)
if (windows_aid_c > 0) : print("windows_aid =", windows_aid_c)
if (kindle_aid_c > 0) : print("kindle_aid =", kindle_aid_c)
if (developer_id_c > 0) : print("developer_id =", developer_id_c)

print("------------END OF VALIDATION------------")  
