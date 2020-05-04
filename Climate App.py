import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

###Design a query to retrieve the last 12 months of precipitation data.###
###Convert the query results to a dictionary using `date` as the key and `prcp` as the value.###
###Return the JSON representation of your dictionary.###
@app.route("/api/v1.0/precipitation")
def precipation():

    session = Session(engine)

    precip_data = session.query(func.strftime("%Y-%m-%d", Measurement.date), Measurement.prcp).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= "2016-08-23").\
        group_by(Measurement.date).\
        order_by(Measurement.date).all()

    all_precipitation_totals = []
    for result in precip_data:
        row = {}
        row["date"] = rain[0]
        row["prcp"] = rain[1]
        rain_totals.append(row)

    return jsonify(all_precipitation_totals)

###Return a JSON list of stations from the dataset.###
@app.route("/api/v1.0/stations")
def stations():
   
    session = Session(engine)

    results = session.query(Measurement.station).all()

    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

###Query the dates and temperature observations of the most active station for the last year of data.### 
###Return a JSON list of temperature observations (TOBS) for the previous year.###
@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    station_temperature = session.query(Measurements.date, Measurements.tobs).filter(Measurement.station == "USC00519281").\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= "2016-08-23").all()
    
    all_temperatures = []
    for result in station_temperature:
        row = {}
        row["date"] = temperature[0]
        row["tobs"] = temperature[1]
        all_temperatures.append(row)

    return jsonify(all_temperatures)

###Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.###
###When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.###
###When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.###
@app.route("/api/v1.0/<start><br/>")
def temps1(start):

    session = Session(engine)

    temps = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= "2016-08-23").all()
    
    session.close()

    all_temps = list(np.ravel(temps))

    return jsonify(all_temps) 

@app.route("/api/v1.0/<start>/<end><br/>")
def temps2(start,end):

    session = Session(engine)

    temps = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= "2016-08-23").filter(func.strftime("%Y-%m-%d", Measurement.date) <= "2017-08-23").all()
    
    session.close()

    all_temps = list(np.ravel(temps))

    return jsonify(all_temps)


if __name__ == '__main__':
    app.run(debug=True)