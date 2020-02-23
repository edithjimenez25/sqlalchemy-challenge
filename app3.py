{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": "* Serving Flask app \"__main__\" (lazy loading)\n * Environment: production\n   WARNING: This is a development server. Do not use it in a production deployment.\n   Use a production WSGI server instead.\n * Debug mode: on\n * Restarting with stat\n"
    },
    {
     "ename": "SystemExit",
     "evalue": "1",
     "output_type": "error",
     "traceback": [
      "An exception has occurred, use %tb to see the full traceback.\n",
      "\u001b[1;31mSystemExit\u001b[0m\u001b[1;31m:\u001b[0m 1\n"
     ]
    }
   ],
   "source": [
    "### Step 2 - Climate App - Flask API\n",
    "# Import Dependencies\n",
    "import numpy as np\n",
    "\n",
    "import sqlalchemy\n",
    "from sqlalchemy.ext.automap import automap_base\n",
    "from sqlalchemy.orm import Session\n",
    "from sqlalchemy import create_engine\n",
    "from sqlalchemy import func\n",
    "from sqlalchemy import inspect\n",
    "from sqlalchemy import Column, Integer, String, Float, Text\n",
    "\n",
    "from pprint import pprint\n",
    "\n",
    "from flask import Flask, jsonify\n",
    "\n",
    "import datetime as dt\n",
    "\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "\n",
    "%matplotlib inline\n",
    "from matplotlib import style\n",
    "style.use('fivethirtyeight')\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "\n",
    "#################################################\n",
    "# Database Setup\n",
    "#################################################\n",
    "engine = create_engine(\"sqlite:///Resources/hawaii.sqlite\")\n",
    "\n",
    "# reflect an existing database into a new model\n",
    "Base = automap_base()\n",
    "\n",
    "# reflect the tables\n",
    "Base.prepare(engine, reflect=True)\n",
    "\n",
    "# Create a session (link) from Python to the Database\n",
    "session = Session(engine)\n",
    "\n",
    "# Save references to the invoices and invoice_items tables\n",
    "Measurement = Base.classes.measurement\n",
    "Station = Base.classes.station\n",
    "\n",
    "#################################################\n",
    "# Flask Setup\n",
    "#################################################\n",
    "\n",
    "# Flask Setup\n",
    "app = Flask(__name__)\n",
    "\n",
    "\n",
    "# Flask Route All\n",
    "\n",
    "@app.route(\"/\")\n",
    "\n",
    "def wELCOME():\n",
    "    \"\"\"List all available api routes.\"\"\"\n",
    "    return (\n",
    "        f\"<h1>Climate Analysis</h1><br/><br/>\"\n",
    "        f\"Available Routes:<br/>\"\n",
    "        \"\"\"<a href=\"/api/v1.0/stations\">/api/v1.0/stations (List of Stations)</a><br/>\"\"\"\n",
    "        \"\"\"<a href=\"/api/v1.0/tobs\">/api/v1.0/tobs (Temperature observations for the previous year)</a><br/>\"\"\"\n",
    "        \"\"\"<a href=\"/api/v1.0/precipitation\">/api/v1.0/precipitation (Precipitation from 08/21/2016 to 08/23/17)</a><br/>\"\"\"\n",
    "        \"\"\"<a href=\"/api/v1.0/2016-08-23/2017-08-23\">/api/v1.0/date_start/date_end (Temperature on the range)</a><br/>\"\"\"\n",
    "    )\n",
    "\n",
    "\n",
    "########## Flask Route Station #################\n",
    "\n",
    "def stations():\n",
    "    # Function returns a json list of stations from the dataset\n",
    "    \n",
    "    # Query database for stations\n",
    "    stations = session.query(Station.station).all()\n",
    "    \n",
    "    # Convert object to a list\n",
    "    station_list=[]\n",
    "    for sublist in stations:\n",
    "        for item in sublist:\n",
    "            station_list.append(item)\n",
    "    \n",
    "    # Return jsonified list\n",
    "    return (jsonify(station_list))\n",
    "\n",
    "\n",
    "# Flask Route Temperature Observations############\n",
    "@app.route(\"/api/v1.0/tobs\")\n",
    "\n",
    "def tobs():\n",
    "    # Function returns a json list of Temperature Observations (tobs) for the previous year\n",
    "    \n",
    "    # Calulate the date 1 year ago from today\n",
    "    year_ago_dt = dt.date.today() - dt.timedelta(days=365)\n",
    "    \n",
    "    # Query database for stations\n",
    "    tobs = session.query(Measurement.date, Measurement.tobs)\\\n",
    "            .filter(Measurement.date >= year_ago_dt)\\\n",
    "            .order_by(Measurement.date).all()\n",
    "    \n",
    "    # Convert object to a list\n",
    "    tobs_list=[]\n",
    "    for sublist in tobs:\n",
    "        for item in sublist:\n",
    "            tobs_list.append(item)\n",
    "    \n",
    "    # Return jsonified list\n",
    "    return (jsonify(tobs_list))\n",
    "\n",
    "# Flask Route Precipitation####################\n",
    "@app.route(\"/api/v1.0/precipitation\")\n",
    "\n",
    "def precipitation():\n",
    "    # Function returns a json dictionary of dates and precipitation from the last year\n",
    "    \n",
    "    # Calulate the date 1 year ago from today\n",
    "    year_ago_dt = dt.date.today() - dt.timedelta(days=365)\n",
    "    \n",
    "    # Query database for stations\n",
    "    prcp = session.query(Measurement.date, Measurement.prcp)\\\n",
    "            .filter(Measurement.date >= year_ago_dt)\\\n",
    "            .order_by(Measurement.date).all()\n",
    "    \n",
    "    # Convert object to a list\n",
    "    prcp_list={}\n",
    "    for item in prcp:\n",
    "        prcp_list[item[0]]=item[1]\n",
    "    \n",
    "    # Return jsonified list\n",
    "    return (jsonify(prcp_list))\n",
    "\n",
    "\n",
    "# Flask Route Start###########################\n",
    "@app.route(\"/api/v1.0/<start_date>\")\n",
    "\n",
    "def start_temp(start):\n",
    "    # get the min/avg/max\n",
    "    temp_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), \\\n",
    "                              func.max(Measurement.tobs)).filter(Measurement.date >= start).all()\n",
    "    \n",
    "    return jsonify(temp_data)\n",
    "\n",
    "# Flask Route Start Date - End Date ##############\n",
    "@app.route(\"/api/v1.0/<date_start>/<date_end>\")\n",
    "\n",
    "def temp_stats(date_start, date_end=0):\n",
    "    # Function returns a json list of the minimum, average and maximum temperature for a given date range\n",
    "\n",
    "    # If no end date, then make end date today's date so it is all inclusive\n",
    "    if date_end == 0:\n",
    "        date_end = dt.date.today()\n",
    "    \n",
    "    # Query database for tobs between start and end date\n",
    "    tobs = session.query(Measurement.tobs)\\\n",
    "            .filter(Measurement.date >= date_start)\\\n",
    "            .filter(Measurement.date <= date_end).all()\n",
    "   \n",
    "    # Convert results to dataframe\n",
    "    tobs_df = pd.DataFrame(tobs, columns=['tobs'])\n",
    "    \n",
    "    # Append integer versions of each item (can't JSONify numpy class) into a list\n",
    "    tobs_list = []\n",
    "    tobs_list.append(np.asscalar(np.int16(tobs_df['tobs'].min())))\n",
    "    tobs_list.append(np.asscalar(np.int16(tobs_df['tobs'].mean())))\n",
    "    tobs_list.append(np.asscalar(np.int16(tobs_df['tobs'].max())))\n",
    "    \n",
    "    # Return JSONified list of minimum, average and maximum temperatures\n",
    "    return (jsonify(tobs_list))\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    app.run(debug=True)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.4-final"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}