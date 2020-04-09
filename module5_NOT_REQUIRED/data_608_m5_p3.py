from flask import Flask, jsonify, request
import requests
from json2html import *

# Data 608, M5.3, Jenkins

# To run on Windows
# Navigate to the file directory
# Enter in the command line
# set FLASK_APP=data_608_m5_p3
# flask run

app = Flask(__name__)


assignment = '''
            <div>
            <h2>Module 4.5 Directions</h2>
                <p>In this module, we’ll be building on our work from module 4. We’re going to create a flask
                API that responds to information from the URL.</p><p>
                Look through the sample API provided and test it out for yourself. This is using Flask’s
                jsonify method to return a json blob. Make sure you’re able to see both the hello json
                and are able to see the complex json return values based on the provided url.</p><p>
                In addition to the provided sample code, take a look at this Flask introduction in three parts:
                part 1, part 2, and part 3.</p><p>
                Part 1 is the most important. Parts 2 and 3 go deeper into Flask. For this course we’re only
                going to be using Flask in a superficial way, so don’t worry if you don’t feel like an expert in
                the tool.</p><p>
                Your goal for this module is to create a rest API that returns something from the tree census.
                It can be anything. Your only requirement is that it needs to accept a variable from the URL.
                While it can be anything, It will be helpful to think about what we’ll be doing with this. For one
                of our options in module 5, we’ll be using this API to create a simple web app that gives
                users some information about trees. Think about what you might like a user to see</p>
            </div>
            <div>
                <h2>Module 5, Part 3 Directions</h2>
                <p>This is one of three homework assignments you can complete for this week (you must do
                two, you may do all three for extra credit). Use the flask API you designed in module 4.5 to
                display some sort of information based on user input. D3.json will allow you to read json
                directly from a url.</p><p>
                Create an app that takes in some user input, and returns some sort of information from the
                trees dataset.</p><p>
                This is geared towards those of you who have worked with javascript before and want a
                challenge.</p><p>
                Deployment: Your apps from parts 1 and 2 must be deployed. There are a lot of options for
                deploying javascript apps, however I would recommend using github pages. Read more
                about how github pages work here: https://pages.github.com/</p><p>
                Part 3 includes a flask app, so don’t worry about deployment. Just submit your flask app,
                your html file, and js files if required.</p>
            </div>
'''

work = '''
        <div><h1>Data 608, Module 5, Part 3</h1></div>
        <div>
            <h2>Assignment</h2>
            Go to the following url to see a demo example of this app: <a href="http://localhost:5000/sota/health/Good">http://localhost:5000/sota/health/Good</a></p><p>Next, check out these resources for the components of this app:
            <ol>
            <li>Connecting to Tree Data: <a href="https://data.cityofnewyork.us/Environment/2015-Street-Tree-Census-Tree-Data/uvpi-gqnh">https://data.cityofnewyork.us/Environment/2015-Street-Tree-Census-Tree-Data/uvpi-gqnh</a></li>
            <li>More on Socrata: <a href="https://dev.socrata.com/docs/endpoints.html">https://dev.socrata.com/docs/endpoints.html</a></li>
        <li>More on Flask: <a href="https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask">https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask</a></li>
            <li>Example of a typical API call: <a href="https://data.cityofnewyork.us/resource/nwxe-4ae8.json?health=Good&spc_common=honeylocust&problems=Stones&nta_name=Chinatown">https://data.cityofnewyork.us/resource/nwxe-4ae8.json?health=Good&spc_common=honeylocust&problems=Stones&nta_name=Chinatown</a></li></ol>
            <p>In order to view available options for your url query, check out the first link above. In our example above, we use the key health and the value Good, which appear in the url.</p>
        </div>
'''

form = '''
        <h3>Here is where the user can access Tree information based on Health input.</h3>
        <p>Enter health of Good, Fair, or Poor in the input box.</p>
        <form method="post" action="/sota">
        <fieldset>

        <legend>Tree Health Search MVP</legend>

        <div>
            <label for="health">Tree Health</label>
            <div>
                <select id="health" name="health">
                <option value="Good">Good</option>
                    <option value="Fair">Fair</option>
                    <option value="Poor">Poor</option>
                </select>
            </div>
        </div>
        <div>
            <label for="button"></label>
            <div>
                <button id="button" name="button" type="submit" value="submit">Get Trees</button>
            </div>
        </div>

        </fieldset>
        </form>
'''


# This is a more complex API who's returned information depends on a variable
# from the URL.
# visit localhost:5000/complex/foo to see what gets returned. Replace
# foo with other words to verify the API is reponding to that variable.

@app.route('/sota', methods=['GET', 'POST'])

def return_home():
    # Result Table is empty
    tables = ''

    if request.method == 'POST':
        # Get submitted input form option from POST
        health_input = request.form['health']
        # inject form input option into API call url
        # Form currently working for health parameter only,
        # with available values of: Good, Fair, Poor
        url = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json'
        query = str(url + '?health=' + health_input)

        # Call Socrata API
        # https://data.cityofnewyork.us/Environment/2015-Street-Tree-Census-Tree-Data/uvpi-gqnh
        r = requests.get(query)
        result_json = r.json()

        # Convert JSON results to table
        tables = json2html.convert(json = result_json)
        tables = '<h3>Sota Tree Search for: health =' + health_input + '</h3>' + tables

    # Return html page
    html = '<html><body><head><title>Data 608, M5.3, Jenkins</title></head>' +  work + form  + tables + assignment + '</body></html>'

    return html


# Satisfy Module 4.5
# Enter url and use parts as variables to query treee API
# Example Queries
    #https://data.cityofnewyork.us/resource/nwxe-4ae8.json?health=Good
    #https://data.cityofnewyork.us/resource/nwxe-4ae8.json?health=Good&spc_common=honeylocust&problems=Stones&nta_name=Chinatown
# Url Query ptions https://data.cityofnewyork.us/Environment/2015-Street-Tree-Census-Tree-Data/uvpi-gqnh

@app.route('/sota/<string:key>/<string:value>')
def return_complex(key, value):

    # Build API Call
    url = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json'
    query = str(url+'?'+key+'='+value)

    # Call the API
    r = requests.get(query)
    result_json = r.json()

    # Convert JSON to table
    tables = json2html.convert(json = result_json)
    html = '<html><body><head><title>Data 608, M5.3, Jenkins</title></head><body><h1>Sota Tree Search for: ' + key + '=' + value + '</h1>' + tables + '</body></html>'
    # Return the html page
    return html


if __name__ == '__main__':
    app.run(debug=True)
