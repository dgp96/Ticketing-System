from Classes.Client import Client as Client
from Classes.Utils import Utils as Utils

def test_userDataDetails():
    #checks if getIds returns only unique ids to remove redundancy
    util = Utils()
    data = [
    {
        "url": "https://zccdgp.zendesk.com/api/v2/tickets/1.json",
        "id": 1,
        "requester_id": 422082826411
    },
    {
         "url": "https://zccdgp.zendesk.com/api/v2/tickets/2.json",
         "id": 2,
         "requester_id": 1903521205887
    },
    {
        "url": "https://zccdgp.zendesk.com/api/v2/tickets/3.json",
        "id": 3,
        "requester_id": 1903521205887
    }
    ]

    assert len(util.getIds(data,"requester_id")) == 2 #since 2 ids are repeated we only have length=2

def test_userMapping():
    #checks if the id gets mapped to the current _name
    util = Utils()
    user_data = [
    {
        "id": 422082826411,
        "url": "https://zccdgp.zendesk.com/api/v2/users/422082826411.json",
        "name": "The Customer"
    },
    {
         "id": 1903521205887,
         "url": "https://zccdgp.zendesk.com/api/v2/users/1903521205887.json",
         "name": "Dharmit Prajapati"
    }
    ]

    userMapping = {
        "422082826411": "The Customer",
        "1903521205887": "Dharmit Prajapati"
    }

    util_userMapping = util.mapIds(user_data)
    assert userMapping["422082826411"] == util_userMapping["422082826411"]
    assert userMapping["1903521205887"] == util_userMapping["1903521205887"]

def test_modifiedTicketData():
    #checks if ticket data has new attribute "requester_name" after calling the modified function
    util = Utils()
    ticket = [
    {
        "url": "https://zccdgp.zendesk.com/api/v2/tickets/1.json",
        "id": 1,
        "requester_id": 422082826411
    },
    {
         "url": "https://zccdgp.zendesk.com/api/v2/tickets/2.json",
         "id": 2,
         "requester_id": 1903521205887
    },
    {
        "url": "https://zccdgp.zendesk.com/api/v2/tickets/3.json",
        "id": 3,
        "requester_id": 1903521205887
    }
    ]

    userMapping = {
        "422082826411": "The Customer",
        "1903521205887": "Dharmit Prajapati"
    }

    keys = ["requester_id"]
    fields = ["requester"]
    tickets = util.modifyTicket(ticket,userMapping,keys,fields)
    assert tickets[0]["requester_name"] == userMapping["422082826411"]

def test_modifiedDate():
    #remove the timezone part from the date fields
    util = Utils()
    api_date = "2021-11-22T08:15:40Z"
    expectedDate = "2021-11-22 08:15:40"
    modifiedDate = util.modifyDate(api_date)

    assert modifiedDate==expectedDate

def test_tags():
    #tags are retrieved as a list in the response, need to convert them to a single comma-separated string to display on UI
    util = Utils()
    tags = ["laborum","mollit","proident"]
    expectedTag = "laborum,mollit,proident"
    modifiedTags = util.modifyTags(tags)
    assert modifiedTags==expectedTag
