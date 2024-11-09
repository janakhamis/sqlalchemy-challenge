# Sqlachemy Project

This project involves climate analysis and exploration of weather dataset using SQLAlchemy, Pandas, and Flask. The project is designed to give insights into precipitation and temperature patterns using a SQLite database and a Flask API for simple data access (Module 10 Challenge).

## Project Overview

### 1. Database Connection
- •	Connected to SQLite Database: Used SQLAlchemy's create_engine() to connect and automap_base() to reflect tables.
- References and Session: Created references to station and measurement tables and established a session for querying.


### 2. Data Analysis

#### Precipitation Analysis
- Queried the latest date in the dataset (8/23/2017).
- Retrieved date and precipitation data for the last year, stored in a Pandas DataFrame.
- Plotted precipitation over time and provided summary statistics.


#### Station Analysis
- Counted the number of unique stations and identified the most active station.
- For the most active station, calculated min, max, and average temperatures.
- Retrieved the last year of temperature data for the most active station and created a histogram.


### 3. Flask API

Developed a Flask API with the following routes:

- **/** : Homepage with a list of available routes.
- **/api/v1.0/precipitation** : Returns JSON data of the last 12 months of precipitation.
- **/api/v1.0/stations** : Returns a JSON list of all stations.
- **/api/v1.0/tobs** : Provides temperature observations for the most active station for the past year.
- **/api/v1.0/<start>** and **/api/v1.0/<start>/<end>** : Returns the minimum, average, and maximum temperatures for specified date ranges.

## How to Run

 1. Clone the repository:
       1. Open your terminal (Git Bash, Command Prompt, or any Git client).
       2. Use the cd command to navigate to the directory where you want to clone the repository.
       3. Run the following command to clone the repository: git clone link_provided

  2. Ensure Pandas, Matplotlib, Scipy, Numpy, and Sqlalchemy is installed on your machine.
     - Install Pandas using pip if it's not already installed (pip install pandas).
     - Install Matplotlib using pip if it's not already installed (pip install matplotlib).
     - Install SciPy using pip if it's not already installed (pip install scipy).
     - Install NumPy using pip if it's not already installed (pip install numpy).
     - Install NumPy using pip if it's not already installed (pip install sqlalchemy).

  3. Open the cloned file in the Visual Studio Code:
       1. Go to file > Open Folder and navigate to the folder where you cloned the repository.
       2. Select the folder to open in VS code.

  4. Run the Jupyter Notebook
     1. Open the notebook file (climate_starter.ipynb) in VS code or Jupyter.
     2. Run the cells to perform the Analysis.
        
  5. Run the Flask API
     - Open the terminal in VS Code or your preferred terminal.
     - Navigate to the directory containing the Flask app.
     - Once the script is executed the terminal will provide an API URL (http://127.0.0.1:5000/)
     - Use the available API routes (e.g., /api/v1.0/precipitation) in your browser to access the API data.
