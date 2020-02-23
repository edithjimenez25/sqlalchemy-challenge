### Step 2 - Climate App - Flask API
# Import Dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy import inspect
from sqlalchemy import Column, Integer, String, Float, Text

from pprint import pprint

from flask import Flask, jsonify

import datetime as dt

import numpy as np
import pandas as pd


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Create a session (link) from Python to the Database
session = Session(engine)

# Save references to the invoices and invoice_items tables
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################

# Flask Setup
app = Flask(__name__)


# Flask Route All

@app.route("/")

def wELCOME():
    """List all available api routes."""
    return (
        f"<h1>Climate Analysis</h1><br/><br/>"
        f"Available Routes:<br/>"
        """<a href="/api/v1.0/stations">/api/v1.0/stations (List of Stations)</a><br/>"""
        """<a href="/api/v1.0/tobs">/api/v1.0/tobs (Temperature observations for the previous year)</a><br/>"""
        """<a href="/api/v1.0/precipitation">/api/v1.0/precipitation (Precipitation from 08/21/2016 to 08/23/17)</a><br/>"""
        """<a href="/api/v1.0/2016-08-23/2017-08-23">/api/v1.0/date_start/date_end (Temperature on the range)</a><br/>"""
    )


########## Flask Route Station #################

def stations():
    # Function returns a json list of stations from the dataset
    
    # Query database for stations
    stations = session.query(Station.station).all()
    
    # Convert object to a list
    station_list=[]
    for sublist in stations:
        for item in sublist:
            station_list.append(item)
    
    # Return jsonified list
    return (jsonify(station_list))


# Flask Route Temperature Observations############
@app.route("/api/v1.0/tobs")

def tobs():
    # Function returns a json list of Temperature Observations (tobs) for the previous year
    
    # Calulate the date 1 year ago from today
    year_ago_dt = dt.date.today() - dt.timedelta(days=365)
    
    # Query database for stations
    tobs = session.query(Measurement.date, Measurement.tobs)\
            .filter(Measurement.date >= year_ago_dt)\
            .order_by(Measurement.date).all()
    
    # Convert object to a list
    tobs_list=[]
    for sublist in tobs:
        for item in sublist:
            tobs_list.append(item)
    
    # Return jsonified list
    return (jsonify(tobs_list))

# Flask Route Precipitation####################
@app.route("/api/v1.0/precipitation")

def precipitation():
    # Function returns a json dictionary of dates and precipitation from the last year
    
    # Calulate the date 1 year ago from today
    year_ago_dt = dt.date.today() - dt.timedelta(days=365)
    
    # Query database for stations
    prcp = session.query(Measurement.date, Measurement.prcp)\
            .filter(Measurement.date >= year_ago_dt)\
            .order_by(Measurement.date).all()
    
    # Convert object to a list
    prcp_list={}
    for item in prcp:
        prcp_list[item[0]]=item[1]
    
    # Return jsonified list
    return (jsonify(prcp_list))


# Flask Route Start###########################
@app.route("/api/v1.0/<start_date>")

def start_temp(start):
    # get the min/avg/max
    temp_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), \
                              func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    
    return jsonify(temp_data)

# Flask Route Start Date - End Date ###############
@app.route("/api/v1.0/<date_start>/<date_end>")

def temp_stats(date_start, date_end=0):
    # Function returns a json list of the minimum, average and maximum temperature for a given date range

    # If no end date, then make end date today's date so it is all inclusive
    if date_end == 0:
        date_end = dt.date.today()
    
    # Query database for tobs between start and end date
    tobs = session.query(Measurement.tobs)\
            .filter(Measurement.date >= date_start)\
            .filter(Measurement.date <= date_end).all()
   
    # Convert results to dataframe
    tobs_df = pd.DataFrame(tobs, columns=['tobs'])
    
    # Append integer versions of each item (can't JSONify numpy class) into a list
    tobs_list = []
    tobs_list.append(np.asscalar(np.int16(tobs_df['tobs'].min())))
    tobs_list.append(np.asscalar(np.int16(tobs_df['tobs'].mean())))
    tobs_list.append(np.asscalar(np.int16(tobs_df['tobs'].max())))
    
    # Return JSONified list of minimum, average and maximum temperatures
    return (jsonify(tobs_list))

if __name__ == "__main__":
    app.run(debug=True)