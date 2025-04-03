from DataHelper import Location, Registration
from fastapi import FastAPI, Response
from uvicorn import run
import datetime
import persistence

from frcm.frcapi import METFireRiskAPI
from frcm.datamodel.model import Location

from persistence import PgRegistrationRepository


app = FastAPI()
db = PgRegistrationRepository()

@app.get("/checkhealth")
def read_root():
    return "alive"

# @app.get("/TTF/{location}/{date}")
# def calculateTTF(location: str, date: datetime):

#     if location.lower() == "bergen":
#        ttfLocation = Location(60.383,5.3327)

#     if location.lower() == "haugesund":
#         ttfLocation = Location(latitude=59.4225, longitude=5.2480)
#     else: 
#         #Do a db call

#         #If db call returning 0 results:
#         return Response(content=f"Nothing found. Please try another location or check if spelled correct.", status_code=404)

#     #check if we have stored in our database before fetching from 3rd party

#     TTF = db.getTTFForGivenDateAndLocation(date,location)
#     if TTF == 0:
#         TTF = calculateTTF(ttfLocation,date)

#     #save the TTF in our own database to prevent spaming 3rd party.
#     db.saveTTFForGivenDataAndLocation(date,location, TTF)

#     return Response(content=TTF, status_code=200)

@app.get("/locations/{location}")
def get_location(location: str):

    if location.lower() == "bergen":
       locationDto = Location(latitude= 60.383, longitude=5.3327)
       return Response(content=f"Location data: Location name: {location}, Latitude:{locationDto.latitude}, Longitude: {locationDto.longitude} ", status_code=200)
       
    if location.lower() == "haugesund":
        locationDto = Location(60.383,5.3327)
        return Response(content=f"{locationDto}", status_code=200)

    locationFromDb = db.getLocation(location)
    print(locationFromDb)
    if (locationFromDb) != []:
        return Response(content=f"{locationFromDb}", status_code=200)
    else:
        return Response(content=f"Unknown location: {location}. Please add it if needed.", status_code=404)


@app.post("/locations/{location}")
def make_registrations(locationName: str, latitude:float, longitude:float):
    #TODO to db

    #check if already exists in db

    locationExists = db.getLocation(location)

    if locationExists != []:
        return Response("Location already exists", status_code=404)
    else:
        db.addLocation(locationName,latitude,longitude)
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


def calculateTTF(location, date):
    frc = METFireRiskAPI(date, location)
    #obs_delta = datetime.timedelta(days=2)

    return frc.compute_now(location, date)

def main():
    run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
