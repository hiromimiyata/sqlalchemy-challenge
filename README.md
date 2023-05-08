# sqlalchemy-challenge
Goal: To perform a climate analysis. 

Part 1: Analyzed and Explored the Climate Data
I used Python and SQLAlchemy to perform a basic climate analysis and data exploration of a climate database. To do this, I followed the steps below:

I used the SQLAlchemy create_engine() function to connect to the SQLite database.
I used the SQLAlchemy automap_base() function to reflect the tables into classes, and saved references to the classes named station and measurement.
I linked Python to the database by creating a SQLAlchemy session.
I performed a precipitation analysis by finding the most recent date in the dataset, querying the previous 12 months of precipitation data, selecting only the "date" and "prcp" values, loading the query results into a Pandas DataFrame, explicitly setting the column names, sorting the DataFrame values by "date", and plotting the results using the DataFrame plot method. I also used Pandas to print the summary statistics for the precipitation data.
I performed a station analysis by designing queries to calculate the total number of stations in the dataset, find the most-active stations (that is, the stations that have the most rows), calculate the lowest, highest, and average temperatures that filters on the most-active station id found in the previous query, and get the previous 12 months of temperature observation (TOBS) data by filtering by the station that has the greatest number of observations and querying the previous 12 months of TOBS data for that station. I plotted the results as a histogram with bins=12 and closed the session.
Part 2: Designed My Climate App
After completing the initial analysis, I designed a Flask API based on the queries that I developed by creating the following routes:

"/" to start at the homepage and list all the available routes.
"/api/v1.0/precipitation" to convert the query results from the precipitation analysis to a dictionary using date as the key and prcp as the value and return the JSON representation of the dictionary.
"/api/v1.0/stations" to return a JSON list of stations from the dataset.
"/api/v1.0/tobs" to query the dates and temperature observations of the most-active station for the previous year of data and return a JSON list of temperature observations for the previous year.
"/api/v1.0/<start>" and "/api/v1.0/<start>/<end>" to return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range. For a specified start, I calculated TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date. For a specified start date and end date, I calculated TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
