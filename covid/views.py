
import datetime
import json

import pyrebase
from django.shortcuts import render,redirect
from django.conf import settings
from django.contrib import auth
import webbrowser
import os
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.contrib import messages
import re
from .x import write_in_sheet
from .utils import render_to_pdf
from .todrive import to_drive
from .pdf import hello

from django.core.mail import EmailMessage
# config = {
#   'apiKey': "AIzaSyCem898av3L1upKEgiju3AlpP_3Y-npP74",
#   'authDomain': "covidcrisis-312210.firebaseapp.com",
#   'databaseURL': "https://covidcrisis-312210-default-rtdb.firebaseio.com",
#   'projectId': "covidcrisis-312210",
#   'storageBucket': "covidcrisis-312210.appspot.com",
#   'messagingSenderId': "767269885711",
#   'appId': "1:767269885711:web:5c358d78c6ef37953e507a"
# }

#For Firebase JS SDK v7.20.0 and later, measurementId is optional
config= {
  'apiKey': "AIzaSyA0QWwHeUY9YP2ueryzYRA8zhiKMC32nS4",
  'authDomain': "opdonthego-47eec.firebaseapp.com",
  'projectId': "opdonthego-47eec",
  'storageBucket': "opdonthego-47eec.appspot.com",
  'messagingSenderId': "968501440458",
  'appId': "1:968501440458:web:01793f30e9c35b4b622933",
  'measurementId': "G-46PDW6H1DF",
  'databaseURL':"https://opdonthego-47eec-default-rtdb.firebaseio.com",


}
firebase = pyrebase.initialize_app(config)
database = firebase.database()
authe = firebase.auth()

def login(request):
    return render(request, "login.html")

def logout(request):
    auth.logout(request)
    return render(request, "login.html")



def Login(request):
    email = request.POST.get("email")
    password = request.POST.get("password")
    print("hey")
    print(email)

    print(password)
    try:
        user = firebase.auth().sign_in_with_email_and_password(email, password)
        print(user)
        session_id = str(user['localId'])

        #print(session_id)
        #print("1")
        request.session['email'] = str(email)
        print("2")

        names,ids=[],[]
        a = database.child("Doctor_Data").get()
        # print(a)
        drname = ""
        info2 = [x.val() for x in a.each()]
        print(info2)
        drs = []
        for y in info2:
            print(y['Name'])
            drs.append(y['Name'])
            print("1")



        #print(user)
        print(drs)
        #email = request.session.get('email')
        if str(email)=="rishabhraghuvanshi.10.e.fe@gmail.com":
            print("ooooooo")
            name_id = database.child("Doctor").get()
            info = [x.val() for x in name_id.each()]
            print(info)
            for i in info:
                for x in i.values():
                    names.append(x['Name'])
                    ids.append(x['ID'])

            print(names,ids)
            combilist= zip(names,ids)
            combi2= zip(names,ids)
            print("123")
            combi3 = zip(names,ids)
            print("horsestyle")


            return render(request,"adminpatientname.html",{"combi":combilist,"combi2":combi2,"combi3":combi3,"drs":drs})


        #print(email)
        #print(a)
        print("hello")
        drname = ""
        info2 = [x.val() for x in a.each()]
        print(info2)
        for y in info2:
            if y['Email'] == email:
                drname = y['Name']
        request.session['drname'] = str(drname)

        #print(drname)
        name = []
        id = []
        doctors = database.child("Doctor").child(drname).get()
        drs_patient = [d.val() for d in doctors.each()]
        print(drs_patient)
        for x in drs_patient:
            print(x)
            name.append(x['Name'])
            id.append(x['ID'])

        print(name, id)

        combi = zip(name, id)
        return render(request, "patientsname.html",{"data":combi})
    except Exception as e:
        print(e)
        message = "Invalid Email-id or password"
        return render(request, "login.html", {"message": message, })







def reset(request):
    email = request.POST.get("email")
    authe.send_password_reset_email(email)
    return render(request, "login.html")

def homepage(request):
    return render(request,"homepage.html")

def patientlist(request):

    email=request.session.get('email')
    print(email)

    # if str(email) == "ruchitthaker.43.e.fe@gmail.com":
    #     names, ids = [], []
    #     a = database.child("Doctor_Data").get()
    #     # print(a)
    #     drname = ""
    #     info2 = [x.val() for x in a.each()]
    #     print(info2)
    #     drs = []
    #     for y in info2:
    #         print(y['Name'])
    #         drs.append(y['Name'])
    #         print("1")
    #     print("ooooooo")
    #     name_id = database.child("Doctor").get()
    #     info = [x.val() for x in name_id.each()]
    #     print(info)
    #     for i in info:
    #         for x in i.values():
    #             names.append(x['Name'])
    #             ids.append(x['ID'])
    #
    #     print(names, ids)
    #     combilist = zip(names, ids)
    #     combi2 = zip(names, ids)
    #     print("123")
    #     combi3 = zip(names, ids)
    #     print("horsestyle")
    #
    #     return render(request, "adminpatientname.html",
    #                   {"combi": combilist, "combi2": combi2, "combi3": combi3, "drs": drs})


    a = database.child("Doctor_Data").get()
    print(a)
    drname=""
    info = [x.val() for x in a.each()]
    print(info)
    for y in info:
        if y['Email']==email:
            drname=y['Name']

    print(drname)
    name = []
    id = []
    doctors=database.child("Doctor").child(drname).get()
    drs_patient=[d.val() for d in doctors.each()]
    print(drs_patient)
    for x in drs_patient:
        print(x)
        name.append(x['Name'])
        id.append(x['ID'])


    print(name,id)




    combi=zip(name,id)
    data="a"
    return render(request,"patientsname.html",{"data":combi})



# def patientdashboard(request):
#
#   return render(request,"patientdashboard.html")
#
# def persdetails(request):
#
#   return render(request,"personal.html")

def patientdetails(request,ID):

    print(ID)
    x = str(ID)
    i = 0
    y = ""
    for i in range(0, len(x)):
        if x[i] == 'D':
            y = "Diabetes"
        elif x[i] == 'S':
            y += "Heart Disease/Stroke"
        elif x[i] == 'O':
            y += "Obesity"
        elif x[i] == 'L':
            y += "Liver Disease"
        elif x[i] == 'T':
            y += "Stent"
        elif x[i] == 'C':
            y += "CKD"
        elif x[i] == 'B':
            y += "Bypass"
        elif x[i] == 'm':
            y += "(On medication), "
        elif x[i] == 'c':
            y += "(Controlled), "
        else:
            y += ""
    y = y[:-2]
    print(database.child("Personal_Details").child(ID).get(),"sdadas")
    pers = database.child("Personal_Details").child(ID).get()
    info1 = [t.val() for t in pers.each()]
    print(info1)
    med = database.child("Medical_Details").child(ID).get()
    info2 = [x.val() for x in med.each()]

    dtfromform = info1[1]
    formatteddate = dtfromform[:10]
    date_1 = datetime.datetime.strptime(formatteddate, '%Y-%m-%d')
    end_date = date_1 + datetime.timedelta(days=1)
    finaldate = str(end_date)
    finaldate=finaldate[0:10]




    try:
        data_in_database = database.child("Var_Med_Details").child(ID).child("others").child("1").get()
        print(data_in_database.each)
        print("x")
        item = data_in_database

        item = data_in_database
        try:
            if (item.val()['HRCT'] != ""):
                info2[9] = item.val()['HRCT']
        except:
            print("nohrct")
        try:
            if (item.val()['CRP'] != ""):
                info2[-7] = item.val()['CRP']
        except:
            print("nocrp")
        try:
            if (item.val()['others'] != ""):
                info2[-6] = item.val()['others']
        except:
            print("noothers")

        # updated_meds=database.child('Var_Med_Details').child(id).child("others").child("1").get()
        # info4 = [x.val() for x in updated_meds.each()]
        # if (info4):
        #     info2[9]=info4[1]
        #     info2[-7]=info4[0]
        #     info2[-6]=info4[4]
        new_symptoms = ""
        ddimer = ""
        try:
            if item.val()['newsymp'] != "":
                new_symptoms = item.val()['newsymp']
        except:
            print("nonewsymptoms")
        try:
            if item.val()['ddimer']:
                ddimer = item.val()['ddimer']
        except:
            print("noddimer")



    except:
        new_symptoms = "_"
        ddimer = "_"
        print("hii")
    d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14 = "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_"

    try:
        d1 = info2[3]
        spo2 = database.child("Var_Med_Details").child(ID).child("SpO2").child("1").get()
        spo2_rec = spo2
        try:
            if (spo2.val()['d2'] != "" or spo2.val()['d3'] != "" or spo2.val()['d4'] != "" or spo2.val()['d5'] != ""):
                d1 = spo2.val()['d1']
                d2 = spo2.val()['d2']
                d3 = spo2.val()['d3']
                d4 = spo2.val()['d4']
                d5 = spo2.val()['d5']
                d6 = spo2.val()['d6']
                d7 = spo2.val()['d7']
                d8 = spo2.val()['d8']
                d9 = spo2.val()['d9']
                d10 = spo2.val()['d10']
                d11 = spo2.val()['d11']
                d12 = spo2.val()['d12']
                d13 = spo2.val()['d13']
                d14 = spo2.val()['d14']




        except:
            print("nospo2")



    except:
        print("hii2")
        d2 = "-"
        d3 = "-"
        d4 = "-"
        d5 = "-"
        d6 = "-"
        d7 = "-"
        d8 = "-"
        d9 = "-"
        d10 = "-"
        d11 = "-"
        d12 = "-"
        d13 = "-"
        d14 = "-"

    try:
        No_of_pres = list(database.child("prescription").child(ID).shallow().get().val())
        num = len(No_of_pres)

        combilis = []
        for i in range(num, 0, -1):
            prescription = "PRESCRIPTION " + str(i)
            pres = list(database.child("prescription").child(ID).child(prescription).get().val().items())
            medicine = (pres[0][1]).split(",")
            mg = (pres[1][1]).split(",")
            notes = (pres[2][1]).split(",")
            time = (pres[3][1]).split(",")
            combi = zip(medicine, mg, time, notes)
            combilis.append(combi)

        prescnum = list(range(len(combilis), 0, -1))

        print(prescnum)
        combilis = zip(combilis, prescnum)
    except:
        print("hoo")
        patient_data = {
            "Name": info1[6],
            "ID": ID,
            "Age": info1[0],
            "Mobile": info1[5],
            "Email": info1[2],
            "Location": info1[4],
            "Sex": info1[7],
            "Date": finaldate,

            "Fileno": info1[-1],

            "RTPCR": info2[-5],
            "CT": info2[-4],
            "Past": y,
            "Symptoms": info2[-3],
            "Firstsymp": info2[5],
            "Currspo2": info2[3],
            "Vacstat": info2[2],
            "1stvac": info2[6],
            "2ndvac": info2[8],
            "vaccomp": info2[0],
            "hrct": info2[9],
            "CRP": info2[-7],
            "multiple_vals": info2[-6],
            "curr_treatent": info2[4],
            "date_presc": info2[7],
            "Other_recent_investigation": info2[1],
            "Treatment_prescribed_while_filling_form": info2[-1],
            "newsymp": new_symptoms,
            "ddimer": ddimer,
            "day1": info2[3],
            "day2": d2,
            "day3": d3,
            "day4": d4,
            "day5": d5,
            "day6": d6,
            "day7": d7,
            "day8": d8,
            "day9": d9,
            "day10": d10,
            "day11": d11,
            "day12": d12,
            "day13": d13,
            "day14": d14

        }

        return render(request, "patientdetails.html", patient_data)

    patient_data = {
        "Name": info1[6],
        "ID": ID,
        "Age": info1[0],
        "Mobile": info1[5],
        "Email": info1[2],
        "Location": info1[4],
        "Sex": info1[7],
        "Date":finaldate,

        "Fileno": info1[-1],

        "RTPCR": info2[-5],
        "CT": info2[-4],
        "Past": y,
        "Symptoms": info2[-3],
        "Firstsymp": info2[5],
        "Currspo2": info2[3],
        "Vacstat": info2[2],
        "1stvac": info2[6],
        "2ndvac": info2[8],
        "vaccomp": info2[0],
        "hrct": info2[9],
        "CRP": info2[-7],
        "multiple_vals": info2[-6],
        "curr_treatent": info2[4],
        "date_presc": info2[7],
        "Other_recent_investigation": info2[1],
        "Treatment_prescribed_while_filling_form": info2[-1],
        "newsymp": new_symptoms,
        "ddimer": ddimer,
        "day1": info2[3],
        "day2": d2,
        "day3": d3,
        "day4": d4,
        "day5": d5,
        "day6": d6,
        "day7": d7,
        "day8": d8,
        "day9": d9,
        "day10": d10,
        "day11": d11,
        "day12": d12,
        "day13": d13,
        "day14": d14,
        "combilis":combilis

    }

    return render(request, "patientdetails.html",patient_data)

def presc(request):
    return render(request,"presc.html")


def sub(request):
    print("i am in")
    data = json.loads(request.POST['json'])
    print(data)
    print(type(data))

    id = request.POST.get('pat_id')
    mob = request.POST.get('pat_mob')
    email = request.POST.get('pat_email')
    if email==None or email=="":
        email=""
    # Whatsapp
    import pywhatkit

    wait_time = 10
    print(data)
    medicine, mg, time, notes = "", "", "", ""
    j = 1
    line = "----------------------------------------\n"
    message = "ALERT PRESCRIPTION UPDATE\n"
    for i in data:
        medicine = medicine + "," + i["medicine"]
        mg = mg + "," + i["mg"]
        time = time + "," + i["time"]
        notes = notes + "," + i["notes"]

        submsg = line + "" + str(j) + ".\n" + "Rx " + i["medicine"] + "\nPower:" + i["mg"] + "mg\nTime: " + i[
            "time"] + "\n" + \
                 i["notes"] + "\n"
        message = message + submsg
        j = j + 1

    medicine = medicine[1:]
    mg = mg[1:]
    time = time[1:]
    notes = notes[1:]

    med1, mg1, time1, notes1 = [], [], [], []
    med1 = medicine.split(",")
    mg1 = mg.split(",")
    time1 = time.split(",")
    notes1 = notes.split(",")
    print(med1)
    print(mg1)
    print(time1)
    print(notes1)
    pers = database.child("Personal_Details").child(id).get()
    info1 = [x.val() for x in pers.each()]
    name = info1[6]
    zippresc = zip(med1, mg1, time1, notes1)

    hello(zippresc,med1, mg1, time1, notes1, name, str(id), mob)

    # database store
    try:
        No_of_pres = list(database.child("prescription").child(id).shallow().get().val())
        num = len(No_of_pres) + 1
        prescription = "PRESCRIPTION " + str(num)
        dat = {"medicine": medicine, "mg": mg, "time": time, "notes": notes}
        database.child("prescription").child(id).child(prescription).set(dat)
    except:

        dat = {"medicine": medicine, "mg": mg, "time": time, "notes": notes}
        database.child("prescription").child(id).child("PRESCRIPTION 1").set(dat)
    # -------------------------------------------------------------------------------
    # db ret
    No_of_pres = list(database.child("prescription").child(id).shallow().get().val())
    num = len(No_of_pres)

    combilis = []
    for i in range(num, 0, -1):
        prescription = "PRESCRIPTION " + str(i)
        pres = list(database.child("prescription").child(id).child(prescription).get().val().items())
        medicine = (pres[0][1]).split(",")
        mg = (pres[1][1]).split(",")
        notes = (pres[2][1]).split(",")
        time = (pres[3][1]).split(",")
        combi = zip(medicine, mg, time, notes)
        combilis.append(combi)

    # ---------------------------------Whatsapp------------------------------------------------------------
    message = message + "\n*Please Note*: A pdf copy of prescription is sent on your registered email-id."
    try:
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        time_hour = int(current_time[:2])
        time_min = int(current_time[3:5]) + 1

        print("whatsapp")
        pywhatkit.sendwhatmsg("+91" + mob, message, time_hour, time_min, wait_time)
    except:
        pass
    print("whatsapp")

    # ---------------------------------------------------------------------------------

    # email
    print("whatsapp")
    try:
        html_content = "Attached below is the updated prescription."
        email = EmailMessage("CC-Prescription", html_content,
                             "opdonthego@gmail.com", [email])
        email.content_subtype = "html"
        email.attach_file('media/prescription'+str(id)+'.pdf')
        res = email.send()

        delete = default_storage.delete('prescription'+id+'.pdf')


    except:
        pass
    print("whatsapp")

    # ------------------------------------------
    prescnum = list(range(len(combilis), 0, -1))

    print(prescnum)
    combilis = zip(combilis, prescnum)

    # _______________________________#
    print(id)
    x = str(id)
    i = 0
    y = ""
    for i in range(0, len(x)):
        if x[i] == 'D':
            y = "Diabetes"
        elif x[i] == 'S':
            y += "Heart Disease/Stroke"
        elif x[i] == 'O':
            y += "Obesity"
        elif x[i] == 'L':
            y += "Liver Disease"
        elif x[i] == 'T':
            y += "Stent"
        elif x[i] == 'C':
            y += "CKD"
        elif x[i] == 'B':
            y += "Bypass"
        elif x[i] == 'm':
            y += "(On medication), "
        elif x[i] == 'c':
            y += "(Controlled), "
        else:
            y += ""
    y = y[:-2]

    # print(info1)
    med = database.child("Medical_Details").child(id).get()
    info2 = [x.val() for x in med.each()]

    dtfromform = info1[1]
    formatteddate = dtfromform[:10]
    date_1 = datetime.datetime.strptime(formatteddate, '%Y-%m-%d')
    end_date = date_1 + datetime.timedelta(days=1)
    finaldate = str(end_date)
    finaldate = finaldate[0:10]

    try:
        data_in_database = database.child("Var_Med_Details").child(id).child("others").child("1").get()
        print(data_in_database.each)
        print("x")

        item = data_in_database
        try:
            if (item.val()['HRCT'] != ""):
                info2[9] = item.val()['HRCT']
        except:
            print("nohrct")
        try:
            if (item.val()['CRP'] != ""):
                info2[-7] = item.val()['CRP']
        except:
            print("nocrp")
        try:
            if (item.val()['others'] != ""):
                info2[-6] = item.val()['others']
        except:
            print("noothers")

        # updated_meds=database.child('Var_Med_Details').child(id).child("others").child("1").get()
        # info4 = [x.val() for x in updated_meds.each()]
        # if (info4):
        #     info2[9]=info4[1]
        #     info2[-7]=info4[0]
        #     info2[-6]=info4[4]
        new_symptoms = ""
        ddimer = ""
        try:
            if item.val()['newsymp'] != "":
                new_symptoms = item.val()['newsymp']
        except:
            print("nonewsymptoms")
        try:
            if item.val()['ddimer']:
                ddimer = item.val()['ddimer']
        except:
            print("noddimer")



    except:
        new_symptoms = "_"
        ddimer = "_"
        print("hiiiiii")

    d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14 = "", "", "", "", "", "", "", "", "", "", "", "", "_"

    try:
        d1 = info2[3]
        spo2 = database.child("Var_Med_Details").child(id).child("SpO2").child("1").get()
        spo2_rec = spo2
        try:
            if (spo2.val()['d2'] != "" or spo2.val()['d3'] != "" or spo2.val()['d4'] != "" or spo2.val()[
                'd5'] != ""):
                d1 = spo2.val()['d1']
                d2 = spo2.val()['d2']
                d3 = spo2.val()['d3']
                d4 = spo2.val()['d4']
                d5 = spo2.val()['d5']
                d6 = spo2.val()['d6']
                d7 = spo2.val()['d7']
                d8 = spo2.val()['d8']
                d9 = spo2.val()['d9']
                d10 = spo2.val()['d10']
                d11 = spo2.val()['d11']
                d12 = spo2.val()['d12']
                d13 = spo2.val()['d13']
                d14 = spo2.val()['d14']




        except:
            print("nospo2")



    except:
        print("hii2")
        d2 = "-"
        d3 = "-"
        d4 = "-"
        d5 = "-"
        d6 = "-"
        d7 = "-"
        d8 = "-"
        d9 = "-"
        d10 = "-"
        d11 = "-"
        d12 = "-"
        d13 = "-"
        d14 = "-"

    patient_data = {
        "Name": info1[6],
        "ID": id,
        "Age": info1[0],
        "Mobile": info1[5],
        "Email": info1[2],
        "Location": info1[4],
        "Sex": info1[7],
        "Date": finaldate,

        "Fileno": info1[-1],

        "RTPCR": info2[-5],
        "CT": info2[-4],
        "Past": y,
        "Symptoms": info2[-3],
        "Firstsymp": info2[5],
        "Currspo2": info2[3],
        "Vacstat": info2[2],
        "1stvac": info2[6],
        "2ndvac": info2[8],
        "vaccomp": info2[0],
        "hrct": info2[9],
        "CRP": info2[-7],
        "multiple_vals": info2[-6],
        "curr_treatent": info2[4],
        "date_presc": info2[7],
        "Other_recent_investigation": info2[1],
        "Treatment_prescribed_while_filling_form": info2[-1],
        "newsymp": new_symptoms,
        "ddimer": ddimer,
        "day1": info2[3],
        "day2": d2,
        "day3": d3,
        "day4": d4,
        "day5": d5,
        "day6": d6,
        "day7": d7,
        "day8": d8,
        "day9": d9,
        "day10": d10,
        "day11": d11,
        "day12": d12,
        "day13": d13,
        "day14": d14,
        "combilis": combilis

    }

    # _______________________________#

    return render(request, "patientdetails.html", patient_data)


def medupdate(request):
    print("hello")
    id=request.POST.get("pat_id")
    hrct_score=request.POST.get("hrct")
    crp_value = request.POST.get("crp")
    otherinvest = request.POST.get("others")
    ddimer = request.POST.get("anyother")
    newsymp = request.POST.get("newsymp")
    print("hi"+ddimer+"ih")


    if hrct_score=="":
        h=database.child("Var_Med_Details").child(id).child("others").child("1").child("HRCT").get().val()
        if h!="":
            hrct_score=h
        else:
            hrct_score=database.child("Medical_Details").child(id).child("HRCT_CT_Score_out_of_25").get().val()
    if crp_value == "":
        c = database.child("Var_Med_Details").child(id).child("others").child("1").child("CRP").get().val()
        if c!="":
            crp_value=c
        else:
            crp_value=database.child("Medical_Details").child(id).child("Investigations_CRP_Values_mg_per_L_with_dates").get().val()
    if otherinvest == "":
        o = database.child("Var_Med_Details").child(id).child("others").child("1").child("others").get().val()
        if o!="":
            otherinvest=o
        else:
            otherinvest=database.child("Medical_Details").child(id).child("Investigations_Hb_TLC_Nutrophils_Lynphosities_PlatletClount_RDW_and_ESR").get().val()
    if ddimer == "":
        ddimer = database.child("Var_Med_Details").child(id).child("others").child("1").child("ddimer").get().val()
    if newsymp == "":
        newsymp = database.child("Var_Med_Details").child(id).child("others").child("1").child("newsymp").get().val()

    print(id)
    print(hrct_score)
    medupdate_data={
        "HRCT":hrct_score,
        "CRP":crp_value,
        "others":otherinvest,
        "ddimer":ddimer,
        "newsymp":newsymp
    }

    database.child("Var_Med_Details").child(id).child("others").child("1").set(medupdate_data)

    print(id)
    x = str(id)
    i = 0
    y = ""
    for i in range(0, len(x)):
        if x[i] == 'D':
            y = "Diabetes"
        elif x[i] == 'S':
            y += "Heart Disease/Stroke"
        elif x[i] == 'O':
            y += "Obesity"
        elif x[i] == 'L':
            y += "Liver Disease"
        elif x[i] == 'T':
            y += "Stent"
        elif x[i] == 'C':
            y += "CKD"
        elif x[i] == 'B':
            y += "Bypass"
        elif x[i] == 'm':
            y += "(On medication), "
        elif x[i] == 'c':
            y += "(Controlled), "
        else:
            y += ""
    y = y[:-2]

    pers = database.child("Personal_Details").child(id).get()
    info1 = [x.val() for x in pers.each()]
    #print(info1)
    med = database.child("Medical_Details").child(id).get()
    info2 = [x.val() for x in med.each()]

    dtfromform = info1[1]
    formatteddate = dtfromform[:10]
    date_1 = datetime.datetime.strptime(formatteddate, '%Y-%m-%d')
    end_date = date_1 + datetime.timedelta(days=1)
    finaldate = str(end_date)
    finaldate = finaldate[0:10]

    try:
        data_in_database = database.child("Var_Med_Details").child(id).child("others").child("1").get()
        print(data_in_database.each)
        print("x")


        item = data_in_database
        try:
            if (item.val()['HRCT'] != ""):
                info2[9] = item.val()['HRCT']
        except:
            print("nohrct")
        try:
            if (item.val()['CRP'] != ""):
                info2[-7] = item.val()['CRP']
        except:
            print("nocrp")
        try:
            if (item.val()['others'] != ""):
                info2[-6] = item.val()['others']
        except:
            print("noothers")

        # updated_meds=database.child('Var_Med_Details').child(id).child("others").child("1").get()
        # info4 = [x.val() for x in updated_meds.each()]
        # if (info4):
        #     info2[9]=info4[1]
        #     info2[-7]=info4[0]
        #     info2[-6]=info4[4]
        new_symptoms=""
        ddimer=""
        try:
            if item.val()['newsymp']!="":
                new_symptoms = item.val()['newsymp']
        except:
            print("nonewsymptoms")
        try:
            if item.val()['ddimer']:
               ddimer = item.val()['ddimer']
        except:
            print("noddimer")



    except:
        new_symptoms="_"
        ddimer="_"
        print("hiiiiii")

    d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14 = "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_"

    try:
        d1 = info2[3]
        spo2 = database.child("Var_Med_Details").child(id).child("SpO2").child("1").get()
        spo2_rec = spo2
        try:
            if (spo2.val()['d2'] != "" or spo2.val()['d3'] != "" or spo2.val()['d4'] != "" or spo2.val()['d5'] != ""):
                d1 = spo2.val()['d1']
                d2 = spo2.val()['d2']
                d3 = spo2.val()['d3']
                d4 = spo2.val()['d4']
                d5 = spo2.val()['d5']
                d6 = spo2.val()['d6']
                d7 = spo2.val()['d7']
                d8 = spo2.val()['d8']
                d9 = spo2.val()['d9']
                d10 = spo2.val()['d10']
                d11 = spo2.val()['d11']
                d12 = spo2.val()['d12']
                d13 = spo2.val()['d13']
                d14 = spo2.val()['d14']




        except:
            print("nospo2")



    except:
        print("hii2")
        d2 = "-"
        d3 = "-"
        d4 = "-"
        d5 = "-"
        d6 = "-"
        d7 = "-"
        d8 = "-"
        d9 = "-"
        d10 = "-"
        d11 = "-"
        d12 = "-"
        d13 = "-"
        d14 = "-"
    try:
        No_of_pres = list(database.child("prescription").child(id).shallow().get().val())
        num = len(No_of_pres)

        combilis = []
        for i in range(num, 0, -1):
            prescription = "PRESCRIPTION " + str(i)
            pres = list(database.child("prescription").child(id).child(prescription).get().val().items())
            medicine = (pres[0][1]).split(",")
            mg = (pres[1][1]).split(",")
            notes = (pres[2][1]).split(",")
            time = (pres[3][1]).split(",")
            combi = zip(medicine, mg, time, notes)
            combilis.append(combi)

        prescnum = list(range(len(combilis), 0, -1))

        print(prescnum)
        combilis = zip(combilis, prescnum)
    except:
        print("hoo")
        patient_data = {
            "Name": info1[6],
            "ID": id,
            "Age": info1[0],
            "Mobile": info1[5],
            "Email": info1[2],
            "Location": info1[4],
            "Sex": info1[7],
            "Date": finaldate,

            "Fileno": info1[-1],

            "RTPCR": info2[-5],
            "CT": info2[-4],
            "Past": y,
            "Symptoms": info2[-3],
            "Firstsymp": info2[5],
            "Currspo2": info2[3],
            "Vacstat": info2[2],
            "1stvac": info2[6],
            "2ndvac": info2[8],
            "vaccomp": info2[0],
            "hrct": info2[9],
            "CRP": info2[-7],
            "multiple_vals": info2[-6],
            "curr_treatent": info2[4],
            "date_presc": info2[7],
            "Other_recent_investigation": info2[1],
            "Treatment_prescribed_while_filling_form": info2[-1],
            "newsymp": new_symptoms,
            "ddimer": ddimer,
            "day1": info2[3],
            "day2": d2,
            "day3": d3,
            "day4": d4,
            "day5": d5,
            "day6": d6,
            "day7": d7,
            "day8": d8,
            "day9": d9,
            "day10": d10,
            "day11": d11,
            "day12": d12,
            "day13": d13,
            "day14": d14,



        }

        return render(request, "patientdetails.html", patient_data)
    patient_data = {
        "Name": info1[6],
        "ID": id,
        "Age": info1[0],
        "Mobile": info1[5],
        "Email": info1[2],
        "Location": info1[4],
        "Sex": info1[7],
        "Date": finaldate,

        "Fileno": info1[-1],

        "RTPCR": info2[-5],
        "CT": info2[-4],
        "Past": y,
        "Symptoms": info2[-3],
        "Firstsymp": info2[5],
        "Currspo2": info2[3],
        "Vacstat": info2[2],
        "1stvac": info2[6],
        "2ndvac": info2[8],
        "vaccomp": info2[0],
        "hrct": info2[9],
        "CRP": info2[-7],
        "multiple_vals": info2[-6],
        "curr_treatent": info2[4],
        "date_presc": info2[7],
        "Other_recent_investigation": info2[1],
        "Treatment_prescribed_while_filling_form": info2[-1],
        "newsymp": new_symptoms,
        "ddimer": ddimer,
        "day1": info2[3],
        "day2": d2,
        "day3": d3,
        "day4": d4,
        "day5": d5,
        "day6": d6,
        "day7": d7,
        "day8": d8,
        "day9": d9,
        "day10": d10,
        "day11": d11,
        "day12": d12,
        "day13": d13,
        "day14": d14,
        "combilis":combilis

    }


    return render(request, "patientdetails.html", patient_data)

def O2update(request):
    print("hello")
    id = request.POST.get("pat_id")

    day1=request.POST.get("Day_1")
    print("this is from hidden" + day1)
    day2,day3,day4,day5=".",".",".","."

    if request.POST.get("day2")!=None:
        day2=request.POST.get("day2")
        print("d",day2)
    else:
        day2=request.POST.get("Day_2")
        print("D"+day2)

    if request.POST.get("day3")!=None:
        day3=request.POST.get("day3")
    else :
        day3=request.POST.get("Day_3")

    if request.POST.get("day4")!=None:
        day4=request.POST.get("day4")
    else :
        day4=request.POST.get("Day_4")

    if request.POST.get("day5")!=None:
        day5=request.POST.get("day5")
    else:
        day5=request.POST.get("Day_5")

    if request.POST.get("day6")!=None:
        day6=request.POST.get("day6")
    else:
        day6=request.POST.get("Day_6")

    if request.POST.get("day7")!=None:
        day7=request.POST.get("day7")
    else:
        day7=request.POST.get("Day_7")

    if request.POST.get("day8")!=None:
        day8=request.POST.get("day8")
    else:
        day8=request.POST.get("Day_8")

    if request.POST.get("day9")!=None:
        day9=request.POST.get("day9")
    else:
        day9=request.POST.get("Day_9")

    if request.POST.get("day10")!=None:
        day10=request.POST.get("day10")
    else:
        day10=request.POST.get("Day_10")

    if request.POST.get("day11")!=None:
        day11=request.POST.get("day11")
    else:
        day11=request.POST.get("Day_11")

    if request.POST.get("day12")!=None:
        day12=request.POST.get("day12")
    else:
        day12=request.POST.get("Day_12")

    if request.POST.get("day13")!=None:
        day13=request.POST.get("day13")
    else:
        day13=request.POST.get("Day_13")

    if request.POST.get("day14")!=None:
        day14=request.POST.get("day14")
    else:
        day14=request.POST.get("Day_14")


    Oxy_data = {
        "d1":day1,
        "d2":day2,
        "d3": day3,
        "d4": day4,
        "d5": day5,
        "d6": day6,
        "d7": day7,
        "d8": day8,
        "d9": day9,
        "d10": day10,
        "d11": day11,
        "d12": day12,
        "d13": day13,
        "d14": day14
    }


    database.child("Var_Med_Details").child(id).child("SpO2").child("1").set(Oxy_data)

    x = str(id)
    i = 0
    y = ""
    for i in range(0, len(x)):
        if x[i] == 'D':
            y = "Diabetes"
        elif x[i] == 'S':
            y += "Heart Disease/Stroke"
        elif x[i] == 'O':
            y += "Obesity"
        elif x[i] == 'L':
            y += "Liver Disease"
        elif x[i] == 'T':
            y += "Stent"
        elif x[i] == 'C':
            y += "CKD"
        elif x[i] == 'B':
            y += "Bypass"
        elif x[i] == 'm':
            y += "(On medication), "
        elif x[i] == 'c':
            y += "(Controlled), "
        else:
            y += ""
    y = y[:-2]

    pers = database.child("Personal_Details").child(id).get()
    info1 = [x.val() for x in pers.each()]
    # print(info1)
    med = database.child("Medical_Details").child(id).get()
    info2 = [x.val() for x in med.each()]

    dtfromform = info1[1]
    formatteddate = dtfromform[:10]
    date_1 = datetime.datetime.strptime(formatteddate, '%Y-%m-%d')
    end_date = date_1 + datetime.timedelta(days=1)
    finaldate = str(end_date)
    finaldate = finaldate[0:10]


    try:
        data_in_database = database.child("Var_Med_Details").child(id).child("others").child("1").get()
        print(data_in_database.each)
        print("x")

        item = data_in_database
        try:
            if (item.val()['HRCT'] != ""):
                info2[9] = item.val()['HRCT']
        except:
            print("nohrct")
        try:
            if (item.val()['CRP'] != ""):
                info2[-7] = item.val()['CRP']
        except:
            print("nocrp")
        try:
            if (item.val()['others'] != ""):
                info2[-6] = item.val()['others']
        except:
            print("noothers")

        # updated_meds=database.child('Var_Med_Details').child(id).child("others").child("1").get()
        # info4 = [x.val() for x in updated_meds.each()]
        # if (info4):
        #     info2[9]=info4[1]
        #     info2[-7]=info4[0]
        #     info2[-6]=info4[4]
        new_symptoms = ""
        ddimer = ""
        try:
            if item.val()['newsymp'] != "":
                new_symptoms = item.val()['newsymp']
        except:
            print("nonewsymptoms")
        try:
            if item.val()['ddimer']:
                ddimer = item.val()['ddimer']
        except:
            print("noddimer")



    except:
        new_symptoms = "_"
        ddimer = "_"
        print("hiiiiii")

    d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14 = "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_"

    try:
        d1=day1
        spo2 = database.child("Var_Med_Details").child(id).child("SpO2").child("1").get()
        spo2_rec = spo2
        try:
            if(spo2.val()['d2']!="" or spo2.val()['d3']!="" or spo2.val()['d4']!="" or spo2.val()['d5']!=""):
                d1= spo2.val()['d1']
                d2 = spo2.val()['d2']
                d3 = spo2.val()['d3']
                d4 = spo2.val()['d4']
                d5 = spo2.val()['d5']
                d6 = spo2.val()['d6']
                d7 = spo2.val()['d7']
                d8 = spo2.val()['d8']
                d9 = spo2.val()['d9']
                d10 = spo2.val()['d10']
                d11= spo2.val()['d11']
                d12 = spo2.val()['d12']
                d13 = spo2.val()['d13']
                d14 = spo2.val()['d14']




        except:
            print("nospo2")



    except:
        print("hii2")
        d2 = "-"
        d3 = "-"
        d4 = "-"
        d5 = "-"
        d6 = "-"
        d7 = "-"
        d8 = "-"
        d9 = "-"
        d10 = "-"
        d11 = "-"
        d12 = "-"
        d13 = "-"
        d14 = "-"

    patient_data = {
        "Name": info1[6],
        "ID": id,
        "Age": info1[0],
        "Mobile": info1[5],
        "Email": info1[2],
        "Location": info1[4],
        "Sex": info1[7],
        "Date": finaldate,

        "Fileno": info1[-1],

        "RTPCR": info2[-5],
        "CT": info2[-4],
        "Past": y,
        "Symptoms": info2[-3],
        "Firstsymp": info2[5],
        "Currspo2": info2[3],
        "Vacstat": info2[2],
        "1stvac": info2[6],
        "2ndvac": info2[8],
        "vaccomp": info2[0],
        "hrct": info2[9],
        "CRP": info2[-7],
        "multiple_vals": info2[-6],
        "curr_treatent": info2[4],
        "date_presc": info2[7],
        "Other_recent_investigation": info2[1],
        "Treatment_prescribed_while_filling_form": info2[-1],
        "newsymp": new_symptoms,
        "ddimer": ddimer,
        "day1":day1,
        "day2": d2,
        "day3": d3,
        "day4": d4,
        "day5": d5,
        "day6": d6,
        "day7": d7,
        "day8": d8,
        "day9": d9,
        "day10": d10,
        "day11": d11,
        "day12": d12,
        "day13": d13,
        "day14": d14

    }



    return render(request,"patientdetails.html",patient_data)


def movepatient(request):
    uid = request.POST.get("patient_id")
    indexnum = uid.index("  ")
    num = indexnum
    id = uid[:num]
    num = indexnum + 2
    name = uid[num:]



    doctor2 = request.POST.get("doctor2")
    data = {"id": id,"name":name}
    print(data)
    print(doctor2)
    shift = database.child("SecondaryDoctor").child(doctor2).child(id).set(data)
    names, ids = [], []
    name_id = database.child("Doctor").get()
    info = [x.val() for x in name_id.each()]
    print(info)
    for i in info:
        for x in i.values():
            names.append(x['Name'])
            ids.append(x['ID'])

    a = database.child("Doctor_Data").get()
    # print(a)
    drname = ""
    info2 = [x.val() for x in a.each()]
    print(info2)
    drs = []
    for y in info2:
        print(y['Name'])
        drs.append(y['Name'])
        print("1")

    print(names, ids)
    combilist = zip(names, ids)
    combi2 = zip(names, ids)
    print("123")
    combi3 = zip(names, ids)
    print("horsestyle")
    return render(request, "adminpatientname.html",
                  {"combi": combilist, "combi2": combi2, "combi3": combi3, "drs": drs})


def secondarypatient(request):
    drname=request.session.get("drname")
    doctors = database.child("SecondaryDoctor").child(drname).get()
    drs_patient = [d.val() for d in doctors.each()]
    print(drs_patient)
    name,id=[],[]
    for x in drs_patient:
        print(x)
        name.append(x['name'])
        id.append(x['id'])

    print(name, id)

    combi = zip(name, id)
    return render(request, "patientsname.html", {"data": combi,"flag":"1"})


def deletesecondary(request):
    drname = request.session.get("drname")

    id = request.POST.get("id")
    database.child("SecondaryDoctor").child(drname).child(id).remove()
    try:
        doctors = database.child("SecondaryDoctor").child(drname).get()
        drs_patient = [d.val() for d in doctors.each()]
        print(drs_patient)
        name, id = [], []
        for x in drs_patient:
            print(x)
            name.append(x['name'])
            id.append(x['id'])

        print(name, id)

        combi = zip(name, id)
        return render(request, "patientsname.html", {"data": combi, "flag": "1"})
    except:
        return render(request, "patientsname.html")


def dischargepatient(request):
    uid = request.POST.get("patid")
    #uid = "OcSmDc11  Ruchit Thaker"
    print(uid)
    indexnum = uid.index("  ")
    num = indexnum
    id = uid[:num]
    num = indexnum + 2
    name = uid[num:]

    #======================================================================================




    i = 0
    y = ""
    x=id
    for i in range(0, len(x)):
        if x[i] == 'D':
            y = "Diabetes"
        elif x[i] == 'S':
            y += "Heart Disease/Stroke"
        elif x[i] == 'O':
            y += "Obesity"
        elif x[i] == 'L':
            y += "Liver Disease"
        elif x[i] == 'T':
            y += "Stent"
        elif x[i] == 'C':
            y += "CKD"
        elif x[i] == 'B':
            y += "Bypass"
        elif x[i] == 'm':
            y += "(On medication), "
        elif x[i] == 'c':
            y += "(Controlled), "
        else:
            y += ""
    y = y[:-2]

    pers = database.child("Personal_Details").child(id).get()
    info1 = [t.val() for t in pers.each()]
    # print(info1)
    med = database.child("Medical_Details").child(id).get()
    info2 = [x.val() for x in med.each()]

    dtfromform = info1[1]
    formatteddate = dtfromform[:10]
    date_1 = datetime.datetime.strptime(formatteddate, '%Y-%m-%d')
    end_date = date_1 + datetime.timedelta(days=1)
    finaldate = str(end_date)
    finaldate = finaldate[0:10]

    # firstsymptomdate = info2[5]
    # formatteddate2 = firstsymptomdate[:10]
    # date_2 = datetime.datetime.strptime(formatteddate2, '%Y-%m-%d')
    # end_date2 = date_2 + datetime.timedelta(days=1)
    # finaldate2 = str(end_date2)
    # finaldate2 = finaldate2[0:10]
    #
    # firststshot = info2[6]
    # formatteddate = dtfromform[:10]
    # date_1 = datetime.datetime.strptime(formatteddate, '%Y-%m-%d')
    # end_date = date_1 + datetime.timedelta(days=1)
    # finaldate = str(end_date)
    # finaldate = finaldate[0:10]
    #
    # dtfromform = info2[8]
    # formatteddate = dtfromform[:10]
    # date_1 = datetime.datetime.strptime(formatteddate, '%Y-%m-%d')
    # end_date = date_1 + datetime.timedelta(days=1)
    # finaldate = str(end_date)
    # finaldate = finaldate[0:10]

    try:
        data_in_database = database.child("Var_Med_Details").child(id).child("others").child("1").get()
        print(data_in_database.each)
        print("x")
        item = data_in_database

        item = data_in_database
        try:
            if (item.val()['HRCT'] != ""):
                info2[9] = item.val()['HRCT']
        except:
            print("nohrct")
        try:
            if (item.val()['CRP'] != ""):
                info2[-7] = item.val()['CRP']
        except:
            print("nocrp")
        try:
            if (item.val()['others'] != ""):
                info2[-6] = item.val()['others']
        except:
            print("noothers")

        # updated_meds=database.child('Var_Med_Details').child(id).child("others").child("1").get()
        # info4 = [x.val() for x in updated_meds.each()]
        # if (info4):
        #     info2[9]=info4[1]
        #     info2[-7]=info4[0]
        #     info2[-6]=info4[4]
        new_symptoms = ""
        ddimer = ""
        try:
            if item.val()['newsymp'] != "":
                new_symptoms = item.val()['newsymp']
        except:
            print("nonewsymptoms")
        try:
            if item.val()['ddimer']:
                ddimer = item.val()['ddimer']
        except:
            print("noddimer")



    except:
        new_symptoms = "_"
        ddimer = "_"
        print("hii")
    d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14 = "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_"

    try:
        d1 = info2[3]
        spo2 = database.child("Var_Med_Details").child(id).child("SpO2").child("1").get()
        spo2_rec = spo2
        try:
            if (spo2.val()['d2'] != "" or spo2.val()['d3'] != "" or spo2.val()['d4'] != "" or spo2.val()['d5'] != ""):
                d1 = spo2.val()['d1']
                d2 = spo2.val()['d2']
                d3 = spo2.val()['d3']
                d4 = spo2.val()['d4']
                d5 = spo2.val()['d5']
                d6 = spo2.val()['d6']
                d7 = spo2.val()['d7']
                d8 = spo2.val()['d8']
                d9 = spo2.val()['d9']
                d10 = spo2.val()['d10']
                d11 = spo2.val()['d11']
                d12 = spo2.val()['d12']
                d13 = spo2.val()['d13']
                d14 = spo2.val()['d14']




        except:
            print("nospo2")



    except:
        print("hii2")
        d2 = "-"
        d3 = "-"
        d4 = "-"
        d5 = "-"
        d6 = "-"
        d7 = "-"
        d8 = "-"
        d9 = "-"
        d10 = "-"
        d11 = "-"
        d12 = "-"
        d13 = "-"
        d14 = "-"
    combilis = []
    try:
        No_of_pres = list(database.child("prescription").child(id).shallow().get().val())
        num = len(No_of_pres)


        for i in range(num, 0, -1):
            prescription = "PRESCRIPTION " + str(i)
            pres = list(database.child("prescription").child(id).child(prescription).get().val().items())
            medicine = (pres[0][1]).split(",")
            mg = (pres[1][1]).split(",")
            notes = (pres[2][1]).split(",")
            time = (pres[3][1]).split(",")
            combi = zip(medicine, mg, time, notes)
            combilis.append(combi)

        prescnum = list(range(len(combilis), 0, -1))

        print(prescnum)
        combilis = zip(combilis, prescnum)
    except:
        print("hoo")
        patient_data = {
            "Name": info1[6],
            "ID": id,
            "Age": info1[0],
            "Mobile": info1[5],
            "Email": info1[2],
            "Location": info1[4],
            "Sex": info1[7],
            "Date": finaldate,

            "Fileno": info1[-1],

            "RTPCR": info2[-5],
            "CT": info2[-4],
            "Past": y,
            "Symptoms": info2[-3],
            "Firstsymp": info2[5],
            "Currspo2": info2[3],
            "Vacstat": info2[2],
            "1stvac": info2[6],
            "2ndvac": info2[8],
            "vaccomp": info2[0],
            "hrct": info2[9],
            "CRP": info2[-7],
            "multiple_vals": info2[-6],
            "curr_treatent": info2[4],
            "date_presc": info2[7],
            "Other_recent_investigation": info2[1],
            "Treatment_prescribed_while_filling_form": info2[-1],
            "newsymp": new_symptoms,
            "ddimer": ddimer,
            "day1": info2[3],
            "day2": d2,
            "day3": d3,
            "day4": d4,
            "day5": d5,
            "day6": d6,
            "day7": d7,
            "day8": d8,
            "day9": d9,
            "day10": d10,
            "day11": d11,
            "day12": d12,
            "day13": d13,
            "day14": d14

        }


    patient_data = {
        "Name": info1[6],
        "ID": id,
        "Age": info1[0],
        "Mobile": info1[5],
        "Email": info1[2],
        "Location": info1[4],
        "Sex": info1[7],
        "Date": finaldate,

        "Fileno": info1[-1],

        "RTPCR": info2[-5],
        "CT": info2[-4],
        "Past": y,
        "Symptoms": info2[-3],
        "Firstsymp": info2[5],
        "Currspo2": info2[3],
        "Vacstat": info2[2],
        "1stvac": info2[6],
        "2ndvac": info2[8],
        "vaccomp": info2[0],
        "hrct": info2[9],
        "CRP": info2[-7],
        "multiple_vals": info2[-6],
        "curr_treatent": info2[4],
        "date_presc": info2[7],
        "Other_recent_investigation": info2[1],
        "Treatment_prescribed_while_filling_form": info2[-1],
        "newsymp": new_symptoms,
        "ddimer": ddimer,
        "day1": info2[3],
        "day2": d2,
        "day3": d3,
        "day4": d4,
        "day5": d5,
        "day6": d6,
        "day7": d7,
        "day8": d8,
        "day9": d9,
        "day10": d10,
        "day11": d11,
        "day12": d12,
        "day13": d13,
        "day14": d14,
        "combilis": combilis

    }



    #========================================================================================


    print(patient_data)
    pdf = render_to_pdf('invoice.html',uid, patient_data)

    to_drive(uid)

    # return HttpResponse(pdf, content_type='application/pdf')

    database.child("Personal_Details").child(id).remove()
    database.child("Medical_Details").child(id).remove()
    try:

        database.child("Var_Med_Details").child(id).remove()

    except:
        print("no data there")
    try:

        database.child("prescription").child(id).remove()
    except:
        print("no data there")
    drname=write_in_sheet(id)

#------------------------------------send final mail------------------------------------------------
    try:
        email=info1[2]
        html_content = "This is a test mail for sent prescription"
        email = EmailMessage("CC-Prescription", html_content,
                             "opdonthegot@gmail.com", [email])
        email.content_subtype = "html"
        email.attach_file('media/'+uid+'.pdf')
        res = email.send()
        print("whatsapp")
    except:
        pass
    database.child("Doctor").child(drname).child(id).remove()
    print("hi")
    names,ids=[],[]
    name_id = database.child("Doctor").get()
    info = [x.val() for x in name_id.each()]
    print(info)
    for i in info:
        for x in i.values():
            names.append(x['Name'])
            ids.append(x['ID'])

    a = database.child("Doctor_Data").get()
    # print(a)
    drname = ""
    info2 = [x.val() for x in a.each()]
    print(info2)
    drs = []
    for y in info2:
        print(y['Name'])
        drs.append(y['Name'])
        print("1")

    print(names, ids)
    combilist = zip(names, ids)
    combi2 = zip(names, ids)
    print("123")
    combi3 = zip(names, ids)
    print("horsestyle")
    delete = default_storage.delete('media/'+uid+'.pdf')
    return render(request, "adminpatientname.html",
                  {"combi": combilist, "combi2": combi2, "combi3": combi3, "drs": drs})

