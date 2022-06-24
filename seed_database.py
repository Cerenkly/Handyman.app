import os
import json
from random import choice, randint

import crud
import model
import server

#os.system("dropdb handyman")
#os.system("createdb handyman")

model.connect_to_db(server.app)
#model.db.create_all()

cleaning = crud.create_service("cleaning")
moving = crud.create_service("moving")
painting = crud.create_service("painting")


model.db.session.add(cleaning)
model.db.session.add(moving)
model.db.session.add(painting)
model.db.session.commit()