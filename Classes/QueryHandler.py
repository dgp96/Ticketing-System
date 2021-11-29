from Classes.Client import Client as Client
from Classes.Utils import Utils as Utils
class QueryHandler:

    def getTicketResponse(self,endpoint):
        queryHandler = Client.getInstance()
        return queryHandler.getTicketResponse(endpoint)

    def getUserIds(self,tickets,id):
        queryHandler = Utils()
        return queryHandler.getIds(tickets,id)

    def getUserData(self,endpoint):
        queryHandler = Client.getInstance()
        return queryHandler.getUserNames(endpoint)

    def getMapping(self,userData):
        queryHandler = Utils()
        return queryHandler.mapIds(userData)

    def getModifiedTickets(self,tickets,data,keys,fields):
        queryHandler = Utils()
        return queryHandler.modifyTicket(tickets,data,keys,fields)

    def getGroups(self,endpoint):
        queryHandler = Client.getInstance()
        return queryHandler.getGroups(endpoint)

    def getPagedTicketResponse(self,endpoint,params):
        queryHandler = Client.getInstance()
        return queryHandler.getPagedTicketResponse(endpoint,params)

    def getIndividualTicketResponse(self, endpoint):
        queryHandler = Client.getInstance()
        return queryHandler.getIndividualTicketResponse(endpoint)

    def getModifiedDate(self, date):
        queryHandler = Utils()
        return queryHandler.modifyDate(date)

    def getModifiedTags(self,tags):
        queryHandler = Utils()
        return queryHandler.modifyTags(tags)
    # def getCount(self,endpoint):
    #     queryHandler = Client.getInstance()
    #     return queryHandler.getCount(endpoint)
