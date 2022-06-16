import os
import json
from random import choice, randint

import crud
import model
import server

os.system("dropdb handyman")
os.system("createdb handyman")

model.connect_to_db(server.app)
model.db.create_all()