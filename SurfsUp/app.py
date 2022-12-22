# Import Dependencies
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np

# Database setup

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Reflect existing database into new model

Base = automap_base()

#Reflect the tables

Base.prepare(autoload_with=engine)

#View all of the classes that automap found

Base.classes.keys()

#Save references to tables

measurement = Base.classes.measurement

station = Base.classes.station

# Flask setup

app = Flask(__name__)

# Flask routes

@app.route('/')
def home():
    return("Available Routes: \n 1.  /api/v1.0/precipitation \n 2. /api/v1.0/stations \n 3. /api/v1.0/tobs \n 4. /api/v1.0/<start> and /api/v1.0/<start>/<end>")


@app.route('/api/v1.0/precipitation')
def precipitation():
   
    #create session

    session = Session(engine)

    #Query

    sel_md = [measurement.date, func.sum(measurement.prcp)]
    prcp_date_data = session.query(*sel_md).filter(measurement.date >= '2016-08-23').group_by(measurement.date).order_by(measurement.date).all()
    session.close()

    #Create empty list to store dictionaries
    prcp_data_list = []

    #loop through data and append to list
    for date, prcp in prcp_date_data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_data_list.append(prcp_dict)
    return jsonify(prcp_data_list)


@app.route('/api/v1.0/stations')
def stations():
    #create session
    session = Session(engine)

    #Query
    station_names = session.query(station.name).all()

    session.close()

    station_names_list = list(np.ravel(station_names))

    return jsonify(station_names_list)

@app.route('/api/v1.0/tobs')
def tobs():

    #create session
    session = Session(engine)

    #Query
    sel = [measurement.station, measurement.tobs, measurement.date]
    full_temp_data = session.query(*sel).filter((measurement.station == 'USC00519281') & (measurement.date > '2016-08-23'))

    session.close()

    #create empty list for date/temp measurements
    tobs_list = []
    #loop through data and append to list
    for id, tobs, date in full_temp_data:
        tobs_date_dict = {}
        tobs_date_dict['date'] = date
        tobs_date_dict['tobs'] = tobs
        tobs_list.append(tobs_date_dict)

    return jsonify(tobs_list)

@app.route('/api/v1.0/<start>')
def start(start):
    #create engine
    session = Session(engine)

    sel = [measurement.station, measurement.date, func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)]
    full_temps = session.query(sel).group_by(measurement.date).filter(measurement.date > start)

    return jsonify(full_temps)









if __name__ == '__main__':
    app.run(debug=True)




