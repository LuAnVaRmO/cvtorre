#!/usr/bin/env python3
from api.v1.views import app_views
from flask import url_for, jsonify, request, make_response, render_template, redirect
import requests
import forms


@app_views.route('/status', methods=['GET'])
def status():
    """ Return status 200 if ok """
    return jsonify({"status": "OK"})


@app_views.route('/', methods=['GET', 'POST'])
def index():
    """ Initial page """
    creation = forms.CreationForm(request.form)
    if request.method == 'POST' and creation.validate():
        name = creation.username.data
        personaldata = []
        document = creation.document.data.replace(" ", "%25")
        address = creation.address.data.replace(" ", "%25")
        birth = creation.birth.data.replace("/", "%28")
        nationality = creation.nation.data.replace(" ", "%25")
        phone = creation.phone.data.replace(" ", "%25")
        email = creation.email.data
        # Adding personal information to a list
        personaldata.append(document)
        personaldata.append(address)
        personaldata.append(birth)
        personaldata.append(nationality)
        personaldata.append(phone)
        personaldata.append(email)
        data = str(personaldata)
        return redirect(url_for('app_views.generate_url', name=name, data=data))
    else:  # GET method
        return render_template('index.html', form=creation)


@app_views.route('/cv/<string:name>/<string:data>', methods=['GET'])
def generate_url(name, data):
    data = data.replace("%25", " ")
    data = data.replace("%28", "/")
    data = data.replace("[", "")
    data = data.replace("]", "")
    data = data.replace("'", "")
    newdata = data.split(",")
    document = newdata.pop(0)
    personaldata = newdata.copy()
    username = name
    url = "https://torre.bio/api/bios/{}".format(username)
    response = requests.get(url)
    if response.status_code == 200:
        orgs = []
        schools = []
        proheadline = response.json()['person']['professionalHeadline']
        person = response.json()['person']
        if 'summaryOfBio' in person:
            summary = response.json()['person']['summaryOfBio']
        else:
            summary = "Please complete your Genome"
        name = response.json()['person']['name']
        jobdata = response.json()['jobs']
        educationdata = response.json()['education']
        for i in range(len(jobdata)):
            if [d['organizations'] for d in jobdata][i]:
                orgs.append([d['organizations']
                             for d in jobdata][i][0]['name'])
            else:
                orgs.append('...')
        for i in range(len(educationdata)):
            if [d['organizations'] for d in educationdata][i]:
                schools.append([d['organizations']
                                for d in educationdata][i][0]['name'])
            else:
                schools.append('...')
        location = response.json()['person']['location']['name']

        # Saving skills in a list
        skills = response.json()['strengths']
        skillsdata = []
        for i in skills:
            value = i['name']
            skillsdata.append(value)
        # Saving social media information
        dictemp = {}
        socialdata = []
        social = response.json()['person']['links']
        for i in social:
            dictemp['name'] = i['name']
            dictemp['address'] = i['address']
            socialdata.append(dictemp.copy())
        # Saving pic
        picture = response.json()['person']['picture']
    else:
        return make_response(render_template('error.html', error=response.status_code))
    return render_template('layout.html', proheadline=proheadline,
                           summary=summary,
                           jobdata=jobdata,
                           orgs=orgs,
                           name=name,
                           educationdata=educationdata,
                           schools=schools,
                           location=location,
                           document=document,
                           personaldata=personaldata,
                           skillsdata=skillsdata,
                           socialdata=socialdata,
                           picture=picture)
