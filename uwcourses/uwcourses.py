# A simple flask web app for browsing University of Waterloo # courses.
# Provides the terms in which a course is offered, it's prerequisites,
#    terms in which prerequisite is offered and the prerequisites of the
#    prerequisites. Gives a link to the lecturer's uwflow page.


from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap
import json, requests

app = Flask(__name__)

key = '' # Get api key from https://uwaterloo.ca/api/

@app.route("/")
def hello(name=None):
    return render_template('index.html', name=name)


@app.route("/c/<crse>")
def expandurls(crse=None):
    sub = crse.rstrip('0123456789')
    num = crse[len(sub):]
    return redirect('/course/%s/%s' % (sub, num), code=302)


@app.route('/course/<subject>/<number>/')
def getcourse(subject, number):
    def offrd(crse):
        try:
            sub = crse.rstrip('0123456789')
            num = crse[len(sub):]
            odat = requests.get("https://api.uwaterloo.ca/v2/courses/%s/%s.json?key=%s" % (sub, num, key)).json()
            return odat['data']['terms_offered']
        except:
            return []
    moredat = requests.get("https://api.uwaterloo.ca/v2/courses/%s/%s/schedule.json?key=%s" % (subject, number, key)).json()
    
    def getclss(clss):
        try:
            enrl = moredat['data'][clss]['enrollment_total']
            enrlcap = moredat['data'][clss]['enrollment_capacity']
            instruct = moredat['data'][clss]['classes'][0]['instructors']
        except:
            enrl=''
            enrlcap=''
            instruct = ''
        return [clss, enrl, enrlcap, instruct]

    def getrat(stng):
        name = stng.split(',')
        nm = name[1].split(' ')
        na = "https://uwflow.com/professor/"+nm[0].lower()+"_"+name[0].lower()
        return na

    
    def getreqs(crse):
        sub = crse.rstrip('0123456789')
        num = crse[len(sub):]
        try:
            reqd = requests.get("https://api.uwaterloo.ca/v2/courses/%s/%s/prerequisites.json?key=%s" % (sub, num, key)).json()
            preqs = reqd['data']['prerequisites_parsed']
            if(preqs[0] == 1):
                preqs[0]="One of"
            for i in preqs:
                if(i[0] == 1):
                    i[0]="One of"
        except:
            preqs=[]
        return preqs

    try:
        try:
            reqd = requests.get("https://api.uwaterloo.ca/v2/courses/%s/%s/prerequisites.json?key=%s" % (subject, number, key)).json()
            preqs = reqd['data']['prerequisites_parsed']
        except:
            preqs=[]
        data = requests.get("https://api.uwaterloo.ca/v2/courses/%s/%s.json?key=%s" % (subject, number, key)).json()
        title = data['data']['title']
        desc = data['data']['description']
        subject = data['data']['subject']
        coreqs = data['data']['corequisites']
        cross = data['data']['crosslistings']
        off = data['data']['terms_offered']
    except:
        title='no idea'
        desc='no idea'
        coreqs=[]
        cross=''
        off=''
    return render_template('course.html', subject=subject, number=number, title=title, preqs=preqs, desc=desc, coreqs=coreqs, cross=cross, offerd=(lambda x: offrd(x)) ,off=off, getclass=(lambda x: getclss(x)), getrat=(lambda x: getrat(x)), getreqs=(lambda x: getreqs(x)))

if __name__ == "__main__":
    app.run()
