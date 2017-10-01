from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from flask import request
import uuid
from flask_cassandra import CassandraCluster
import json
import datetime as dt
 
app = Flask(__name__)
app.secret_key = 'any random string'
cassandra = CassandraCluster()
app.config['CASSANDRA_NODES'] = ['52.25.173.31', '35.165.251.179', '52.27.187.234', '52.38.246.84']  # can be a string or list of nodes
# global instrCode 
global usernameCurrent
instrCode= 'ok is taking this'

def jsonCassandraFormat(textJson):
    strJson = '{'
    for key in textJson:
        if key == 'sentiment_term': 
            valueFormatted = '['
            for el in textJson.get(key):
                valueFormatted += '"' + el + '",'
            valueFormatted = valueFormatted[0:-1]+']'
            strJson += '"'+str(key) + '":' + valueFormatted + ','
        else:
            strJson += '"'+str(key)+'"' + ':"' + str(textJson.get(key)) + '",'
    
    strJson = strJson[0:-1]+'}'
    return strJson


@app.route('/', methods=['GET'])
def home():
    print("hey at home")
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        value = 10
        return render_template('index.html', instrCode=instrCode, my_value=value) #dashboard()

@app.route('/dashboard')
def dashboard():
    print("ok")
    return render_template("index.html")

@app.route('/get_data', methods=['GET'])
def get_data():
    # df = sqlio.read_sql(query, conn)
    sessiondb = cassandra.connect()
    sessiondb.set_keyspace("tweetdb")
    query = "SELECT  * FROM testtable"
    query = "select ticker, insertion_time, value from stocktable WHERE ticker= 'AAPL' LIMIT 1"
    rows  = sessiondb.execute(query)
    # print(rows[0])
    # print(rows[0].insertion_time)
    # print(rows[0].value[0])
    # value = float(rows[0].value[0])
    # print(value)
    value = {'price': float(rows[0].value[0]), 'timeStamp': str(rows[0].insertion_time)}
    print(json.dumps(value))
    return json.dumps(value)

@app.route('/submit', methods=['POST'])
def my_form_post():

    # return "Gotta update new instruction"
    text = request.form['codeUser']
    textJson = json.loads(text)
    textJson['insertion_time'] = dt.datetime.today().strftime("%Y-%m-%d")
    textJson['user'] = session.get('usernameCurrent', None)


    textJsonFormatted = jsonCassandraFormat(textJson)

    # return str(textJsonFormatted)
    sessiondb = cassandra.connect()
    sessiondb.set_keyspace("tweetdb")
   

    cql = "UPDATE instructiontable SET  INTO instructiontable JSON '%s'"
    cqlDelete = "DELETE FROM instructiontable WHERE user= '%s' AND ticker= '%s'"

    # return cqlDelete % (session.get('usernameCurrent', None),textJson['ticker'])
    sessiondb.execute(cqlDelete % (session.get('usernameCurrent', None),textJson['ticker']))

    cql = "INSERT INTO instructiontable JSON '%s'"
    sessiondb.execute(cql % textJsonFormatted )

    query = "SELECT JSON * FROM instructiontable WHERE user=%s"
    instrCode = str(sessiondb.execute(query,[session.get('usernameCurrent', None)])[:])#)#request.form['username'])
    
    # return str(instrCode)
    return render_template('index.html', instrCode=text) #dashboard()

    return textJsonFormatted

    return text

    cql = "INSERT INTO tweettable (tweet, sentiment) VALUES (%s, %s)"
    sessiondb.execute(cql, (text, -1) )
        

    query = "SELECT tweet FROM tweettable WHERE tweet=%s"
    row = sessiondb.execute(query,[text])

    outputText = textJson.get("ticker")

    return  str(outputText) #str(row[0])#row[0].upper #"ok" #row[0]  #str(r[0])


@app.route('/login', methods=['POST'])
def do_admin_login():
    # return "you are in buddy"
    if request.form['password'] == 'password' and request.form['username'] == 'paul':
        session['usernameCurrent'] = request.form['username']
        # usernameCurrent = request.form['username']
        session['logged_in'] = True
        sessiondb = cassandra.connect()
        sessiondb.set_keyspace("tweetdb")
        # return "hey there"

        query = "SELECT JSON * FROM instructiontable WHERE user=%s"
        instrCode = str(sessiondb.execute(query,[request.form['username']])[:])#)#request.form['username'])

    return render_template('index.html', instrCode=instrCode) #dashboard()

    return home(instrCode)

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

 
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
