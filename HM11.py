from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")
print("Connected to DB")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
Base.classes.keys()
Measurements = Base.classes.measurements
Stations = Base.classes.stations
# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup

app = Flask(__name__)



@app.route("/")
def welcome():
    """List all available api routes."""
    return ("Available Routes:<br/> \
            /api/v1.0/precipitation<br/> \
            /api/v1.0/stations<br/> \
            /api/v1.0/tobs<br/> \
            /api/v1.0/start<br/> \
            /api/v1.0/start/end_date \
            ")


@app.route("/api/v1.0/precipitation")
def precipitation():
    """ Return tobs in the last 12 months """
    results = session.query(Measurements.date, Measurements.station, Measurements.tobs). \
            filter(Measurement.date.between('2016-06-06', '2017-06-23')). \
            group_by(Measurement.date).order_by(Measurement.date).all()

    
    tobs_data = []
    for rec in range(len(results)):
        tobs_dict = {}
        tobs_dict['date'] = results[rec][0]
        tobs_dict['temp'] = results[rec][2]
        tobs_data.append(tobs_dict)
    return jsonify(tobs_data)
    # return tobs_data

    return jsonify(all_names)

@app.route("/api/v1.0/stations")
def stations():
    """Return the json list of all stations in the data set"""
    all_stations = session.query(Stations.station, Stations.name).all()

    stations_data = []
    for rec in range(len(all_stations)):
        station_dict = {}
        station_dict['station_id'] = all_stations[rec][0]
        station_dict['name'] = all_stations[rec][1]
        stations_data.append(station_dict)
    
    return jsonify(stations_data)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return the json list of tobs for the last 12 months"""
    last12_tobs = session.query(Measurements.date, Measurements.station, Measurements.tobs).\
               filter(Measurements.date.between('2016-08-24', '2017-08-23')).\
               group_by(Measurements.date).order_by(Measurements.date).all()

    tobs_data = []
    for rec in range(len(last12_tobs)):
        tobs_dict = {}
        tobs_dict['date'] = last12_tobs[rec][0]
        tobs_dict['temp'] = last12_tobs[rec][2]
        tobs_data.append(tobs_dict)
    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def temp_range(start):
    """Return the json list of min, average and max temperature for a given date"""
    min_temp = session.query(func.min(Measurements.tobs)).\
               filter(Measurements.date == start).first()
    avg_temp = session.query(func.avg(Measurements.tobs)).\
               filter(Measurements.date == start).first()
    max_temp = session.query(func.max(Measurements.tobs)).\
               filter(Measurements.date == start).first()

    tobs_data = [min_temp, avg_temp, max_temp]
    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>/<end_date>")
def temp_ranges(start, end_date):
    """Return the json list of min, average and max temperature for a given date range"""
    min_temp = session.query(func.min(Measurements.tobs)).\
               filter(Measurements.date.between(start, end_date)).first()
    avg_temp = session.query(func.avg(Measurements.tobs)).\
               filter(Measurements.date.between(start, end_date)).first()
    max_temp = session.query(func.max(Measurements.tobs)).\
               filter(Measurements.date.between(start, end_date)).first()
    
    tobs_data = [min_temp, avg_temp, max_temp]
    return jsonify(tobs_data)


if __name__ == "__main__":
    app.run(debug=False)