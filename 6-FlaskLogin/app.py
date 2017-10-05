from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from flask import request
import uuid
from flask_cassandra import CassandraCluster
import json
import datetime as dt
import random
import numpy as np
 
def load_wordlist(filename):
    """ 
    This function returns a list or set of words from the given filename.
    """
    f = open(filename, 'rU')
    text = f.read()
    text = text.split('\n')[:-1]
    f.close()
    return text

app = Flask(__name__)
app.secret_key = 'any random string'
cassandra = CassandraCluster()
app.config['CASSANDRA_NODES'] = ['52.25.173.31', '35.165.251.179', '52.27.187.234', '52.38.246.84']  # can be a string or list of nodes
# global instrCode 
global usernameCurrent
instrCode= 'ok is taking this'
tickers = []
tickerQ = []




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
        return render_template('index.html', instrCode=instrCode, my_value=value, tickers = tickers, searchterms = searchterms) #dashboard()

@app.route('/dashboard')
def dashboard():
    print("ok")
    return render_template("index.html")

@app.route('/get_data/<string:ticker>/', methods=['GET'])
# @app.route('/get_data', methods=['GET','POST'])
def get_data(ticker):
    # print('got back in python')
    # if request.method == "POST":
    # tickers=request.json['tickers']
    # print(ticker)
    # print('over and out')
    # df = sqlio.read_sql(query, conn)
    # print(tickers)
    sessiondb = cassandra.connect()
    sessiondb.set_keyspace("tweetdb")
    query = "select ticker, insertion_time, value from stocktable WHERE ticker= '%s' LIMIT 100"
    rows  = sessiondb.execute(query % ticker)
    x = []
    y = []
    for user_row in rows:
        x.append(str(user_row.insertion_time))
        y.append(float(user_row.value[0]))

    value = {'price': y, 'timeStamp': x}
    return json.dumps(value)


@app.route('/get_data_sentiment/<string:keyWord>', methods=['GET'])
def get_data_sentiment(keyWord):

    print('got here for sentiment')
    sessiondb = cassandra.connect()
    sessiondb.set_keyspace("tweetdb")
    query = "select searchterm, insertion_time, sentiment from searchtermtable WHERE searchterm = '%s' LIMIT 100"
    # print(keyWord)
    rows  = sessiondb.execute(query % keyWord)
    
    x = [str(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))]
    y = [round((random.random()-1)*2,2)]
    for i,keyWord_row in enumerate(rows):
        x.append(str((dt.datetime.now()- dt.timedelta(seconds=5)).strftime('%Y-%m-%d %H:%M:%S')))
        y.append(round(np.random.uniform(-1,1),2))

    value = {'sentiment': y , 'timeStamp': x}
    print(keyWord)
    print(value)
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
    sessiondb = cassandra.connect()
    sessiondb.set_keyspace("tweetdb")
    query = "SELECT password FROM usertable WHERE user=%s"
    password = sessiondb.execute(query,[request.form['username']])[0].password

    print(password)
    print(request.form['password'])
    if request.form['password'] == password: # request.form['username'] == 'paul':
        session['usernameCurrent'] = request.form['username']
        # usernameCurrent = request.form['username']
        session['logged_in'] = True
        # return "hey there"

        query = "SELECT * FROM usertable WHERE user=%s"
        tickers = sessiondb.execute(query,[request.form['username']])[0].stocklist#)#request.form['username'])
        # print tickers
        # print
        query = "SELECT JSON * FROM instructiontable WHERE user=%s"
        instrCode = str(sessiondb.execute(query,[request.form['username']])[:])#)#request.form['username'])

        searchterms =  load_wordlist("../Dataset/keyWords.txt")

        print('ere are the terms')
        print(searchterms)

        return render_template('index.html', instrCode=instrCode, tickers = tickers, searchterms = searchterms) #dashboard()

    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

 
if __name__ == "__main__":
    #app.secret_key = os.urandom(12)
    app.run(host= '0.0.0.0', debug=False)
    #app.run(host= '0.0.0.0') 
    #app.run(host='0.0.0.0')
    #app.run(debug=True,host='0.0.0.0', port=4000)
