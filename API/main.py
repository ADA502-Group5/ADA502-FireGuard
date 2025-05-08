from fastapi import FastAPI, Response, Depends
from uvicorn import run
import datetime as dt
from datetime import datetime
from frcm.frcapi import METFireRiskAPI
from frcm.datamodel.model import Location
from persistence import PgRegistrationRepository
from DataHelper import User


from kc.auth import verify_admin_role,verify_sadmin_role

app = FastAPI()
db = PgRegistrationRepository()

@app.get("/checkhealth")
def read_root():
    return "alive"

@app.get("/TTF/{locationName}/{date}")
def getTTFCalculation(locationName: str, date: str):
         
    ttfLocation = db.getLocation(locationName)
      
    if ttfLocation == []:
        return Response(content=f"Nothing found. Please try another location or check if spelled correct.", status_code=404)

    date = datetime.strptime(date, "%Y-%m-%d-%H-%M-%S")
       
    #check if we have stored in our database before fetching from 3rd party
    TTF = db.getTTFForGivenDateAndLocation(date,locationName)
        
    if TTF != []:
        stringResponse = str(TTF)
        print(stringResponse)
        return Response(content=stringResponse, status_code=200)

    locationDTO = Location(latitude=ttfLocation[1], longitude=ttfLocation[2])
        
    TTF = calculateTTF(locationDTO,date)
    print(TTF)
    #save the TTF in our own database to prevent spaming 3rd party.
    db.saveTTFForGivenDataAndLocation(date,locationName, TTF)
        
    stringResponse = str(TTF)
    return Response(content=stringResponse, status_code=200)


@app.get("/locations/{location}")
def get_location(location: str, user: bool=Depends(verify_admin_role)):

    locationFromDb = db.getLocation(location)
    print(locationFromDb)
    if (locationFromDb) != []:
        return Response(content=f"{locationFromDb}", status_code=200)
    else:
        return Response(content=f"Unknown location: {location}. Please add it if needed.", status_code=404)


@app.post("/location/{locationName}")
def create_location(locationName:str, location:Location):
    #check if already exists in db

    locationExists = db.getLocation(locationName)

    if locationExists != []:
        return Response("Location already exists", status_code=404)
    else:
        db.createLocation(locationName,location.latitude,location.longitude)
        return Response(content=f"Added location {locationName}", status_code=201)


# # @app.delete("/locations/{location}/registrations/{registration}")
# # def delete_registration(location: str, registration: int):
# #     #Todo to db
# #     if location in location_map:
# #         loc = location_map[location]
# #         for r in p.read_registrations():
# #             if r.id == registration and r.location_name == location:
# #                 loc.registrations.remove(r)
# #                 p.delete_registration(r)

#TODO add crud for users

@app.get("/user/{user_email}")
def getUser(user_email:str):
    
    if "@" not in user_email:
        return Response(content="Email is not valid.", status_code = 404)
    
    user = db.getUser(user_email)

    if user is None:
        return Response (content= "User not found", status_code=200)

    return Response(content=user, status_code = 200)


@app.post("/user/")
def postUser(user:User):
    
    if "@" not in user.user_email:
        return Reponse(content="Email is not valid. User was not saved.", status_code =404)
    if len(user.user_email) > 50:
        return Response(content="Email is too long", status_code=404)
    if len(user.user_name) > 50:
        return Response(content="Username is too long", status_code=404)
    
    locationFromDb = db.getLocation(user.user_location.city)

    if locationFromDb == []:
        return Response (content="Location does not exist. Please try again", status_code=404)
    
    userExists = db.getUser(user.user_email)

    if userExists != None:
        return Response (content="User already exisits", status_code=404)
   
    db.saveUser(user)

    return Response(content="User created successfully", status_code =200)


def calculateTTF(location:Location, date):
    
    
    print(location.latitude)
    #Guard this with a static response
    #return 5.55
    frc = METFireRiskAPI()

    obs_delta = dt.timedelta(days=2)  
    result = frc.compute_now(location,obs_delta)

    print(result.firerisks)
    print(result.location)

    return result.firerisks

def main():
    run(app, host="0.0.0.0", port=9000)


if __name__ == "__main__":
    main()
