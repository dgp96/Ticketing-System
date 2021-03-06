from flask import Flask,render_template,request
from Classes.Client import Client as Client
from Classes.QueryHandler import QueryHandler as QueryHandler
from Classes.Utils import Utils as Utils
from pathlib import Path
import requests
import ujson
import ast

app = Flask(__name__)

@app.errorhandler(404) # routing for invalid url

# inbuilt function which takes error as parameter

def page_not_found(e):
    return render_template("404.html"), 404




@app.route('/')
def index(): #index page

    endpoint1 = "api/v2/tickets" #endpoint for getting tickets
    endpoint2 = "api/v2/users/show_many.json?ids=" #endpoint for getting userData from user ids
    endpoint3 = "api/v2/groups" #endpoint to get all the groups

    response = True

    queryHandler = QueryHandler()
    try:
        tickets,count = queryHandler.getTicketResponse(endpoint1)
    except:
        response = False
    if response is False or tickets is None  or len(tickets) == 0:
        #return "Error routing the page"
        return render_template("404.html"), 404

    seperator = ","
    userIds = queryHandler.getUserIds(tickets,"requester_id") #returns unique  user ids from the ticket data
    assigneeIds = queryHandler.getUserIds(tickets,"assignee_id")#returns assignee ids from the ticket data

    try:
        userData = queryHandler.getUserData(endpoint2+seperator.join(userIds)+","+seperator.join(assigneeIds)) #returns userData based on passed ids
    except:
        response = False
    if response is False or userData is None:
        #return "Error routing the page"
        return render_template("404.html"), 404

    userMapping = queryHandler.getMapping(userData)
    keys = ["requester_id","assignee_id"]
    fields = ["requester","assignee"]
    tickets = queryHandler.getModifiedTickets(tickets,userMapping,keys,fields) #adds requester and assignee name to the ticket data

    keys = ["group_id"]
    fields = ["group"]

    try:
        groups = queryHandler.getGroups(endpoint3)
    except:
        response = False
    if response is False or groups is None:
        #return "Error routing the page"
        return render_template("404.html"), 404



    groupMapping = queryHandler.getMapping(groups) #maps group ids to group names
    tickets = queryHandler.getModifiedTickets(tickets,groupMapping,keys,fields) # adds group names to ticket data


    pages = int(count/25)
    extra = count%25
    if extra>0:
        pages += 1
    pg_no = 1
    next = "page-item"
    previous =  "page-item"

    if pg_no <= 1:
        previous = "page-item disabled"

    if pg_no >= pages:
        next = "page-item disabled"
    #tickets = queryHandler.getModifiedTickets(tickets,userMapping,"assignee_id","assignee")
    #return render_template('bs4_account_tickets.html')
    # if pg_no is not undefined:
    #     if pg_no > pages or pg_no <= 0:
    #         return "Page doesn't exist"
    # #tickets = queryHandler.getModifiedTickets(tickets,userMapping,"assignee_id","assignee")
    #return render_template('bs4_account_tickets.html')
    page_data = {}
    page_data["pages"] = pages
    page_data["current_page"] = 1
    page_data["previous"] = previous
    page_data["next"] = next
    return render_template("ticket_list.html", len = len(tickets), page_data=page_data, ticket_data = tickets)

@app.route('/page/<int:pg_no>') #routes to different page no in list view
def paginate(pg_no):
    print("Page no: " +str(pg_no))
    if pg_no is None or pg_no<=0:
        return render_template("404.html"), 404



    response = True
    params = {"per_page":25,"page":pg_no}

    endpoint1 = "api/v2/tickets"
    endpoint2 = "api/v2/users/show_many.json?ids="
    endpoint3 = "api/v2/groups"

    queryHandler = QueryHandler()



    try:
        tickets,count = queryHandler.getPagedTicketResponse(endpoint1,params)
    except:
        response = False
    if response is False or tickets is None or len(tickets) == 0:
        #return "Error routing the page"
        return render_template("404.html"), 404

    seperator = ","
    userIds = queryHandler.getUserIds(tickets,"requester_id")
    assigneeIds = queryHandler.getUserIds(tickets,"assignee_id")

    #userData = queryHandler.getUserData(endpoint2+seperator.join(userIds)+","+seperator.join(assigneeIds))
    try:
        userData = queryHandler.getUserData(endpoint2+seperator.join(userIds)+","+seperator.join(assigneeIds))
    except:
        response = False
    if response is False or userData is None:
        #return "Error routing the page"
        return render_template("404.html"), 404



    userMapping = queryHandler.getMapping(userData)
    keys = ["requester_id","assignee_id"]
    fields = ["requester","assignee"]
    tickets = queryHandler.getModifiedTickets(tickets,userMapping,keys,fields)

    keys = ["group_id"]
    fields = ["group"]

    #groups = queryHandler.getGroups(endpoint3)

    try:
        groups = queryHandler.getGroups(endpoint3)
    except:
        response = False
    if response is False or groups is None:
        #return "Error routing the page"
        return render_template("404.html"), 404

    groupMapping = queryHandler.getMapping(groups)
    tickets = queryHandler.getModifiedTickets(tickets,groupMapping,keys,fields)


    next = "page-item"
    previous =  "page-item"
    pages = int(count/25)
    extra = count%25
    if extra>0:
        pages += 1

    if pg_no <= 1:
        previous = "page-item disabled"

    if pg_no >= pages:
        next = "page-item disabled"

    # if pg_no > pages or pg_no <= 0:
    #     return "Page doesn't exist"
    #tickets = queryHandler.getModifiedTickets(tickets,userMapping,"assignee_id","assignee")
    #return render_template('bs4_account_tickets.html')
    page_data = {}
    page_data["pages"] = pages
    page_data["current_page"] = pg_no
    page_data["previous"] = previous
    page_data["next"] = next

    return render_template("ticket_list.html", len = len(tickets), page_data=page_data, ticket_data = tickets)
    #return "You're requesting page# " + pg_no

@app.route('/ticket/<int:ticket_id>') #reoutes to different tickets in ticket details view
def showTicketInfo(ticket_id):

    endpoint1 = "api/v2/tickets/" +str(ticket_id)
    endpoint2 = "api/v2/users/show_many.json?ids="
    endpoint3 = "api/v2/groups"
    response = True
    queryHandler = QueryHandler()

    #ticket = queryHandler.getIndividualTicketResponse(endpoint1)
    try:
        ticket = queryHandler.getIndividualTicketResponse(endpoint1)
    except:
        response = False
    if response is False or ticket is None or len(ticket) == 0:
        #return "Error routing the page"
        return render_template("404.html"), 404

    ticket["created_at"] = queryHandler.getModifiedDate(ticket["created_at"])
    ticket["updated_at"] = queryHandler.getModifiedDate(ticket["updated_at"])
    ticket["tags"] = queryHandler.getModifiedTags(ticket["tags"])


    ticket_list = []
    ticket_list.append(ticket)

    seperator = ","
    userIds = queryHandler.getUserIds(ticket_list,"requester_id")
    assigneeIds = queryHandler.getUserIds(ticket_list,"assignee_id")
    #userData = queryHandler.getUserData(endpoint2+seperator.join(userIds)+","+seperator.join(assigneeIds))

    try:
        userData = queryHandler.getUserData(endpoint2+seperator.join(userIds)+","+seperator.join(assigneeIds))
    except:
        response = False
    if response is False or userData is None:
        #return "Error routing the page"
        return render_template("404.html"), 404

    userMapping = queryHandler.getMapping(userData)
    keys = ["requester_id","assignee_id"]
    fields = ["requester","assignee"]
    ticket_list = queryHandler.getModifiedTickets(ticket_list,userMapping,keys,fields)


    keys = ["group_id"]
    fields = ["group"]
    #groups = queryHandler.getGroups(endpoint3)

    try:
        groups = queryHandler.getGroups(endpoint3)
    except:
        response = False
    if response is False or groups is None:
        #return "Error routing the page"
        return render_template("404.html"), 404

    groupMapping = queryHandler.getMapping(groups)
    ticket_list = queryHandler.getModifiedTickets(ticket_list,groupMapping,keys,fields)

    with open('TicketMapping.txt') as f: #TicketMapping contains which fields to be shown on the ticket details page
        data= f.read() #first dictionary contains left data to be displayed on the left and second dictionary indicates data to be displayed on the right

    ticket_key_values = ast.literal_eval(data)

    return render_template("ticket_details.html", len = len(ticket_key_values), ticket_data = ticket_list,ticket_key_values=ticket_key_values )



if __name__== "__main__":
    app.run(host='localhost', port=5050, debug=True)
    #app.run()
