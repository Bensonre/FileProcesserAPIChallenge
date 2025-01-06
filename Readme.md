# Challenge 1 City suggestion API
# Basics and Usage
This is a API that "processs" text files. By appending the word Processed to them.

Ex when running locally:

    http://127.0.0.1:8000/trigger

    Body= {
        Files:[
            {
                "FileUri": "Some file location"
                "OutUri": "Some file Destination"
            },
            ...
            {
                "FileUri": "Another file location"
                "OutUri": "Another file Destination"
            }
        ]
    }    
The api will then return a Job Id

        { 
        }

Option querry parameters latitude, and longitude can be passed to improve guesses.

Ex when running locally:

    http://127.0.0.1:5000/suggestions?q=Newport&latitude=44&longitude=-124

This makes Newport, OR, US the most likely of the Newports.

    { 
        "suggestions": 
            [
                {
                    "name":"Newport, OR, US",
                    "latitude":44.63678,
                    "longitude":-124.05345,
                    "score":0.998673375
                },
                {
                    "name":"Newport, RI, US",
                    "latitude":41.4901,
                    "longitude":-71.31283,
                    "score":0.9947710417
                },
                {
                    "name":"Newport, KY, US",
                    "latitude":39.09145,
                    "longitude":-84.49578,
                    "score":0.9897738542
                },
                {
                    "name":"Newport, TN, US",
                    "latitude":35.96704,
                    "longitude":-83.18766,
                    "score":0.9832646667
                }
            ]
    }

# Running the code Locally
## In Venv
### Navigate to Challenge 1 folder and build venv
```
py -3 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
flask --app buzz run
```
The output should look something like this:
        
        * Serving Flask app 'buzz'
        * Debug mode: off
        WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
        * Running on http://127.0.0.1:5000
        Press CTRL+C to quit
        127.0.0.1 - - [16/Dec/2024 15:25:20] "GET / HTTP/1.1" 200 -

Now simply navigate to the returned url at /suggestions and begin querrying


## Via Docker
    docker build -t city_suggestor .
    docker run -p 5000:8080 city_suggestor
With docker it will output `INFO:waitress:Serving on http://0.0.0.0:8080 http:://0.0.0.0:8080`

However it only runs there inside of the container you will still access it via `http://127.0.0.1:5000/suggestions?q=beavers`


# Testing the code
Tests were implemented using unittest. 
To run the tests simply run: `python -m unittest` from the Challenge 1 folder this will run all the tests in the tests folder

# For Developers (The nuts and Bolts)
## File structure

The file structure is very striaght forward for this small project. You find all of the basics about each file below. Of all the files below 2 are the most important tests/testDataParser.py the file that handles most of the data manipulation and buzz.py the main flask driver file.

   - Challenge 1 (root folder)
        - .venv (optional: folder created when running locally in a virtual environment)
        - Data (Folder containing the Dataset, config file and python classes that interact with the Dataset)
            - \_\_init\_\_.py (empty file makes import Data.<file> callable)
            - [cities_canada-usa.tsv](Data/cities_canada-usa.tsv) (this is the default dataset as a tab seperated file)
            - [dataRetriever.py](Data/DataRetreiver.py) (Simplist class, retrieves the data and returns a subset of neccessary columns as a python pandas dataframe. Absracted from parser so that the parser will still work if a simple database or other infrastucture was created)
            - ***[DataParser.py](Data/DataParser.py)*** (This is the workhorse class. It takes the dataframe returned by the retriever and builds the suggestions)
        - tests/ (folder containing all the tests)
            - \_\_init\_\_.py (empty file makes import tests.<file> callable)
            - [alt_test_file.csv](tests/alt_test_file.csv) (Alternate Data for testing in the csv format to test data retrieval from a file different seperator. Also provides a smaller more managable set of data to test the parser with)
            - [test_config.json](tests/test_config.json) (Alternate Config file for the parser so that we can retreive more results)
            - [testDataParser.py](tests/testDataParser.py) (unit tests the DataParser Class)
            - [testDataRetriver.py](tests/testDataRetriver.py) (unit tests the dataRetriver class)
        - [buzz.py](buzz.py) (this is the Driver that executes flask and handle path parsing)
        - [response.py](response.py) (this is a class file that handles sending the proper response. It is very permitive in its current state but abstracting it here makes it easy to expand upon)


##


#   Credits
 - Flask
    - This Api was created using [flask](https://flask.palletsprojects.com/en/stable/). 
    - Flask is a simple Library for creating apis, or webservers using python.
    - Check out https://flask.palletsprojects.com/en/stable/ for more information on flask.

 - Pandas
    - The data parsing in the DataParser is handled by the [pandas](https://pandas.pydata.org/) library. A common, open source, data analysis and manipulation tool.
    - Check out https://pandas.pydata.org/ for more info on pandas
 - DataSet
    - The Dataset for this project was provided via https://geonames.org.
    - The dataset contains only sample data for some US and Canadian cities
 - MarkDown
    - This Mark down file is Returned as html at the root endpoint using the [markdown](https://python-markdown.github.io/index.html) library.
    - visit https://python-markdown.github.io/index.html to learn more about this library

# Criteria
- [x] the endpoint is exposed at `/suggestions`
- [x] the partial (or complete) search term is passed as a query string parameter `q`
- [x] the caller's location can optionally be supplied via query string parameters `latitude` and `longitude` to help improve relative scores
- [x] the endpoint returns a JSON response with an array of scored suggested matches
    - [x] the suggestions are sorted by descending score 
    - [x] each suggestion has a score between 0 and 1 (inclusive) indicating confidence in the suggestion (1 is most confident)
    - [x] each suggestion has a name which can be used to disambiguate between similarly named locations
    - [x] each suggestion has a latitude and longitude
- [x] all functional tests should pass (additional tests may be implemented as necessary).
