import web

db = web.database(dbn='sqlite',
        db='MyAuctionBase.db' 
    )

SEARCH_DEFAULT_ENC = 0
SEARCH_WITH_ONLY_ITEMID = 1
SEARCH_WITH_ONLY_USERID = 2
SEARCH_WITH_ONLY_MIN = 4
SEARCH_WITH_ONLY_MAX = 16


######################BEGIN HELPER METHODS######################

# Enforce foreign key constraints
# WARNING: DO NOT REMOVE THIS!
def enforceForeignKey():
    db.query('PRAGMA foreign_keys = ON')

# initiates a transaction on the database
def transaction():
    return db.transaction()
# Sample usage (in auctionbase.py):
#
# t = sqlitedb.transaction()
# try:
#     sqlitedb.query('[FIRST QUERY STATEMENT]')
#     sqlitedb.query('[SECOND QUERY STATEMENT]')
# except:
#     t.rollback()
#     raise
# else:
#     t.commit()
#
# check out http://webpy.org/cookbook/transactions for examples

# returns the current time from your database
def getTime():
    query_string = 'select CurrTime from CurrentTime'
    results = query(query_string)
    # alternatively: return results[0]['CurrTime']
    return results[0].CurrTime 

# updates the current time in the database
def updateTime(selected_time):
    query_string = 'update CurrentTime set CurrTime = $selTime'
    results = query(query_string, {'selTime': selected_time})


def join_condList(condList):
    #for item in condList:
     #   print item
    return ' and '.join(condList)

# returns a single item specified by the ItemID and UserID in the database
# Note: if the `result' list is empty (i.e. there are no items for a
# a given ID), this will throw an Exception!
def getItemById(item_id, user_id, min_price, max_price, status, enc):

    query_string_itemInfo = 'select * from BidInfo B, ItemInfo I where I.ItemID = B.ItemID and '
    query_string_condList = list()
    query_dict_itemInfo = dict()
    #if enc == SEARCH_DEFAULT_ENC:
    #    return None
    if enc & SEARCH_WITH_ONLY_ITEMID:
        query_string_condList.append('(I.ItemID in (select ItemID from BidInfo where ItemID = $itemID))')
        query_dict_itemInfo['itemID'] = item_id
    if enc & SEARCH_WITH_ONLY_USERID:
        query_string_condList.append('(I.SellerUserID = $userID)')
        query_dict_itemInfo['userID'] = user_id
    if enc & SEARCH_WITH_ONLY_MIN:
        query_string_condList.append('(I.ItemID in (select ItemID from BidInfo where Currently >= $minPrice))')
        query_dict_itemInfo['minPrice'] = min_price
    if enc & SEARCH_WITH_ONLY_MAX:
        query_string_condList.append('(I.ItemID in (select ItemID from BidInfo where Currently <= $maxPrice))')
        query_dict_itemInfo['maxPrice'] = max_price

    if (status == 'open'):
        query_string_condList.append('(B.Currently < I.BuyPrice or I.BuyPrice is NULL)')
        query_string_condList.append('(Started <= (select CurrTime from CurrentTime))')
        query_string_condList.append('(Ends > (select CurrTime from CurrentTime))')
    elif (status == 'close'):
        query_string_condList.append('((B.Currently >= I.BuyPrice) OR (Ends <= (select CurrTime from CurrentTime)))')
    elif (status == 'notStarted'):
        query_string_condList.append('(Started > (select CurrTime from CurrentTime))')

    query_string_itemInfo += join_condList(query_string_condList)

    #print 'query_string_itemInfo = ', query_string_itemInfo
    #print 'query_dict_itemInfo = ', query_dict_itemInfo

    query_dict = query_dict_itemInfo
    query_string = query_string_itemInfo
    result = query(query_string, query_dict)
    #print 'result = ', result

    if not (isResultEmpty(result)):
        result = query(query_string, query_dict)
        return result
    else:
        return None        


# returns a single item specified by the Item's ID in the database
# Note: if the `result' list is empty (i.e. there are no items for a
# a given ID), this will throw an Exception!
def getItemByItemId(item_id):
    query_string = 'select * from ItemInfo where ItemID = $itemID'
    result = query(query_string, {'itemID': item_id})

    if not (isResultEmpty(result)):
        result = query(query_string, {'itemID': item_id})
        return result
    else:
        return None        

# returns a single item specified by the SellerUser's ID in the database
# Note: if the `result' list is empty (i.e. there are no items for a
# a given ID), this will throw an Exception!
def getItemByUserId(user_id):
    query_string = 'select * from ItemInfo where SellerUserID = $userID'
    result = query(query_string, {'userID': user_id})

    if not (isResultEmpty(result)):
        result = query(query_string, {'userID': user_id})
        return result
    else:
        return None        



# returns a single item specified by the Item's ID in the database
# Note: if the `result' list is empty (i.e. there are no items for a
# a given ID), this will throw an Exception!
def getBidInfoById(item_id):
    # TODO: rewrite this method to catch the Exception in case `result' is empty
    query_string = 'select * from BidInfo where ItemID = $itemID'
    result = query(query_string, {'itemID': item_id})
    return result[0]

# returns a single item specified by the Item's ID in the database
# Note: if the `result' list is empty (i.e. there are no items for a
# a given ID), this will throw an Exception!
def getBidderInfoById(item_id):
    # TODO: rewrite this method to catch the Exception in case `result' is empty
    query_string = 'select * from BidderInfo where ItemID = $itemID'
    result = query(query_string, {'itemID': item_id})
    return result[0]

# returns a single winner specified by the Item's ID in the database
# Note: if the `result' list is empty (i.e. there are no items for a
# a given ID), this will throw an Exception!
def getWinnerByItemId(item_id):
    query_string = 'select * from UserInfo where UserID in (select BidderUserID from BidderInfo where ItemID = $itemID and Amount in (select max(Amount) from BidderInfo where ItemID = $itemID))'
    result = query(query_string, {'itemID': item_id})
    if not (isResultEmpty(result)):
        result = query(query_string, {'itemID': item_id})
        return result
    else:
        return None

def isAuctionOpen(item_id):
    query_string = 'select * from ItemInfo where ItemID = $itemID and Started <= (select CurrTime from CurrentTime) and Ends > (select CurrTime from CurrentTime) and ( ((select Currently from BidInfo where ItemID = $itemID) < (select BuyPrice from ItemInfo where ItemID = $itemID)) OR BuyPrice is NULL)'
    result = query(query_string, {'itemID': item_id})
    return not (isResultEmpty(result))

def isAuctionNotStarted(item_id):
    query_string = 'select * from ItemInfo where ItemID = $itemID and Started > (select CurrTime from CurrentTime)'
    result = query(query_string, {'itemID': item_id})
    return not (isResultEmpty(result))

def insertBid(item_id, user_id, price):
    if (isAuctionOpen(item_id)):
        query_string = 'insert into BidderInfo (ItemID, BidderUserID, Time, Amount) select $itemID, $userID, CurrTime, $price_new from CurrentTime'
        query_dict = {'itemID': item_id, 'userID' : user_id, 'price_new': price}

        t = transaction()
        try:
            query(query_string, query_dict)
        except:
            t.rollback()
            return False
        else:
            t.commit()
            return True
    else:
        return False

# helper method to determine whether query result is empty
# Sample use:
# query_result = sqlitedb.query('select currenttime from Time')
# if (sqlitedb.isResultEmpty(query_result)):
#   print 'No results found'
# else:
#   .....
#
# NOTE: this will consume the first row in the table of results,
# which means that data will no longer be available to you.
# You must re-query in order to retrieve the full table of results
def isResultEmpty(result):
    try:
        result[0]
        return False
    except:
        return True

# wrapper method around web.py's db.query method
# check out http://webpy.org/cookbook/query for more info
def query(query_string, vars = {}):
    #print 'query_string = ', query_string
    #print 'vars = ', vars
    return db.query(query_string, vars)

#####################END HELPER METHODS#####################
