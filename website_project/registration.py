import hashlib
import json

'''
data = {"hugh.hall@epower.ie": {"access": "ALL CHARGERS", "password": ""},
        "josef.tugwell@epower.ie": {"access": "ALL CHARGERS", "password": ""},
        "douglas.hall@epower.ie": {"access": "ALL CHARGERS", "password": ""},
        "admin@epower.ie": {"access": "ALL CHARGERS", "password": ""},
        "marymount@epower.ie": {"access": ["Marymount CP1 001", "Marymount CP1 002"], "password": ""},
        "lilly.littleisland@epower.ie": {"access": ["Eli Lilly LI CP1 001", "Eli Lilly LI CP1 002", "Eli Lilly LI CP1 003"], "password": ""},
        "hovione.ringaskiddy@epower.ie": {"access": ["Hovione CP1 001", "Hovione CP1 002", "Hovione CP1 003", "Hovione CP1 004"], "password": ""},
        "shannahans@epower.ie": {"access": ["Shanahan Circle K CP1 001"], "password": ""},
        "crestsolutions@epower.ie": {"access": ["Crest CP1 001"], "password": ""}}

'''

with open('salt') as salt_file:
    salt = salt_file.read()

with open("users") as json_file:  # opening users db
    db = json.load(json_file)

# OPTION 1
#  if you want to change all passwords at once,
# please write your preferable passwords in sequence instead of numbers
'''
passwords = ['1', '2', '3', '3', '4', '5', '6', '7', '8']
count = 0
for value in db.values():
    hashed_pass = hashlib.sha256(
        f"{passwords[count]}{salt}".encode()).hexdigest()
    value['password'] = hashed_pass
    count += 1
'''
# -- end of option 1


# OPTION 2
# If you want to change the password of one user.
'''
password = "Your password"
hashed_pass = hashlib.sha256(f"{password}{salt}".encode()).hexdigest()
db["josef.tugwell@epower.ie"]['password'] = hashed_pass
'''
# -- end of option 2


# after selecting one of the aforementioned options do the following
# updating db

with open("users", "w") as f:
    json.dump(db, f, indent=2)




