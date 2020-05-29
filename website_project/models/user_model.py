# from website_project import db
import hashlib

# with open('salt') as salt_file:
#     salt = salt_file.read()

import json

with open('users') as json_file:
    db = json.load(json_file)


salt = '2f546fa116533c013fceb653c20ef64f'


class User:
    def __init__(self, email):
        self.email = email

    @staticmethod
    def check_user_password(email, password):
        user = db.get(email)
        if user:
            pass_hash = hashlib.sha256(
                f"{password}{salt}".encode()).hexdigest()
            stored_password = user['password']
            if pass_hash == stored_password:
                return True
            else:
                return False
        return False

    @staticmethod
    def get_access(email):
        charging_station_names = ["Rockgrove CP1 001", "Marymount CP1 001",
                                  "Marymount CP1 002", "Eli Lilly LI CP1 001",
                                  "Eli Lilly LI CP1 002",
                                  "Eli Lilly LI CP1 003",
                                  "Shanahan Circle K CP1 001",
                                  "Hovione CP1 001",
                                  "Hovione CP1 002", "Hovione CP1 003",
                                  "Hovione CP1 004", "Crest CP1 001"]

        access = db.get(email)['access']
        if access == "ALL CHARGERS":
            return charging_station_names
        else:
            return access

    @staticmethod
    def get_company_name(email):
        return db.get(email)['company_name']
