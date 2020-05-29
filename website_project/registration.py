import hashlib
import json

# '''
# data = {"hugh.hall@epower.ie": {"access": "ALL CHARGERS", "password": ""},
#         "josef.tugwell@epower.ie": {"access": "ALL CHARGERS", "password": ""},
#         "douglas.hall@epower.ie": {"access": "ALL CHARGERS", "password": ""},
#         "admin@epower.ie": {"access": "ALL CHARGERS", "password": ""},
#         "marymount@epower.ie": {"access": ["Marymount CP1 001", "Marymount CP1 002"], "password": ""},
#         "lilly.littleisland@epower.ie": {"access": ["Eli Lilly LI CP1 001", "Eli Lilly LI CP1 002", "Eli Lilly LI CP1 003"], "password": ""},
#         "hovione.ringaskiddy@epower.ie": {"access": ["Hovione CP1 001", "Hovione CP1 002", "Hovione CP1 003", "Hovione CP1 004"], "password": ""},
#         "shannahans@epower.ie": {"access": ["Shanahan Circle K CP1 001"], "password": ""},
#         "crestsolutions@epower.ie": {"access": ["Crest CP1 001"], "password": ""}}
#
#
# with open("users","w") as json_file:
#         json.dump(data, json_file)
# '''
#
# with open('salt') as salt_file:
#     salt = salt_file.read()
#     print(salt)
#
# with open("users") as json_file:
#     db = json.load(json_file)
# passwords = ['k4$32F^QBm2', 'aCAE%9Eg6l$', '97jx&9TLTls', 'u8o$PwR2ubE',
#              '3C6YMj!N*yP', '@04XPs7BOul', 'tQs9&48^o1f',
#              'iQXtk07@GR%', 'Eg26w^Gvc9y']
# count = 0
# for value in db.values():
#     hashed_pass = hashlib.sha256(
#         f"{passwords[count]}{salt}".encode()).hexdigest()
#     value['password'] = hashed_pass
#     count+=1
#
# # updating db
# with open("users", "w") as f:
#     json.dump(db, f, indent=2)




# with open("users") as json_file:
#     db = json.load(json_file)
# c = 1
# for i in db.values():
#     i['id'] = c
#     c += 1
# with open("users", "w") as f:
#     json.dump(db, f, indent=2)



