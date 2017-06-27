#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "order_phone":
        return {}
    
    result = req.get("result")
    parameters = result.get("parameters")
    OS = parameters.get("OS")
    if OS is None:
        return {}
    
    res = makeWebhookResult(OS)
    return res
     
    



def makeWebhookResult(OS):
    #speech = " OS = " + OS
    with open("tyy-4io.txt","r") as ins:
        for line in ins:
            if OS in line:
                 matched_line=line
                 break
    columns = matched_line.split('\t')
    title = columns[0]
    price = columns[4]
    productUrl = columns[5]
    
    speech="Here is a phone that suits your needs " + title + "\nPriced at Rs." + price + ".\nMore details at  " + productUrl 
    #speech = title + price + productUrl
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "Jeena-John/apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
