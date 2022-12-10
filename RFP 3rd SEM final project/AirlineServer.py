#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import json

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='1234',
                       db='data',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


#Define a route to hello function
@app.route('/')
def hello():
    if 'username' in session:
        if 'airline_name' in session:
            return render_template('index.html', username=session['username'], auth=session['usertype'], airline=session['staff_airline'])
        else:
            return render_template('index.html', username=session['username'], auth=session['usertype'])
    else:
        return render_template('index.html')
    
@app.route('/customer_back')
def customer_back():
    return redirect(url_for('customer_home'))
    #return render_template('customer_home.html', username=session['username'], auth=session['usertype'])

@app.route('/staff_back')
def staff_back():
    return redirect(url_for('staff_home'))
    #return render_template('staff_home.html', username=session['username'], auth=session['usertype'])

#=============================================================================
#Define route for two types of register
@app.route('/customer_register')
def customer_register():
    return render_template('customer_register.html')
@app.route('/staff_register')
def staff_register():
    return render_template('staff_register.html')

#Authenticates the customer_register
@app.route('/customer_registerAuth', methods=['GET', 'POST'])
def customer_registerAuth():
    #grabs information from the forms
    email = request.form['email']
    password = request.form['password']
    name = request.form['customer_name']
    tel = request.form['phone']
    dob = request.form['birthday']
    passportNum = request.form['passport']
    passportCountry = request.form['passport_country']
    passportExpir = request.form['passport_expir']
    buildingNum = request.form['building_number']
    street = request.form['street']
    city = request.form['city']
    state = request.form['state']
    
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM customer WHERE email = %s'
    cursor.execute(query, (email))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
        #If the previous query returns data, then user exists
        error = "This customer already exists"
        return render_template('customer_register.html', error = error)
    else:
        ins = 'INSERT INTO customer VALUES (%s, %s, md5(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (email,name,password,buildingNum,street,city,state,tel,passportNum,passportExpir,passportCountry,dob))
        conn.commit()
        cursor.close()
        return render_template('index.html')

#Authenticates the staff_register
@app.route('/staff_registerAuth', methods=['GET', 'POST'])
def staff_registerAuth():
	#grabs information from the forms
    username = request.form['username']
    password = request.form['password']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    dob = request.form['birthday']
    airlineName = request.form['airline']

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM staff WHERE username = %s'
    cursor.execute(query, (username))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
        #If the previous query returns data, then user exists
        error = "This staff already exists"
        return render_template('staff_register.html', error = error)
    else:
        ins = 'INSERT INTO staff VALUES(%s, md5(%s), %s, %s, %s, %s)'
        cursor.execute(ins, (username, password, firstname, lastname, dob, airlineName))
        conn.commit()
        cursor.close()
        return render_template('index.html')

#=============================================================================
#Define route for login
@app.route('/login')
def login():
	return render_template('login.html')

#Authenticates the customer_login
@app.route('/customer_loginAuth', methods=['GET', 'POST'])
def customer_loginAuth():
    #grabs information from the forms
    email = request.form['username']
    password = request.form['password']

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM customer WHERE email = %s and customer_password = md5(%s)'
    cursor.execute(query, (email, password))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
        #creates a session for the the user
        #session is a built in
        session['username'] = email
        session['usertype'] = 'customer'
        #return redirect(url_for('customer_home'))
        #return redirect('/')
        return render_template('customer_home.html', username=email, auth=session['usertype'])
    else:
        #returns an error message to the html page
        error = 'Invalid login or email'
        return render_template('login.html', error=error)

#Authenticates the staff_login
@app.route('/staff_loginAuth', methods=['GET', 'POST'])
def staff_loginAuth():
	#grabs information from the forms
    
    username = request.form['username']
    password = request.form['password']

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM staff WHERE username = %s and userpassword = md5(%s)'
    cursor.execute(query, (username, password))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    
    error = None
    if(data):
        #creates a session for the user
        #session is a built in
        session['username'] = username
        session['usertype'] = 'staff'
        session['staff_airline'] = str(data['airline_name'])
        
        airline = session['staff_airline']
        return render_template('staff_home.html', username=username, auth=session['usertype'],airline=airline)
    else:
        #returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('login.html', error=error)

#=============================================================================
#Future Flights
@app.route('/future_flights')
def future_flights():
    return render_template('future_flights.html')

@app.route('/future_flightsSearch', methods=['GET', 'POST'])
def future_flightsSearch():
    #get info from form
    deptAir = request.form['dept_air'].upper()
    arrAir = request.form['arr_air'].upper()
    deptDate = request.form['dept_date']
    
    #isRound = request.form['round_trip']
    
    #cursor to send queries
    cursor = conn.cursor()
    #Search for go trip
    query = 'SELECT * FROM flight WHERE (departure_airport, arrival_airport, date(departure_datetime)) = (%s,%s,%s) AND departure_datetime>CURRENT_TIMESTAMP'
    cursor.execute(query, (deptAir,arrAir,deptDate))
    dataGo = cursor.fetchall()
    
    dataReturn = ''
    
    if 'round_trip' in request.form: #it is a round trip
        returnDate = request.form['return_date']
        query2 = 'SELECT * FROM flight WHERE (departure_airport, arrival_airport, date(departure_datetime)) = (%s,%s,%s) AND departure_datetime>CURRENT_TIMESTAMP'
        cursor.execute(query2, (arrAir,deptAir,returnDate))
        dataReturn = cursor.fetchall()
        
    cursor.close()
    
    if (dataReturn):
        return render_template('future_flights.html', dataGo = dataGo, dataReturn = dataReturn, deptAir = deptAir, arrAir = arrAir)
    else:
        return render_template('future_flights.html', dataGo = dataGo, deptAir = deptAir, arrAir = arrAir)

#=============================================================================
#Flght Status
@app.route('/flight_status')
def flight_status():
    return render_template('flight_status.html')
@app.route('/flight_statusSearch', methods=['GET', 'POST'])
def flight_statusSearch():
    #get info from form
    airline = request.form['airline']
    flightNum = request.form['flight_num']
    deptDate = request.form['dept_date']
    
    cursor = conn.cursor()
    query = 'SELECT flight_status FROM flight WHERE (airline_name,flight_number,date(departure_datetime)) = (%s,%s,%s)'
    cursor.execute(query,(airline,flightNum,deptDate))
    airStatus = cursor.fetchone()
    error = None
    
    if not (airStatus):
        error = 'Flight not exist.'
    
    cursor.close()
    return render_template('flight_status.html', airStatus = airStatus, error = error)

#=============================================================================
#My Flights (Customer)
@app.route('/my_flights', methods=['GET', 'POST'])
def my_flights():
    if 'username' in session:
        email = session['username']
        
        cursor = conn.cursor()
        query = ('SELECT flight.airline_name, flight.flight_number, flight.departure_datetime, flight.departure_airport, '
                 'flight.arrival_datetime, flight.arrival_airport, purchase.sold_price FROM customer, purchase, '
                 'ticket NATURAL JOIN flight WHERE customer.email = purchase.email AND purchase.ticket_id = ticket.ticket_id '
                 'AND flight.departure_datetime <= CURRENT_TIMESTAMP AND customer.email = %s')
        cursor.execute(query, (email))
        pastFlights = cursor.fetchall()
        
        query2 = ('SELECT flight.airline_name, flight.flight_number, flight.departure_datetime, flight.departure_airport, '
                 'flight.arrival_datetime, flight.arrival_airport, purchase.sold_price FROM customer, purchase, '
                 'ticket NATURAL JOIN flight WHERE customer.email = purchase.email AND purchase.ticket_id = ticket.ticket_id '
                 'AND flight.departure_datetime >= CURRENT_TIMESTAMP AND customer.email = %s')
        cursor.execute(query2, (email))
        futureFlights = cursor.fetchall()
        
        cursor.close()
        return render_template('my_flights.html', pastFlights = pastFlights, futureFlights = futureFlights, username=session['username'], auth=session['usertype'])
    
    else:
        error = "Not logged in."
        return render_template('my_flights.html', error = error)


#=============================================================================
#Customer Home and Staff Home
@app.route('/customer_home')
def customer_home():
    #return redirect(url_for('customer_home'))
    username = session['username']
    return render_template('customer_home.html', username=username, auth=session['usertype'])

@app.route('/staff_home')
def staff_home():
    #return redirect(url_for('staff_home'))
    username = session['username']
    
    return render_template('staff_home.html', username=username, auth=session['usertype'], airline=session['staff_airline'])

#=============================================================================
#Customer Rate and Comments
@app.route('/customer_ratecomment', methods=['GET', 'POST'])
def customer_ratecomment():
    if 'ratecomment' not in request.form:
        return redirect(url_for('my_flights'))
    
    flightInfoStr = request.form['ratecomment']
    flightTuple = flightInfoStr.split('.,.')
    
    airlineName = flightTuple[0]
    flightNum = flightTuple[1]
    deptDatetime = flightTuple[2]
    
    username = session['username']
    auth = session['usertype']
    
    cursor = conn.cursor()
    #query = "SELECT * FROM customerrate WHERE (email,airline_name,flight_number,departure_datetime) = (%s,%s,%s,%s)"
    query = "SELECT * FROM customerrate WHERE email = %s"
    cursor.execute(query,(username))
    ratecommentData = cursor.fetchall()
    
    cursor.close()

    return render_template('customer_ratecomment.html', username=username, auth=auth,
                           airlineName=airlineName, flightNum=flightNum, deptDatetime=deptDatetime,
                           ratecommentData=ratecommentData)

@app.route('/ratecomment_submit', methods=['GET', 'POST'])
def ratecomment_submit():
    airlineName = request.form['airlineName']
    flightNum = request.form['flightNum']
    deptDatetime = request.form['deptDatetime']
    rate = request.form['rate']
    if 'comment' in request.form:
        comment = request.form['comment']
    else:
        comment = "null"
    
    username = session['username']
    #auth = session['usertype']
    
    cursor = conn.cursor()
    query1 = "DELETE FROM customerrate WHERE (email,airline_name,flight_number,departure_datetime) = (%s,%s,%s,%s)"
    query2 = "INSERT INTO customerrate VALUES (%s,%s,%s,%s,%s,%s)"
    cursor.execute(query1, (username,airlineName,flightNum,deptDatetime))
    cursor.execute(query2, (username,airlineName,flightNum,deptDatetime,rate,comment))
    
    cursor.close()
    
    return redirect(url_for('my_flights'))

#=============================================================================
#Customer search_flights and buy tickets
@app.route('/search_flights', methods=['GET', 'POST'])
def search_flights():
    username = session['username']
    auth = session['usertype']
    return render_template('search_flights.html', username=username,auth=auth)

@app.route('/search_flightsSearch', methods=['GET', 'POST'])
def search_flightsSearch():
    #get info from form
    deptAir = request.form['dept_air'].upper()
    arrAir = request.form['arr_air'].upper()
    deptDate = request.form['dept_date']
    
    #isRound = request.form['round_trip']
    
    #cursor to send queries
    cursor = conn.cursor()
    #Search for go trip
    query = 'SELECT * FROM flight WHERE (departure_airport, arrival_airport, date(departure_datetime)) = (%s,%s,%s) AND departure_datetime>CURRENT_TIMESTAMP'
    cursor.execute(query, (deptAir,arrAir,deptDate))
    dataGo = cursor.fetchall()
    dataReturn = ''
    if 'round_trip' in request.form: #it is a round trip
        returnDate = request.form['return_date']
        query2 = 'SELECT * FROM flight WHERE (departure_airport, arrival_airport, date(departure_datetime)) = (%s,%s,%s) AND departure_datetime>CURRENT_TIMESTAMP'
        cursor.execute(query2, (arrAir,deptAir,returnDate))
        dataReturn = cursor.fetchall()
    cursor.close()
    
    username = session['username']
    auth = session['usertype']
    if (dataReturn):
        return render_template('search_flights.html', dataGo=dataGo, dataReturn=dataReturn, deptAir=deptAir, arrAir=arrAir, username=username, auth=auth)
    else:
        return render_template('search_flights.html', dataGo = dataGo, deptAir = deptAir, arrAir = arrAir, username=username, auth=auth)
    
@app.route('/choose_ticket', methods=['GET', 'POST'])
def choose_ticket():
    flightInfoStr = request.form['chooseFlight']
    flightTuple = flightInfoStr.split('.,.')
    
    airlineName = flightTuple[0]
    flightNum = flightTuple[1]
    deptDatetime = flightTuple[2]
    
    username = session['username']
    auth = session['usertype']
    
    cursor = conn.cursor()
    
    queryCap = "SELECT COUNT(ticket_id) AS capacity FROM ticket WHERE (airline_name,flight_number,departure_datetime) = (%s,%s,%s)"
    cursor.execute(queryCap, (airlineName,flightNum,deptDatetime))
    capacity = cursor.fetchone()['capacity']
    
    queryOcc = "SELECT COUNT(ticket_id) AS occupancy FROM ticket NATURAL JOIN purchase WHERE (airline_name,flight_number,departure_datetime) = (%s,%s,%s)"
    cursor.execute(queryOcc, (airlineName,flightNum,deptDatetime))
    occupancy = cursor.fetchone()['occupancy']
    
    queryTickets = "SELECT ticket_id FROM ticket NATURAL LEFT OUTER JOIN purchase WHERE (airline_name,flight_number,departure_datetime) = (%s,%s,%s) AND email IS null"
    cursor.execute(queryTickets, (airlineName,flightNum,deptDatetime))
    ticketsInfo = ""
    ticketsInfo = cursor.fetchall()
    
    queryBP = "SELECT base_price FROM flight WHERE (airline_name,flight_number,departure_datetime) = (%s,%s,%s)"
    cursor.execute(queryBP, (airlineName,flightNum,deptDatetime))
    basePrice = float(cursor.fetchone()['base_price'])
    
    
    if float(occupancy)/float(capacity)>=0.749999:
        basePrice = basePrice*1.25
        price = round(basePrice,2)
    else:
        price = round(basePrice,2)
    
    cursor.close()
    return render_template('choose_ticket.html', username=username,auth=auth,ticketsInfo=ticketsInfo,
                           airlineName=airlineName,flightNum=flightNum,deptDatetime=deptDatetime,
                           occupancy=occupancy,capacity=capacity,price=price)

@app.route('/buy_ticket', methods=['GET', 'POST'])
def buy_ticket():
    username = session['username']
    auth = session['usertype']
    ticketID = request.form['ticketID']
    price = request.form['price']
    
    return render_template('buy_ticket.html',username=username,auth=auth,ticketID=ticketID,price=price)

@app.route('/buy_ticket_confirm', methods=['GET', 'POST'])
def buy_ticket_confirm():
    email = session['username']
    #auth = session['usertype']
    
    ticket_id = request.form['ticketID']
    card_type = request.form['card_type']
    card_number = request.form['card_number']
    name_on_card = request.form['name_on_card']
    expiration_date = request.form['expiration_date']
    sold_price = request.form['price']
    
    #Insert purchase information
    cursor = conn.cursor()
    queryIns = "INSERT INTO purchase VALUES (%s,%s,%s,%s,%s,%s,%s,CURRENT_TIMESTAMP)"
    cursor.execute(queryIns, (ticket_id, email, sold_price, card_type, card_number, name_on_card, expiration_date))
    
    cursor.close()
    return redirect(url_for('my_flights'))

#=============================================================================
#Customer track spending
@app.route('/track_spending', methods=['GET', 'POST'])
def track_spending():
    email = session['username']
    auth = session['usertype']
    
    cursor = conn.cursor()
    queryYear = "SELECT SUM(sold_price) AS yearSpending, CURRENT_DATE AS enddate, date(CURRENT_DATE-10000) AS startdate FROM purchase WHERE email=%s AND purchase_datetime >= date(CURRENT_DATE-10000) GROUP BY email"
    cursor.execute(queryYear, (email))
    yearSpending = cursor.fetchone()
    
    queryMonth = ("SELECT CURRENT_DATE, year(purchase_datetime) AS year, month(purchase_datetime) AS month, SUM(sold_price) AS spending "
                  "FROM purchase WHERE email=%s GROUP BY year(purchase_datetime), month(purchase_datetime) "
                  "HAVING (year-year(CURRENT_DATE))*12+month >= month(CURRENT_DATE)-5")
    cursor.execute(queryMonth, (email))
    monthlySpending = cursor.fetchall()
    
    
    cursor.close()
    return render_template('/track_spending.html', username=email,auth=auth,yearSpending=yearSpending,monthlySpending=monthlySpending)


@app.route('/track_spendingSearch', methods=['GET', 'POST'])
def track_spendingSearch():
    email = session['username']
    auth = session['usertype']
    
    cursor = conn.cursor()
    queryYear = "SELECT SUM(sold_price) AS yearSpending, CURRENT_DATE AS enddate, date(CURRENT_DATE-10000) AS startdate FROM purchase WHERE email=%s AND purchase_datetime >= date(CURRENT_DATE-10000) GROUP BY email"
    cursor.execute(queryYear, (email))
    yearSpending = cursor.fetchone()
    
    queryMonth = ("SELECT CURRENT_DATE, year(purchase_datetime) AS year, month(purchase_datetime) AS month, SUM(sold_price) AS spending "
                  "FROM purchase WHERE email=%s GROUP BY year(purchase_datetime), month(purchase_datetime) "
                  "HAVING (year-year(CURRENT_DATE))*12+month >= month(CURRENT_DATE)-5")
    cursor.execute(queryMonth, (email))
    monthlySpending = cursor.fetchall()
    
    startDate = request.form['startdate']
    endDate = request.form['enddate']
    querySearch = ("SELECT year(purchase_datetime) AS year, month(purchase_datetime) AS month, SUM(sold_price) AS spending "
                   "FROM purchase WHERE date(purchase_datetime) >= %s AND date(purchase_datetime) <= %s AND email = %s "
                   "GROUP BY year(purchase_datetime),month(purchase_datetime)")
    cursor.execute(querySearch, (startDate,endDate,email))
    searchSpendingData = cursor.fetchall()
    
    error = ""
    if not searchSpendingData:
        error = "No results."
    
    cursor.close()
    return render_template('/track_spending.html', username=email,auth=auth,yearSpending=yearSpending,
                           monthlySpending=monthlySpending,searchSpendingData=searchSpendingData,error=error)


#=============================================================================
#Staff view flights
@app.route('/view_flights', methods=['GET', 'POST'])
def view_flights():
    username = session['username']
    auth = session['usertype']
    airline = session['staff_airline']
    
    cursor = conn.cursor()
    queryDefault = "SELECT * FROM flight WHERE departure_datetime <= CURRENT_TIMESTAMP + INTERVAL 30 day AND departure_datetime >= CURRENT_TIMESTAMP"
    cursor.execute(queryDefault)
    defaultData = cursor.fetchall()
    
    cursor.close()
    return render_template('view_flights.html', username=username,auth=auth, airline=airline, defaultData=defaultData)

@app.route('/view_flightsSearch', methods=['GET', 'POST'])
def view_flightsSearch():
    username = session['username']
    auth = session['usertype']
    airline = session['staff_airline']

    cursor = conn.cursor()
    error = ""
    searchData = ""
    
    startDate = request.form['startDate']
    endDate = request.form['endDate']
    dept_air = request.form['dept_air'].upper()
    arr_air = request.form['arr_air'].upper()
    
    if startDate and endDate and dept_air and arr_air:
        query = "SELECT * FROM flight WHERE date(departure_datetime) >= %s AND date(departure_datetime) <= %s AND (departure_airport,arrival_airport) = (%s,%s)"
        cursor.execute(query, (startDate, endDate, dept_air, arr_air))
        searchData = cursor.fetchall()
        cursor.close()
        return render_template('view_flights.html', username=username,auth=auth, airline=airline, searchData=searchData, error=error)
    
    elif startDate and endDate:
        query = "SELECT * FROM flight WHERE date(departure_datetime) >= %s AND date(departure_datetime) <= %s"
        cursor.execute(query, (startDate, endDate))
        searchData = cursor.fetchall()
        cursor.close()
        return render_template('view_flights.html', username=username,auth=auth, airline=airline, searchData=searchData, error=error)
    
    elif dept_air and arr_air:
        query = "SELECT * FROM flight WHERE (departure_airport,arrival_airport) = (%s,%s)"
        cursor.execute(query, (dept_air, arr_air))
        searchData = cursor.fetchall()
        cursor.close()
        return render_template('view_flights.html', username=username,auth=auth, airline=airline, searchData=searchData, error=error)
    
    else:
        error = "Please Provide Correct Search Information"
    

    cursor.close()
    return render_template('view_flights.html', username=username,auth=auth, airline=airline, searchData=searchData, error=error)

@app.route('/change_status', methods=['GET', 'POST'])
def change_status():
    username = session['username']
    auth = session['usertype']
    airline = session['staff_airline']
    
    flightInfo = request.form['chooseStatus'].split('.,.')
    flight_number = flightInfo[0]
    dept_datetime = flightInfo[1]
    
    newStatus = request.form['newStatus']
    
    cursor = conn.cursor()
    query = "UPDATE flight SET flight_status = %s WHERE (airline_name,flight_number,departure_datetime) = (%s,%s,%s)"
    cursor.execute(query, (newStatus,airline,flight_number,dept_datetime))
    
    #searchData = json.loads(request.form['keepData'])
    #searchData = request.form['keepData']
    
    return redirect(url_for('view_flights'))
    #return render_template('view_flights.html', username=username,auth=auth, airline=airline, error=searchData)
    
#=============================================================================
@app.route('/view_flight_ratings', methods=['GET', 'POST'])
def view_flight_ratings():
    username = session['username']
    auth = session['usertype']
    airline = session['staff_airline']
    return render_template('view_flight_ratings.html', username=username,auth=auth, airline=airline)
    
@app.route('/view_flight_ratingsSearch', methods=['GET', 'POST'])
def view_flight_ratingsSearch():
    username = session['username']
    auth = session['usertype']
    airline = session['staff_airline']

    cursor = conn.cursor()
    error = ""
    searchData = ""
    
    startDate = request.form['startDate']
    endDate = request.form['endDate']
    dept_air = request.form['dept_air'].upper()
    arr_air = request.form['arr_air'].upper()
    
    if startDate and endDate and dept_air and arr_air:
        query = "SELECT * FROM flight WHERE date(departure_datetime) >= %s AND date(departure_datetime) <= %s AND (departure_airport,arrival_airport) = (%s,%s)"
        cursor.execute(query, (startDate, endDate, dept_air, arr_air))
        searchData = cursor.fetchall()
        cursor.close()
        return render_template('view_flight_ratings.html', username=username,auth=auth, airline=airline, searchData=searchData, error=error)
    
    elif startDate and endDate:
        query = "SELECT * FROM flight WHERE date(departure_datetime) >= %s AND date(departure_datetime) <= %s"
        cursor.execute(query, (startDate, endDate))
        searchData = cursor.fetchall()
        cursor.close()
        return render_template('view_flight_ratings.html', username=username,auth=auth, airline=airline, searchData=searchData, error=error)
    
    elif dept_air and arr_air:
        query = "SELECT * FROM flight WHERE (departure_airport,arrival_airport) = (%s,%s)"
        cursor.execute(query, (dept_air, arr_air))
        searchData = cursor.fetchall()
        cursor.close()
        return render_template('view_flight_ratings.html', username=username,auth=auth, airline=airline, searchData=searchData, error=error)
    
    else:
        error = "Please Provide Correct Search Information"
    
    cursor.close()
    return render_template('view_flight_ratings.html', username=username,auth=auth, airline=airline, searchData=searchData, error=error)
    
    
@app.route('/view_ratings', methods=['GET', 'POST'])
def view_ratings():
    username = session['username']
    auth = session['usertype']
    airline = session['staff_airline']
    
    flightInfo = request.form['chooseStatus'].split('.,.')
    flight_number = flightInfo[0]
    dept_datetime = flightInfo[1]
    
    cursor = conn.cursor()
    query = "SELECT * FROM customerrate WHERE (airline_name,flight_number,departure_datetime) = (%s,%s,%s)"
    cursor.execute(query, (airline,flight_number,dept_datetime))
    allRatings = cursor.fetchall()
    
    queryAvg = "SELECT AVG(rate) AS avg_rating FROM customerrate WHERE (airline_name,flight_number,departure_datetime) = (%s,%s,%s)"
    cursor.execute(queryAvg, (airline,flight_number,dept_datetime))
    avgRatingDict = cursor.fetchone()
    avgRating = round(avgRatingDict['avg_rating'],2)
    
    return render_template("view_ratings.html", username=username, auth=auth, airline=airline,
                           allRatings=allRatings, avgRating=avgRating, flight_number=flight_number, dept_datetime=dept_datetime)

#=============================================================================
#Staff create new flights and update status
@app.route('/create_new_flights', methods=['GET', 'POST'])
def create_new_flights():
    username = session['username']
    auth = session['usertype']
    airline_name = session['staff_airline']
    return render_template('create_new_flights.html', username=username,auth=auth, airline=airline_name)


@app.route('/create_new_flightsConfirm', methods=['GET', 'POST'])
def create_new_flightsConfirm():
    username = session['username']
    auth = session['usertype']
    airline = session['staff_airline']
    
    flight_number = request.form['flight_number']
    dept_air = request.form['dept_air'].upper()
    dept_date = request.form['dept_date']
    dept_time = request.form['dept_time']
    dept_datetime = dept_date+" "+dept_time
    arr_air = request.form['arr_air'].upper()
    arr_date = request.form['arr_date']
    arr_time = request.form['arr_time']
    arr_datetime = arr_date+" "+arr_time
    base_price = request.form['base_price']
    airplane_id = request.form['airplane_id']
    status = request.form['status']
    
    cursor = conn.cursor()
    
    #check depature airport exist
    queryCheckDeptAirport = "SELECT * FROM airport WHERE airport_code = %s"
    cursor.execute(queryCheckDeptAirport, (dept_air))
    deptExist = cursor.fetchone()
    
    #check arrival airport exist
    queryCheckArrAirport = "SELECT * FROM airport WHERE airport_code = %s"
    cursor.execute(queryCheckArrAirport, (arr_air))
    arrExist = cursor.fetchone()
    
    #check airplane exist
    queryCheckAirplane = "SELECT * FROM airplane WHERE (airline_name,airplane_id) = (%s,%s)"
    cursor.execute(queryCheckAirplane, (airline,airplane_id))
    airplaneExist = cursor.fetchone()
    if airplaneExist:
        seatNum = int(airplaneExist['seats'])
    
    
    error = "" #invalid airports/airplane/base_price/time
    if not deptExist:
        error = "Invalid Departure Airport."
    elif not arrExist:
        error = "Invalid Destination Airport."
    elif dept_air == arr_air:
        error = "Same Departure and Destination Airport"
    elif not airplaneExist:
        error = "Invalid Airplane"
    elif float(base_price) < 0:
        error = "Invalid Base Price"
    
    
    if not error:
        #delete repeat information
        queryDelete = "DELETE FROM flight WHERE (airline_name,flight_number,departure_datetime) = (%s,%s,%s)"
        cursor.execute(queryDelete, (airline, flight_number, dept_datetime))
        queryDeleteTicket = "DELETE FROM ticket WHERE (airline_name,flight_number,departure_datetime) = (%s,%s,%s)"
        cursor.execute(queryDeleteTicket, (airline, flight_number, dept_datetime))
        
        #insert flight
        queryIns = "INSERT INTO flight VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(queryIns, (airline, flight_number, dept_datetime, dept_air, arr_datetime, arr_air, base_price, airplane_id, status))
        
        #create tickets
        queryCreateTicket = "INSERT INTO ticket VALUES (%s,%s,%s,%s)"
        for seatNumber in range(1,seatNum+1):
            ticket_id = str(str(seatNumber) + "".join(airline.split(" ")) + flight_number + "".join(dept_date.split("-")) + "".join(dept_time.split(":")))
            cursor.execute(queryCreateTicket, (ticket_id, airline, flight_number, dept_datetime))
        
        cursor.close()
        return render_template('view_flights.html', username=username,auth=auth, airline=airline)
    
    else:
        return render_template('create_new_flights.html', username=username,auth=auth, airline=airline, error=error)

#=============================================================================
#Staff add airplanes
@app.route('/add_airplanes', methods=['GET', 'POST'])
def add_airplanes():
    username = session['username']
    auth = session['usertype']
    airline = session['staff_airline']
    
    cursor = conn.cursor()
    query = "SELECT * FROM airplane WHERE airline_name = %s"
    cursor.execute(query, (airline))
    airplaneData = cursor.fetchall()
    
    cursor.close()
    return render_template('add_airplanes.html', username=username, auth=auth, airline=airline, airplaneData=airplaneData)

@app.route('/add_airplanesConfirm', methods=['GET', 'POST'])
def add_airplanesConfirm():
    username = session['username']
    auth = session['usertype']
    airline = session['staff_airline']
    
    if auth != 'staff':
        return redirect(url_for('add_airplanes'))
    
    air_id = request.form['airID']
    seats = request.form['seatNum']
    
    cursor = conn.cursor()
    query = "INSERT INTO airplane VALUES (%s,%s,%s)"
    cursor.execute(query, (airline,air_id,seats))
    
    cursor.close()
    return redirect(url_for('add_airplanes'))

#=============================================================================
#staff add airports
@app.route('/add_airports', methods=['GET', 'POST'])
def add_airports():
    username = session['username']
    auth = session['usertype']
    airline = session['staff_airline']
    
    cursor = conn.cursor()
    query = "SELECT * FROM airport"
    cursor.execute(query)
    airportData = cursor.fetchall()
    
    cursor.close()
    return render_template('add_airports.html', username=username, auth=auth, airline=airline, airportData=airportData)

@app.route('/add_airportsConfirm', methods=['GET', 'POST'])
def add_airportsConfirm():
    username = session['username']
    auth = session['usertype']
    airline = session['staff_airline']
    
    if auth != 'staff':
        return redirect(url_for('add_airplanes'))
    
    air_code = request.form['airCode'].upper()
    air_name = request.form['airName']
    air_city = request.form['airCity']
    
    if len(air_code) != 3:
        return redirect(url_for('add_airports'))
    
    cursor = conn.cursor()
    query = "INSERT INTO airport VALUES (%s,%s,%s)"
    cursor.execute(query, (air_code,air_name,air_city))
    
    cursor.close()
    return redirect(url_for('add_airports'))
    
#=============================================================================
@app.route('/view_frequent_customers', methods=['GET', 'POST'])
def view_frequent_customers():
    username = session['username']
    auth = session['usertype']
    airline = session['staff_airline']
    
    cursor = conn.cursor()

    query = ("SELECT customer.email AS email, customer_name, COUNT(purchase.ticket_id) AS ticketsBought, SUM(sold_price) AS totalSpending "
             "FROM customer,purchase,ticket WHERE purchase.email = customer.email AND purchase_datetime >= CURRENT_TIMESTAMP - INTERVAL 1 year "
             "AND purchase.ticket_id=ticket.ticket_id AND ticket.airline_name = %s "
             "GROUP BY customer_name ORDER BY ticketsBought DESC LIMIT 10")
    cursor.execute(query, (airline))
    allFrequentCustomer = cursor.fetchall()
    
    cursor.close()
    return render_template('view_frequent_customers.html', username=username, auth=auth, airline=airline, allFrequentCustomer=allFrequentCustomer)

@app.route('/particular_customerSearch', methods=['GET', 'POST'])
def particular_customerSearch():
    username = session['username']
    auth = session['usertype']
    airline = session['staff_airline']
    
    cusEmail = request.form['cusEmail']
    
    cursor = conn.cursor()
    query = ("SELECT DISTINCT airline_name, flight_number, departure_datetime, purchase.ticket_id FROM purchase, ticket NATURAL JOIN flight "
             "WHERE purchase.ticket_id=ticket.ticket_id AND purchase.email = %s ORDER BY departure_datetime DESC")
    cursor.execute(query, (cusEmail))
    customerAllFlights = cursor.fetchall()
    
    cursor.close()
    return render_template("customers_all_flights.html", username=username, auth=auth, airline=airline, customerAllFlights=customerAllFlights, cusEmail=cusEmail)

#=============================================================================
#staff view reports and earned revenue
@app.route('/view_earned_revenue', methods=['GET', 'POST'])
def view_earned_revenue():
    username = session['username']
    auth = session['usertype']
    airline = session['staff_airline']
    
    cursor = conn.cursor()
    queryMonth = ("SELECT COUNT(ticket.ticket_id) AS ticketSold, SUM(purchase.sold_price) AS totalRevenue "
                  "FROM ticket,purchase WHERE ticket.ticket_id = purchase.ticket_id AND ticket.airline_name = %s "
                  "AND purchase.purchase_datetime >= CURRENT_TIMESTAMP - INTERVAL 1 month")
    cursor.execute(queryMonth, (airline))
    monthRevenue = cursor.fetchone()
    
    queryYear = ("SELECT COUNT(ticket.ticket_id) AS ticketSold, SUM(purchase.sold_price) AS totalRevenue "
                 "FROM ticket,purchase WHERE ticket.ticket_id = purchase.ticket_id AND ticket.airline_name = %s "
                 "AND purchase.purchase_datetime >= CURRENT_TIMESTAMP - INTERVAL 1 year")
    cursor.execute(queryYear, (airline))
    yearRevenue = cursor.fetchone()
    
    cursor.close()
    return render_template("view_earned_revenue.html", username=username, auth=auth, airline=airline, monthRevenue=monthRevenue, yearRevenue=yearRevenue)

@app.route('/view_earned_revenueSearch', methods=['GET', 'POST'])
def view_earned_revenueSearch():
    username = session['username']
    auth = session['usertype']
    airline = session['staff_airline']
    
    cursor = conn.cursor()
    queryMonth = ("SELECT COUNT(ticket.ticket_id) AS ticketSold, SUM(purchase.sold_price) AS totalRevenue "
                  "FROM ticket,purchase WHERE ticket.ticket_id = purchase.ticket_id AND ticket.airline_name = %s "
                  "AND purchase.purchase_datetime >= CURRENT_TIMESTAMP - INTERVAL 1 month")
    cursor.execute(queryMonth, (airline))
    monthRevenue = cursor.fetchone()
    
    queryYear = ("SELECT COUNT(ticket.ticket_id) AS ticketSold, SUM(purchase.sold_price) AS totalRevenue "
                 "FROM ticket,purchase WHERE ticket.ticket_id = purchase.ticket_id AND ticket.airline_name = %s "
                 "AND purchase.purchase_datetime >= CURRENT_TIMESTAMP - INTERVAL 1 year")
    cursor.execute(queryYear, (airline))
    yearRevenue = cursor.fetchone()
    
    startDate = request.form['startdate']
    endDate = request.form['enddate']
    
    querySearch = ("SELECT year(purchase.purchase_datetime) AS theYear, month(purchase.purchase_datetime) AS theMonth, COUNT(ticket.ticket_id) AS ticketSold, SUM(purchase.sold_price) AS totalRevenue "
                   "FROM ticket,purchase WHERE ticket.ticket_id = purchase.ticket_id AND ticket.airline_name = %s "
                   "AND date(purchase.purchase_datetime) >= %s and date(purchase.purchase_datetime) <= %s "
                   "GROUP BY year(purchase.purchase_datetime), month(purchase.purchase_datetime)")
    cursor.execute(querySearch, (airline, startDate, endDate))
    searchResult = cursor.fetchall()
    
    error = ""
    if not searchResult:
        error = "No Result."
    
    cursor.close()
    return render_template("view_earned_revenue.html", username=username, auth=auth, airline=airline,
                           monthRevenue=monthRevenue, yearRevenue=yearRevenue, searchResult=searchResult, error=error)

#=============================================================================
#staff view top destinations
@app.route('/view_top_destinations', methods=['GET', 'POST'])
def view_top_destinations():
    username = session['username']
    auth = session['usertype']
    airline = session['staff_airline']
    
    cursor = conn.cursor()
    queryMonth = ("SELECT airport.airport_code, airport.airport_name, airport.airport_city, COUNT(ticket.ticket_id) AS ticket_num "
                  "FROM purchase NATURAL JOIN ticket NATURAL JOIN flight, airport "
                  "WHERE flight.arrival_airport = airport.airport_code AND flight.airline_name = %s "
                  "AND purchase.purchase_datetime >= CURRENT_TIMESTAMP - INTERVAL 3 month "
                  "GROUP BY airport.airport_code ORDER BY ticket_num DESC "
                  "LIMIT 3")
    cursor.execute(queryMonth, (airline))
    monthDest = cursor.fetchall()
    
    queryYear = ("SELECT airport.airport_code, airport.airport_name, airport.airport_city, COUNT(ticket.ticket_id) AS ticket_num "
                 "FROM purchase NATURAL JOIN ticket NATURAL JOIN flight, airport "
                 "WHERE flight.arrival_airport = airport.airport_code AND flight.airline_name = %s "
                 "AND purchase.purchase_datetime >= CURRENT_TIMESTAMP - INTERVAL 1 year "
                 "GROUP BY airport.airport_code ORDER BY ticket_num DESC "
                 "LIMIT 3")
    cursor.execute(queryYear, (airline))
    yearDest = cursor.fetchall()
    
    cursor.close()
    return render_template("view_top_destinations.html", username=username, auth=auth, airline=airline, monthDest=monthDest, yearDest=yearDest)

#=============================================================================
#staff add phone
@app.route('/add_phone', methods=['GET', 'POST'])
def add_phone():
    username = session['username']
    auth = session['usertype']
    airline = session['staff_airline']
    
    cursor = conn.cursor()
    query = "SELECT phone_number FROM staffphone WHERE username = %s"
    cursor.execute(query, (username))
    phones = cursor.fetchall()
    
    cursor.close()
    return render_template("add_phone.html", username=username, auth=auth, airline=airline, phones=phones)

@app.route('/add_phoneConfirm', methods=['GET', 'POST'])
def add_phoneConfirm():
    username = session['username']
    auth = session['usertype']
    airline = session['staff_airline']
    
    phoneNum = request.form['phoneNum']
    
    cursor = conn.cursor()
    error = ""
    
    query = "SELECT phone_number FROM staffphone WHERE username = %s"
    cursor.execute(query, (username))
    phones = cursor.fetchall()
    
    queryCheckExist = "SELECT * FROM staffphone WHERE phone_number = %s"
    cursor.execute(queryCheckExist, (phoneNum))
    phoneExist = cursor.fetchone()
    
    if phoneExist:
        error = "Phone number already exist in system."
        return render_template("add_phone.html", username=username, auth=auth, airline=airline, phones=phones, error=error)
    else:
        queryIns = "INSERT INTO staffphone VALUES (%s,%s)"
        cursor.execute(queryIns, (username,phoneNum))
        
        cursor.close()
        return redirect(url_for('add_phone'))

#=============================================================================
#logout method
@app.route('/logout')
def logout():
    session.pop('username')
    #authType.pop('username')
    return redirect('/')
		
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)


