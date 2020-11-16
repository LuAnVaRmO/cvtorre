#!/usr/bin/env python3
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response, render_template
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
        username = creation.username.data
        url = "https://torre.bio/api/bios/{}".format(username)
        response = requests.get(url)
        if response.status_code == 200:
            orgs=[]
            schools=[]
            proheadline = response.json()['person']['professionalHeadline']
            if hasattr(response.json()['person'], 'summaryOfBio'):
                summary = response.json()['person']['summaryOfBio']
            else: 
                summary = "Please complete your Genome"
            name = response.json()['person']['name']
            jobdata = response.json()['jobs']
            educationdata = response.json()['education']
            for i in range(len(jobdata)):
                if [d['organizations'] for d in jobdata][i]:
                    orgs.append([d['organizations'] for d in jobdata][i][0]['name'])
                else:
                    orgs.append('...')
            for i in range(len(educationdata)):
                if [d['organizations'] for d in educationdata][i]:
                    schools.append([d['organizations'] for d in educationdata][i][0]['name'])
                else:
                    schools.append('...')
            location = response.json()['person']['location']['name']
            personaldata=[]
            document = creation.document.data
            address = creation.address.data
            birth = creation.birth.data
            nationality = creation.nation.data
            phone = creation.phone.data
            email = creation.email.data
            # Adding personal information to a list
            personaldata.append(address)
            personaldata.append(birth)
            personaldata.append(nationality)
            personaldata.append(phone)
            personaldata.append(email)
            skills = response.json()['strengths']
            skillsdata = []
            for i in skills:
                value = i['name']
                skillsdata.append(value)
            dictemp = {}
            socialdata = []
            social = response.json()['person']['links']
            for i in social:
                dictemp['name'] = i['name']
                dictemp['address'] = i['address']
                socialdata.append(dictemp.copy())
            picture = response.json()['person']['picture']
        else:
            return make_response(render_template('error.html', error=response.status_code))
        return render_template('layout.html',form=creation,
                                            proheadline=proheadline,
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
    else:
        return render_template('index.html', form=creation)
