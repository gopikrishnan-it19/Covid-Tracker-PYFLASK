from flask import Flask,render_template,request
import urllib.request, json
import requests

app = Flask(__name__)

@app.route("/",methods=['POST','GET'])
def getdata():
    # Overall Covid Cases
    url="https://disease.sh/v3/covid-19/all"
    res=requests.get(url)
    jsonsent=res.json()
    # All country count
    country_url="https://disease.sh/v3/covid-19/countries"
    country_res=requests.get(country_url)
    country_json=country_res.json()
    country_list_json=country_json

    casesDict={}
    recoveredDict={}
    deathDict={}

    
    for i in country_json:
        casesDict[i["country"]]=i["cases"]
        recoveredDict[i["country"]]=i["recovered"]
        deathDict[i["country"]]=i["deaths"]
    
    casesDict=dict(sorted(casesDict.items(), key=lambda item: item[1],reverse=True))
    recoveredDict=dict(sorted(recoveredDict.items(), key=lambda item: item[1],reverse=True))
    deathDict=dict(sorted(deathDict.items(), key=lambda item: item[1],reverse=True))


    # Check if it go up or down
    status_url="https://disease.sh/v3/covid-19/historical/all?lastdays=2"
    status_res=requests.get(status_url)
    status_json=status_res.json()
    prevdata=[]
    for i,j in status_json.items():
        for k in j:
            prevdata.append(j[k])
    caseinStatus=0
    deathinStatus=0
    recovinstatus=0
    if(prevdata[0] < prevdata[1]):
        caseinStatus=1    
    if(prevdata[2] < prevdata[3]):
        deathinStatus=1
    if(prevdata[4] < prevdata[5]):
        recovinstatus=1



    # Select Country
    filterStatus=0
    country_json_specific=''
    display_country='Select Country'
    if(request.method=="POST"):
        filterStatus=1
        countryCode = request.form['countrySelect']
        country_url_format=f'https://disease.sh/v3/covid-19/countries/{countryCode}'
        country_res_specific=requests.get(country_url_format)
        country_json_specific=country_res_specific.json()
        display_country=country_json_specific["country"]

    # List of country for drop down


    return render_template("home.html",jsonsent=jsonsent,country_json=country_json,caseinStatus=caseinStatus,deathinStatus=deathinStatus,recovinstatus=recovinstatus,country_json_specific=country_json_specific,filterStatus=filterStatus,country_list_json=country_list_json,display_country=display_country,recoveredDict=recoveredDict,deathDict=deathDict,casesDict=casesDict)                                                                                        
    


if(__name__=="__main__"):
    app.run(debug=True)