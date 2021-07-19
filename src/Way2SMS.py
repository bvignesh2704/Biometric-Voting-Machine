import requests


# SMS CLASS
class SMS:
    # all parameters are strings
    def __init__(self, apikey, secretkey, usetype='stage', senderid="random"):
        self.URL = 'https://www.sms4india.com/api/v1/sendCampaign'
        self.req_params = {
            "apikey": apikey,
            "secret": secretkey,
            "usetype": usetype,
            "senderid": senderid
        }

    # all parameters are strings
    def sendMessage(self, phonenumber, message):
        self.req_params["phone"] = phonenumber
        self.req_params["message"] = message

        return requests.post(self.URL, self.req_params)
