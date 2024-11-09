# Import the dependencies.
import datetime as dt
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
Base.prepare(autoload_with=engine)

# Saved each references to a table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

# Route to retrieve precipitation data
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Query the most recent date in the database
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    # Extract the date as a string
    most_recent_date_str = most_recent_date[0]

    # Parse the string to a datetime object
    most_recent_date_dt = dt.datetime.strptime(most_recent_date_str, '%Y-%m-%d')
    
    # Calculate the date one year before the most recent date
    one_year_ago = most_recent_date_dt - dt.timedelta(days=365)
    
    # Query for the last 12 months of precipitation data
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago - dt.timedelta(days=1)).all()
    
    # Closing the session after querying
    session.close()
    
    # Create a dictionary with date as key and prcp as value
    precipitation_data = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp

        precipitation_data.append(precipitation_dict)
    
    return jsonify(precipitation_data)

# Route to retrieve all station data
@app.route("/api/v1.0/stations")
def station():

    # Query all stations in the database
    results = session.query(Station.station).all()

    # Closing the session after querying
    session.close()
    
    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))
    
    return jsonify(all_stations)

# Route to retrieve temperature observations for the most active station
@app.route("/api/v1.0/tobs")
def tobs():
    
    # Get the most active station and the last date in data
    most_active_station = session.query(Measurement.station).\
            group_by(Measurement.station).\
            order_by(func.count().desc()).first()

    # Extract the station as a string
    most_active_station_str = most_active_station[0]

     # Query the most recent date in the database
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    # Extract the date as a string
    most_recent_date_str = most_recent_date[0]

    # Parse the string to a datetime object
    most_recent_date_dt = dt.datetime.strptime(most_recent_date_str, '%Y-%m-%d')
    
    # Calculate the date one year before the most recent date
    one_year_ago = most_recent_date_dt - dt.timedelta(days=365)
    
    # Query temperature observations for the most active station in the last year
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station_str).\
        filter(Measurement.date >= one_year_ago - dt.timedelta(days=1)).all()

    # Closing the session after querying 
    session.close()
    

    # Create a dictionary with date as key and prcp as value
    tobs_data = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs

        tobs_data.append(tobs_dict)
    
    return jsonify(tobs_data)

# Route to retrieve min, avg, and max temperatures from a start date
@app.route("/api/v1.0/<start>")
def starts(start=None, end=None):

     # Define query functions for min, avg, and max temperatures
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    # Query temperature stats from the start date
    results = session.query(*sel).filter(Measurement.date >= start).all()        
    
    # Closing the session after querying
    session.close()
    
    # Create a list to hold the stats data
    stats_data = []
    for tmin, tavg, tmax  in results:
        stats_dict = {}
        stats_dict["TMIN"] = tmin
        stats_dict["TAVG"] = tavg
        stats_dict["TMAX"] = tmax

        stats_data.append(stats_dict)
    
    return jsonify(stats_data)

# Route to retrieve min, avg, and max temperatures for a specific date range
@app.route("/api/v1.0/<start>/<end>")
def date_range(start=None, end=None):

    # Define query functions for min, avg, and max temperatures
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    # Query temperature stats within the specified date range
    results = session.query(*sel).filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()

    # Closing the session after querying   
    session.close()
    
    # Create a list to hold the stats data
    stats_data = []
    for tmin, tavg, tmax  in results:
        stats_dict = {}
        stats_dict["TMIN"] = tmin
        stats_dict["TAVG"] = tavg
        stats_dict["TMAX"] = tmax

        stats_data.append(stats_dict)
    
    return jsonify(stats_data)


if __name__ == '__main__':
    app.run(debug=True)