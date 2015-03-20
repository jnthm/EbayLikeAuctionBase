
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS145 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "<>"
DEBUG = False

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

def closeFiles(fItemInfo, fItemCategory, fBidInfo, fBidderInfo, fUserInfo):
    fItemInfo.close()
    fItemCategory.close()
    fBidInfo.close()
    fBidderInfo.close()
    fUserInfo.close()
    

"""
Create the DAT file for ItemInfo Table
"""
def createItemInfoTable(item, f):
    if (DEBUG):
        print "printing ItemINFO"
        print "-=-=-=-=-=-=-=-=-=-="
        print item["ItemID"]
        print item["Name"]
        if item["Description"]:        
            print item["Description"]
        else:
            print "NULL"
        print item["Seller"]["UserID"]
        print item["Started"]
        print item["Ends"]
        if item.get("Buy_Price"):
            print item["Buy_Price"]
        else:
            print "NULL"
        print item["First_Bid"]

    f.write(item["ItemID"] + columnSeparator) 
    f.write(item["Name"] + columnSeparator)
    descr = "NULL"
    if item["Description"]:
        descr = item["Description"]
    f.write(descr + columnSeparator)
    f.write(item["Seller"]["UserID"] + columnSeparator) 
    f.write(transformDttm(item["Started"]) + columnSeparator) 
    f.write(transformDttm(item["Ends"]) + columnSeparator)
    buyPrice = "NULL"
    if item.get("Buy_Price"):
        buyPrice = transformDollar(item["Buy_Price"])
    f.write(buyPrice + columnSeparator) 
    f.write(transformDollar(item["First_Bid"]) + "\n")

"""
Create the DAT file for BidInfo Table
"""
def createBidInfoTable(item, f):
    if (DEBUG):
        print "printing BIDINFO"
        print "-=-=-=-=-=-=-=-=-=-="
        print item["ItemID"]
        print item["Currently"]
        print item["Number_of_Bids"]

    f.write(item["ItemID"] + columnSeparator + transformDollar(item["Currently"]) + columnSeparator + item["Number_of_Bids"] + "\n" )

"""
Create the DAT file for BidderInfo Table
"""
def createBidderInfoTable(item, f):
    if (DEBUG):
        print "printing BIDDERINFO"
        print "-=-=-=-=-=-=-=-=-=-="
        bidsCollection = item["Bids"]
        if bidsCollection:
            print item["ItemID"]
            i=0
            for eachBid in bidsCollection:
                print bidsCollection[i]["Bid"]["Bidder"]["UserID"]
                print bidsCollection[i]["Bid"]["Time"]
                print bidsCollection[i]["Bid"]["Amount"]
                i=i+1

    bidsCollection = item["Bids"]
    if bidsCollection:
        i=0
        for eachBid in bidsCollection:
            f.write(item["ItemID"] + columnSeparator)
            f.write(bidsCollection[i]["Bid"]["Bidder"]["UserID"] + columnSeparator)
            f.write(transformDttm(bidsCollection[i]["Bid"]["Time"]) + columnSeparator)
            f.write(transformDollar(bidsCollection[i]["Bid"]["Amount"]) + "\n")
            i=i+1

"""
Create the DAT file for ItemCategory Table
"""
def createItemCategoryTable(item, f):
    if (DEBUG):
        print "printing ITEMCATEGORYINFO"
        print "-=-=-=-=-=-=-=-=-=-=-=-=-="
        Categories = item["Category"]
        for eachCategory in Categories:
            print item["ItemID"], eachCategory

    Categories = item["Category"]
    for eachCategory in Categories:
        f.write(item["ItemID"] + columnSeparator + eachCategory + "\n")

"""
Create the DAT file for USERINFO table.
"""
def createUserInfoTable(item, f):
    # User is a seller here.
    SellerUserID = item["Seller"]["UserID"]
    # check for NULL
    if item["Location"]:
        SellerUserLocation = item["Location"]        
    else:
        SellerUserLocation = "NULL"
    if item["Country"]:
        SellerUserCountry = item["Country"]        
    else:
        SellerUserCountry = "NULL"
    SellerUserRating = item["Seller"]["Rating"]

    if (DEBUG):
        print "printing USERINFO"
        print "-=-=-=-=-=-=-=-=-="
        print SellerUserID, SellerUserLocation, SellerUserCountry, SellerUserRating
#        print BidderUserID, BidderUserLocation, BidderUserCountry, BidderUserRating

    f.write(SellerUserID + columnSeparator)
    f.write(SellerUserLocation + columnSeparator + SellerUserCountry + columnSeparator) 
    f.write(SellerUserRating)
    f.write("\n")

    bidsCollection = item["Bids"]

    if bidsCollection:
        i=0
        for eachBid in bidsCollection:
            BidderUserID = bidsCollection[i]["Bid"]["Bidder"]["UserID"]
            f.write(BidderUserID + columnSeparator)
            if bidsCollection[i]["Bid"]["Bidder"].get("Location"):
                BidderUserLocation = bidsCollection[i]["Bid"]["Bidder"]["Location"]
            else:
                BidderUserLocation = "NULL"
            if bidsCollection[i]["Bid"]["Bidder"].get("Country"):
                BidderUserCountry = bidsCollection[i]["Bid"]["Bidder"]["Country"]
            else:
                BidderUserCountry = "NULL"
            f.write(BidderUserLocation + columnSeparator + BidderUserCountry + columnSeparator)
            BidderUserRating = bidsCollection[i]["Bid"]["Bidder"]["Rating"]
            f.write(BidderUserRating + "\n")
            i=i+1

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file, fItemInfo, fItemCategory, fBidInfo, fBidderInfo, fUserInfo):
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file

        for item in items:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """
            createUserInfoTable(item, fUserInfo)
            createItemCategoryTable(item, fItemCategory)
            createBidderInfoTable(item, fBidderInfo)
            createBidInfoTable(item, fBidInfo)
            createItemInfoTable(item, fItemInfo)
            pass

"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument

    fItemInfo = open('ItemInfo.Dat','a')
    fItemCategory = open('ItemCategory.Dat','a')        
    fBidInfo = open('BidInfo.Dat','a')
    fBidderInfo = open('BidderInfo.Dat','a')
    fUserInfo = open('UserInfo.Dat','a')

    for f in argv[1:]:
        if isJson(f):
            parseJson(f, fItemInfo, fItemCategory, fBidInfo, fBidderInfo, fUserInfo)
            print "Success parsing " + f

    closeFiles(fItemInfo, fItemCategory, fBidInfo, fBidderInfo, fUserInfo)

if __name__ == '__main__':
    main(sys.argv)
