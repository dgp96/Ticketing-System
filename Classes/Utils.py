import requests
import ujson
import datetime

class Utils:

    def modifyDate(self,date): #returns datetime without timezone
        newDate = datetime.datetime.strptime(date,"%Y-%m-%dT%H:%M:%SZ")
        return str(newDate)

    def modifyTags(self,tags): #returns tags a single string of comma separated tags
        return ",".join(tags)

    def mapIds(self,userData): #maps ids to names
        userNames = {}

        for i in range(len(userData)):
            userNames[str(userData[i]['id'])] = str(userData[i]['name'])

        return userNames

    def getIds(self,tickets,id): #returns unique set of ids
        user_ids = set()
        for i in range(len(tickets)):
            user_ids.add(str(tickets[i][id]))

        return user_ids

    def modifyTicket(self,tickets,data,keys,fields): #adds new keys to the tickets json 
        for i in range(len(tickets)):
            for j in range(len(keys)):
                id = str(tickets[i][keys[j]])
                tickets[i][fields[j] + "_name"] = data[id]
        return tickets
