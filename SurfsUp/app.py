# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
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
Base.prepare(autoload_with=engine)


# Save references to each table
Station = Base.classes.station
Measurements = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)
    
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
        f"/api/v1.0/<start>/<end>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    
# Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.

    sel = [Measurements.date, Measurements.prcp]
    query_date=dt.date(2017,8,23) - dt.timedelta(days=365)
    Rain = session.query(*sel).\
        filter(Measurements.date.between(query_date, '2017-08-23')).\
        order_by(Measurements.date)\
        .all()
    
    prcp_dict ={}
    for day,drop in Rain:
        prcp_dict[day] = drop
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():

# Return a JSON list of stations from the dataset.

   stations_list=session.query(Station.station).all()
   all_stations = []
   for x in stations_list:
       all_stations += x
   return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
# Query the dates and temperature observations of the most-active station for the previous year of data.
    subq = session.query(Station.station, func.count(Measurements.station)).\
        join(Measurements, Station.station == Measurements.station).\
        group_by(Station.station).\
        order_by(func.count(Measurements.station).desc()).first()

    most_active = subq[0]

    query = session.query(func.min(Measurements.tobs), func.max(Measurements.tobs), func.avg(Measurements.tobs)).\
        select_from(Measurements).\
        join(Station, Station.station == Measurements.station).\
        filter(Station.station ==most_active).all()
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    tobs = session.query(Measurements.tobs).\
        filter(Measurements.station == most_active).\
        filter(Measurements.date >= query_date).all()
    # Return a JSON list of temperature observations for the previous year.
    tobs_list = []
    for y in tobs:
        tobs_list += y
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start(start):
    start_query= session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs).\
                     filter(Measurements.date == start)).all()
# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
    start_list =[]    
    for a, b, c in start_query:
       start_list += [a, b,c]
    return jsonify(start_list)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    start_end_query= session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs).\
                     filter(Measurements.date >= start).\
                     filter(Measurements.date <= end)) .all()

# For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
    start_end_list =[]    
    for a, b, c in start_end_query:
       start_end_list += [a, b,c]
    return jsonify(start_end_list)

# @app.route("/api/v1.0/<start>/<end>)
# def end():    
 
if __name__ == "__main__":
    app.run(debug=True)
