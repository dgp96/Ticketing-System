from flask import Flask,render_template,request
from Classes.Client import Client as Client
from Classes.QueryHandler import QueryHandler as QueryHandler
from Classes.Utils import Utils as Utils
import requests
import ujson
app = Flask(__name__)

@app.errorhandler(404)

# inbuilt function which takes error as parameter
def page_not_found(e):
    #return "404",404
    return render_template("404.html"), 404
# # defining function
#
#   #return render_template("404.html"), 404



@app.route('/')
def index():
    #print("frgnr")
    #return "New Instance"
    endpoint1 = "api/v2/tickets"
    endpoint2 = "api/v2/users/show_many.json?ids="
    endpoint3 = "api/v2/groups"
    #endpoint4 = "api/v2/tickets/count"
    response = True

    queryHandler = QueryHandler()
    try:
        tickets,count = queryHandler.getTicketResponse(endpoint1)
    except:
        response = False
    if response is False or tickets is None  or len(tickets) == 0:
        return "Error routing the page"

    seperator = ","
    userIds = queryHandler.getUserIds(tickets,"requester_id")
    assigneeIds = queryHandler.getUserIds(tickets,"assignee_id")

    try:
        userData = queryHandler.getUserData(endpoint2+seperator.join(userIds)+","+seperator.join(assigneeIds))
    except:
        response = False
    if response is False or userData is None:
        return "Error routing the page"

    userMapping = queryHandler.getMapping(userData)
    keys = ["requester_id","assignee_id"]
    fields = ["requester","assignee"]
    tickets = queryHandler.getModifiedTickets(tickets,userMapping,keys,fields)

    keys = ["group_id"]
    fields = ["group"]

    try:
        groups = queryHandler.getGroups(endpoint3)
    except:
        response = False
    if response is False or groups is None:
        return "Error routing the page"



    groupMapping = queryHandler.getMapping(groups)
    tickets = queryHandler.getModifiedTickets(tickets,groupMapping,keys,fields)


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
    return render_template("bs4_account_tickets.html", len = len(tickets), page_data=page_data, ticket_data = tickets)

@app.route('/page/<int:pg_no>')
def paginate(pg_no):
    # here we want to get the value of user (i.e. ?user=some-value)
    #pg_no = request.args.get('page')
    print("Page no: " +str(pg_no))
    if pg_no is None or pg_no<=0:
        return "Error routing the page"



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
        return "Error routing the page"

    seperator = ","
    userIds = queryHandler.getUserIds(tickets,"requester_id")
    assigneeIds = queryHandler.getUserIds(tickets,"assignee_id")

    #userData = queryHandler.getUserData(endpoint2+seperator.join(userIds)+","+seperator.join(assigneeIds))
    try:
        userData = queryHandler.getUserData(endpoint2+seperator.join(userIds)+","+seperator.join(assigneeIds))
    except:
        response = False
    if response is False or userData is None:
        return "Error routing the page"



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
        return "Error routing the page"

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

    return render_template("bs4_account_tickets.html", len = len(tickets), page_data=page_data, ticket_data = tickets)
    #return "You're requesting page# " + pg_no

@app.route('/ticket/<int:ticket_id>')
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
        return "Error routing the page"

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
        return "Error routing the page"

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
        return "Error routing the page"

    groupMapping = queryHandler.getMapping(groups)
    ticket_list = queryHandler.getModifiedTickets(ticket_list,groupMapping,keys,fields)
    #return "You're viewing ticket with id: " +str(ticket_id)
    ticket_key_values = [
    {
     "Requester":"requester_name","Assignee":"assignee_name","Tags":"tags"
    },
    {
    "Ticket ID" : "id", "Date Created":"created_at", "Last Updated":"updated_at", "Status":"status", "Priority":"priority",
    "Type":"type","Group":"group_name","Subject":"subject", "Description":"description"
    }
    ]

    return render_template("shop_user_profile_with_ticket.html", len = len(ticket_key_values), ticket_data = ticket_list,ticket_key_values=ticket_key_values )



if __name__== "__main__":
    app.run(host='localhost', port=5050, debug=True)
    #app.run()
