from django.http.response import HttpResponse
from django.shortcuts import render
from minesite.models import *
from minesite.forms import *
from minesite.classes import *
from datetime import date, datetime

def main_minesite(request):
    return render(request, "main_minesite.html")

def login(request):
    username = "not logged in"
    errors = []
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        verify_data = verify(username,password)
        verify_data.r_username()
        verify_data.r_password()
        errors = verify_data.r_errors()
        try:
            dbuser = LoginModel.objects.get(username = username)
            if password != dbuser.password:
                return render(request,template_name="login.html", context={'errors':['Incorrect Password!']})
        except:
            return render(request,template_name="login.html", context={'errors':["Username does not Exist!"]})

        loginform = LoginForm(request.POST)        
        if loginform.is_valid():
            #information = loginform.cleaned_info()
            #username = information['username']
            if errors == []:
                name = dbuser.name
                username = dbuser.username
                return render(request, "homepage.html",{"name":name, 'username':username})
    else:
        loginform = LoginForm() 
    return render(request, "login.html", {'errors':errors})

def signup(request):
    errors = list()
    if request.method == "POST":
        name = request.POST['name']
        username = request.POST['username']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        email = request.POST['email']
        verify_data = verify(username,password,name,confirmpassword,email)
        verify_data.r_username()
        verify_data.r_password()
        verify_data.r_name()
        verify_data.r_confirmpassword()
        verify_data.r_email()
        errors = verify_data.r_errors()
        try:
            LoginModel.objects.get(username = username)
            errors += ["Username already exists. Please try a different Username."]
        except:
            pass
        if errors == []:
            data = LoginModel(username=username, password = password, name = name, email = email)
            data.save() 
            return render(request, "homepage.html",{"name":name})
    else:
        signupform = SignupForm()
    return render(request, "signup.html",{'errors':errors}) 

def homepage(request):
    return render(request, "homepage.html",{})

def myupcomingflights(request,username):
    transactions = Transactions.objects.filter(username=username)
    num_transactions = len(transactions)
    minetransactions = []
    for i in range(num_transactions):
        transaction = transactions[i]
        if transaction.flightdate<date.today():
            continue
        flightcode = transaction.code
        transaction_num = transaction.transaction_num
        fromplace = transaction.fromplace
        toplace = transaction.toplace
        paymentmode = transaction.paymentmode
        flightclass = transaction.flightclass
        seatnumbers = transaction.seatnumbers
        mealpreferance = transaction.mealpreferance
        flightdate = transaction.flightdate
        flighttime = transaction.flighttime
        flightdetails = FlightDetails.objects.filter(code=flightcode)[:1].get()
        status = flightdetails.status
        minetransactions += [{'code':flightcode,'transaction_num':transaction_num,'fromplace':fromplace,'toplace':toplace,'paymentmode':paymentmode,'flightclass':flightclass,'seatnumbers':seatnumbers,'mealpreferance':mealpreferance,'flightdate':str(flightdate),'flighttime':str(flighttime),'status':status}]
    return render(request,"upcomingflights.html",{'username':username,'transactions':minetransactions[-1::-1]})

def mytransactions(request,username):
    transactions = Transactions.objects.filter(username=username)
    num_transactions = len(transactions)
    minetransactions = []
    for i in range(num_transactions):
        transaction = transactions[i]
        flightcode = transaction.code
        transaction_num = transaction.transaction_num
        fromplace = transaction.fromplace
        toplace = transaction.toplace
        paymentmode = transaction.paymentmode
        flightclass = transaction.flightclass
        seatnumbers = transaction.seatnumbers
        mealpreferance = transaction.mealpreferance
        flightdate = transaction.flightdate
        flighttime = transaction.flighttime
        flightdetails = FlightDetails.objects.filter(code=flightcode)[:1].get()
        status = flightdetails.status
        minetransactions += [{'code':flightcode,'transaction_num':transaction_num,'fromplace':fromplace,'toplace':toplace,'paymentmode':paymentmode,'flightclass':flightclass,'seatnumbers':seatnumbers,'mealpreferance':mealpreferance,'flightdate':str(flightdate),'flighttime':str(flighttime),'status':status}]
    return render(request,"mytransactions.html",{'username':username,'transactions':minetransactions[-1::-1]})

def select_flight(request,username):
    errors = []
    currentdate = date.today()
    if request.method == "POST":
        fromplace = request.POST['from'].title()
        toplace = request.POST['to'].title()
        num_passangers = int(request.POST['num_passangers'])
        flightclass = request.POST['class']
        flightdate = request.POST['date']
        verify_data = verify(fromplace=fromplace,toplace=toplace)
        verify_data.r_fromplace()
        verify_data.r_toplace()
        errors = verify_data.r_errors()
        try:
            flightdetails = FlightDetails.objects.get(date=flightdate,fromplace=fromplace,toplace=toplace,status="CONFIRMED")
            if flightclass == "Economy" and flightdetails.e_numseats >0 and flightdetails.e_numseats>=num_passangers:
                price = flightdetails.e_price
                total = price*num_passangers
                flightcode = flightdetails.code
                return render(request, "transactionpage.html", {'fromplace':fromplace,'toplace':toplace,'flightclass':flightclass,'price':price,'number':num_passangers,'total':total,'flightcode':flightcode, 'username':username, 'errors':errors})
            elif flightclass == "Business" and flightdetails.b_numseats>0 and flightdetails.b_numseats>=num_passangers:
                price = flightdetails.b_price
                total = price*num_passangers
                flightcode = flightdetails.code
                return render(request, "transactionpage.html", {'fromplace':fromplace,'toplace':toplace,'flightclass':flightclass,'price':price,'number':num_passangers,'total':total,'flightcode':flightcode, 'username':username, 'errors':errors})
            else:   
                errors += [str(num_passangers)+" Seats are not Available in "+flightclass+' Class']
                return render(request, "flight_selection.html", {'username':username,'currentdate':str(currentdate), 'errors':errors})
        except:
            if errors == []: 
                try:
                    flightdetails = FlightDetails.objects.get(fromplace=fromplace)
                except:
                    errors += ['No flights from this country. Please choose another Departure Country.']
                try:
                    flightdetails = FlightDetails.objects.get(toplace=toplace)
                except:
                    errors += ['No flights to this country. Please choose another Arrival Country.']
            try:
                flightdetails = FlightDetails.objects.get(flightdate=flightdate)
            except:
                errors += ['No flights available. Please choose another Date.']
            return render(request, "flight_selection.html", {'username':username, 'currentdate':str(currentdate), 'errors':errors})
        
    return render(request, "flight_selection.html", {'username':username,'currentdate':str(currentdate), 'errors':errors})

def account_details(request,username):
    dbuser = LoginModel.objects.get(username=username)
    name = dbuser.name
    email = dbuser.email
    return render(request, "account_details.html", {"username":username, "name":name, "email":email})

def edit_account_details(request,username):
    errors = []
    if request.method == "POST":
        name = request.POST['name']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        email = request.POST['email']
        verify_data = verify(username,password,name,confirmpassword,email)
        verify_data.r_username()
        verify_data.r_password()
        verify_data.r_name()
        verify_data.r_confirmpassword()
        verify_data.r_email()
        errors = verify_data.r_errors()
        if errors == []:
            data = LoginModel.objects.get(username=username)
            data.name = name
            data.password = password
            data.email = email
            data.save()
            return render(request, "account_details_updated.html", {'username':username})
            
    dbuser = LoginModel.objects.get(username=username)
    name = dbuser.name
    email = dbuser.email
    return render(request, "edit_account_details.html", {'username':username, 'name':name, 'email':email, 'errors':errors})

def transaction_page(request):
    if request.method == "POST":
        flightcode = request.POST['flightcode']
        flightclass = request.POST['flightclass']
        num_passangers = request.POST['num_passangers']
        username = request.POST['username']
        paymentmode = request.POST['paymentmode']
        total = request.POST['total']
        flightdetails = FlightDetails.objects.get(code=flightcode)
        fromplace = request.POST.get('fromplace')
        toplace = request.POST.get('toplace')
        flightdate = flightdetails.date
        flighttime = flightdetails.time
        now = datetime.now()
        currenttime = now.strftime("%H:%M:%S")
        for i in range(int(num_passangers)):
            transactionnum = Transactions.objects.latest("transaction_num")
            transaction_num = int(transactionnum.transaction_num) + 1
            transaction = Transactions(username=username, code=flightcode,time=currenttime,fromplace=fromplace,toplace=toplace,num_passangers=num_passangers, total=total,paymentmode=paymentmode,flightclass=flightclass,seatnumbers=" ",mealpreferance="Vegetarian",flightdate=flightdate,flighttime=flighttime, transaction_num=transaction_num)
            transaction.save()
        bookedseats = list(Transactions.objects.filter(code=flightcode, flighttime=flighttime, flightdate=flightdate))
        if flightclass == "Economy":
            return render(request, "e_seatselectionpage.html",{'num':[i for i in range(1,41)],'num_seats':num_passangers, 'username':username, 'bookedseats':bookedseats, 'flightcode':flightcode})
        else:
            return render(request, "b_seatselectionpage.html",{'num':[i for i in range(1,11)],'num_seats':num_passangers, 'username':username, 'bookedseats':bookedseats, 'flightcode':flightcode})
    return render(request, "transactionpage.html",{})

def e_seatselection_page(request):
    errors = []
    if request.method == "POST":
        seats = request.POST.getlist('seat')
        username = request.POST['username']
        num_seats = request.POST['num_seats']
        flightcode = request.POST['flightcode']
        flightdetails = FlightDetails.objects.get(code=flightcode)
        flightdate = flightdetails.date
        flighttime = flightdetails.time
        bookedseats = list(Transactions.objects.filter(code=flightcode, flighttime=flighttime, flightdate=flightdate))
        if int(num_seats) > len(seats):
            errors += ['Choose '+str(int(num_seats)-len(seats))+' more Seats']
            return render(request, "e_seatselectionpage.html",{'errors':errors, 'num':[i for i in range(1,41)],'num_seats':num_seats, 'username':username, 'bookedseats':bookedseats, 'flightcode':flightcode})
        elif int(num_seats) < len(seats):
            errors += ['You chose more than '+str(num_seats)+' seats.']
            return render(request, "e_seatselectionpage.html",{'errors':errors, 'num':[i for i in range(1,41)],'num_seats':num_seats, 'username':username, 'bookedseats':bookedseats, 'flightcode':flightcode})
        else:
            pass
        try:
            if errors == []:
                for i in range(int(num_seats)):
                    transactions = Transactions.objects.filter(username=username,flightdate=flightdate,flighttime=flighttime,seatnumbers=" ")[:1].get()
                    transactions.seatnumbers = seats[i]
                    transactions.mealpreferance = request.POST["meal"]
                    transactions.save()      
                flightdetail = FlightDetails.objects.filter(code=flightcode)[:1].get()
                e_numseats = getattr(flightdetail,'e_numseats') 
                calc = int(e_numseats)-int(num_seats)
                flightdetails.e_numseats = calc
                flightdetails.save()
                return render(request,"seatconfirmed.html")
        except:
            return render(request,"seatdenied.html")

    return render(request, "e_seatselectionpage.html",{'errors':errors})

def b_seatselection_page(request):
    errors = []
    if request.method == "POST":
        seats = request.POST.getlist('seat')
        username = request.POST['username']
        num_seats = request.POST['num_seats']
        flightcode = request.POST['flightcode']
        flightdetails = FlightDetails.objects.get(code=flightcode)
        flightdate = flightdetails.date
        flighttime = flightdetails.time
        bookedseats = list(Transactions.objects.filter(code=flightcode, flighttime=flighttime, flightdate=flightdate))
        if int(num_seats) > len(seats):
            errors += ['Choose '+str(int(num_seats)-len(seats))+' more Seats']
            return render(request, "b_seatselectionpage.html",{'errors':errors, 'num':[i for i in range(1,11)],'num_seats':num_seats, 'username':username, 'bookedseats':bookedseats, 'flightcode':flightcode})
        elif int(num_seats) < len(seats):
            errors += ['You chose more than '+num_seats+' seats.']
            return render(request, "b_seatselectionpage.html",{'errors':errors, 'num':[i for i in range(1,11)],'num_seats':num_seats, 'username':username, 'bookedseats':bookedseats, 'flightcode':flightcode})
        else:
            pass
        try:
            if errors == []:
                for i in range(int(num_seats)):
                    transactions = Transactions.objects.filter(username=username,flightdate=flightdate,flighttime=flighttime,seatnumbers=" ")[:1].get()
                    transactions.seatnumbers = seats[i]
                    transactions.mealpreferance = request.POST["meal"]
                    transactions.save()
                flightdetail = FlightDetails.objects.filter(code=flightcode)[:1].get()
                e_numseats = getattr(flightdetail,'b_numseats') 
                calc = int(e_numseats)-int(num_seats)
                flightdetails.b_numseats = calc
                flightdetails.save()
                return render(request,"seatconfirmed.html")
        except:
            return render(request,"seatdenied.html")

    return render(request, "b_seatselectionpage.html",{'errors':errors})

def deletetransaction(request,transactionid):
    Transactions.objects.filter(transaction_num=transactionid).delete()
    return render(request,"deletedtransaction.html")

def deleteaccount(request,username):
    user = LoginModel.objects.get(username=username)
    user.delete()
    return render(request,"accountdeletedpage.html")

def aboutus(request):
    return render(request, "about.html")