from DataHelper import Location
from fastapi import FastAPI, Response
from uvicorn import run
import datetime as dt
from datetime import datetime
import persistence

from frcm.frcapi import METFireRiskAPI
from frcm.datamodel.model import Location

from persistence import PgRegistrationRepository


app = FastAPI()
db = PgRegistrationRepository()

@app.get("/checkhealth")
def read_root():
    return "alive"

@app.get("/TTF/{locationName}/{date}")
def calculateTTF(locationName: str, date: str):

    try:
        if locationName.lower() == "bergen":
            ttfLocation = Location(latitude=60.383, longitude=5.3327)
        if locationName.lower() == "haugesund":
            ttfLocation = Location(latitude=59.4225, longitude=5.2480)
        if ttfLocation ==[]:      
            ttfLocation = db.getLocation(locationName)
      
        if ttfLocation == []:
            return Response(content=f"Nothing found. Please try another location or check if spelled correct.", status_code=404)

        date = datetime.strptime(date, "%Y-%m-%d")
        
        #check if we have stored in our database before fetching from 3rd party
        TTF = db.getTTFForGivenDateAndLocation(date,locationName)
        
        if TTF != None:
            stringResponse = str(TTF.count)
            print(stringResponse)
            return Response(content="ok", status_code=200)
 
        TTF = calculateTTF(ttfLocation,date)

        #save the TTF in our own database to prevent spaming 3rd party.
        db.saveTTFForGivenDataAndLocation(date,ttfLocation, TTF)
        
        stringResponse = str(TTF)
        return Response(content=stringResponse, status_code=200)
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD"}

@app.get("/locations/{location}")
def get_location(location: str):

    if location.lower() == "bergen":
       locationDto = Location(latitude= 60.383, longitude=5.3327)
       return Response(content=f"Location data: Location name: {location}, Latitude:{locationDto.latitude}, Longitude: {locationDto.longitude} ", status_code=200)
       
    if location.lower() == "haugesund":
        locationDto = Location(latitude=60.383, longitude=5.3327)
        return Response(content=f"{locationDto}", status_code=200)

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

def calculateTTF(location, date):
    
    #Guard this with a static response
    return 5.55
    
    frc = METFireRiskAPI(date, location)
    #obs_delta = datetime.timedelta(days=2)

    return frc.compute_now(location, date)

def main():
    run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
