import requests
import ujson

class Client:

    _self_instance = None
    host = "https://zccdgp.zendesk.com/"
    headers = {"Authorization":"Basic ZHByYWphcDNAYXN1LmVkdS90b2tlbjpYRURoRXFpZEg1eWFPaFZQckkycEFmTDg4d01QTFlEb2s2YlU1T0Vt"}
    params = {"per_page":25}
    def _init_(self):
        if _self_instance != None:
            raise Exception("Cannot be instantiated from here")
        else:
            Client._self_instance = self

    @staticmethod
    def getInstance():
       if Client._self_instance == None:
           return Client()
       return Client._self_instance

    def getUserNames(self,endpoint):
        response = requests.get(Client.host+endpoint,headers=Client.headers)
        if response.status_code == 200:
            data = ujson.loads(response.text)
            return data["users"]
        #return "Error code: " + str(response.status_code)


    def getTicketResponse(self,endpoint):
        response = requests.get(Client.host+endpoint,headers=Client.headers,params=Client.params)
        if response.status_code == 200:
            data = ujson.loads(response.text)
            return data["tickets"],data["count"]
        #return "Error code: " +response.status_code

    def getPagedTicketResponse(self,endpoint,params):
        response = requests.get(Client.host+endpoint,headers=Client.headers,params=params)
        if response.status_code == 200:
            data = ujson.loads(response.text)
            return data["tickets"],data["count"]
        #return "Error code: " +response.status_code

    def getGroups(self,endpoint):
        response = requests.get(Client.host+endpoint,headers=Client.headers)
        if response.status_code == 200:
            data = ujson.loads(response.text)
            return data["groups"]
        #return "Error code: " + str(response.status_code)

    def getIndividualTicketResponse(self, endpoint):
        response = requests.get(Client.host+endpoint,headers=Client.headers)
        if response.status_code == 200:
            data = ujson.loads(response.text)
            return data["ticket"]
        #return "Error code: " +response.status_code
    # def getCount(self,endpoint):
    #     response = requests.get(Client.host+endpoint,headers=Client.headers)
    #     if response.status_code == 200:
    #         data = ujson.loads(response.text)
    #         return data["count"]["value"]
    #     return "Error code: " + str(response.status_code)
