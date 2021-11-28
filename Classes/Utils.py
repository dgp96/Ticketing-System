import requests
import ujson

class Utils:


    def mapIds(self,userData):
        userNames = {}

        for i in range(len(userData)):
            userNames[str(userData[i]['id'])] = str(userData[i]['name'])

        return userNames

    def getIds(self,tickets,id):
        user_ids = set()
        for i in range(len(tickets)):
            user_ids.add(str(tickets[i][id]))

        return user_ids

    def modifyTicket(self,tickets,data,keys,fields):
        for i in range(len(tickets)):
            for j in range(len(keys)):
                id = str(tickets[i][keys[j]])
                tickets[i][fields[j] + "_name"] = data[id]
        return tickets
