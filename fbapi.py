#!/usr/bin/python
# -*- coding: utf-8 -*-



#
#   Copyright 2020 Cristhian Willrich Bilhalva
#
#   This file is part of python-facebook-api.
#
#   python - facebook - api is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   python - facebook - api is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with python-facebook-api.  If not, see <https://www.gnu.org/licenses/>
#


#version 1.0.0


import urllib
import urllib2
import json
import hmac
import hashlib
from poster.encode import multipart_encode
from poster.encode import MultipartParam
from poster.streaminghttp import register_openers
from objdict import objdict


class FbAPI(object):
    def __init__(self,appid, appsecret, token = None):
        self.token = token
        self.secret = appsecret
        self.appid = appid
        self.apiver = 'v2.12'


    def get_acess_token(self,caller_url, code):
        cformat = code.find('#')
        if cformat != -1:
            code = code[:cformat]
        caller_url = urllib.quote_plus(caller_url)
        req_url = 'https://graph.facebook.com/'+self.apiver+'/oauth/access_token?client_id=%s&redirect_uri=%s&client_secret=%s&code=%s' % (self.appid,caller_url, self.secret,code)
        f = None
        try:
            f = urllib2.urlopen(req_url)
        except urllib2.HTTPError as e:
            print str(e)
            print 'request URL:', req_url
            if f:
                print 'Response:', f.read()
            return None
        tk_str = f.read()
        token = json.loads(tk_str)
        token = token.get('access_token')
        self.token = token


    def query(self,endpoint,parameters = {},method = 'GET',postdata='',mimetype=None):
        parameters['access_token'] = self.token
        parameters['appsecret_proof'] = hmac.new(self.secret, self.token, hashlib.sha256).hexdigest()

#       print parameters
        f = None
        resstr = None

        datagen = ''
        headers={}

        if method == 'POST' and postdata is not '':
            register_openers()
            mp_param = MultipartParam('source',value=postdata,filename='upload.png',filetype=mimetype)
            datagen, headers = multipart_encode([mp_param])

        try:
            data = urllib.urlencode(parameters)
            url = 'https://graph.facebook.com/'+self.apiver+'/'+endpoint+'?' + data
            #print url
            if method == 'POST':
                req = urllib2.Request(url,datagen,headers)
            else:
                req = urllib2.Request(url)

            f = urllib2.urlopen(req)
        except urllib2.HTTPError as e:
            print dir(e)
            #print e.message
            print parameters
            return json.loads(e.read(),object_pairs_hook=objdict)

        if f != None:
            resstr = f.read()
            return json.loads(resstr,object_pairs_hook=objdict)


