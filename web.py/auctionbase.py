#!/usr/bin/env python

import sys; sys.path.insert(0, 'lib') # this line is necessary for the rest
import os                             # of the imports to work!

import web
import sqlitedb
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

SEARCH_DEFAULT_ENC = 0
SEARCH_WITH_ONLY_ITEMID = 1
SEARCH_WITH_ONLY_USERID = 2
SEARCH_WITH_ONLY_MIN = 4
SEARCH_WITH_ONLY_MAX = 16

###########################################################################################
##########################DO NOT CHANGE ANYTHING ABOVE THIS LINE!##########################
###########################################################################################

######################BEGIN HELPER METHODS######################

# helper method to convert times from database (which will return a string)
# into datetime objects. This will allow you to compare times correctly (using
# ==, !=, <, >, etc.) instead of lexicographically as strings.

# Sample use:
# current_time = string_to_time(sqlitedb.getTime())

def string_to_time(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

def getInputEnc(post_params):
    enc = SEARCH_DEFAULT_ENC 
    if post_params.get('itemID'):
        enc = enc | SEARCH_WITH_ONLY_ITEMID 
    if post_params.get('userID'):
        enc = enc | SEARCH_WITH_ONLY_USERID 
    if post_params.get('minPrice'):
        enc = enc | SEARCH_WITH_ONLY_MIN
    if post_params.get('maxPrice'):
        enc = enc | SEARCH_WITH_ONLY_MAX
    return enc


# helper method to render a template in the templates/ directory
#
# `template_name': name of template file to render
#
# `**context': a dictionary of variable names mapped to values
# that is passed to Jinja2's templating engine
#
# See curr_time's `GET' method for sample usage
#
# WARNING: DO NOT CHANGE THIS METHOD
def render_template(template_name, **context):
    extensions = context.pop('extensions', [])
    globals = context.pop('globals', {})

    jinja_env = Environment(autoescape=True,
            loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
            extensions=extensions,
            )
    jinja_env.globals.update(globals)

    web.header('Content-Type','text/html; charset=utf-8', unique=True)

    return jinja_env.get_template(template_name).render(context)

#####################END HELPER METHODS#####################

urls = ('/currtime', 'curr_time',
        '/selecttime', 'select_time',
        '/search', 'search_db',
        '/winner', 'findWinner',
        '/add_bid', 'addBid',
        )

class curr_time:
    # A simple GET request, to '/currtime'
    #
    # Notice that we pass in `current_time' to our `render_template' call
    # in order to have its value displayed on the web page
    def GET(self):
        current_time = sqlitedb.getTime()
        return render_template('curr_time.html', time = current_time)

class select_time:
    # Aanother GET request, this time to the URL '/selecttime'
    def GET(self):
        return render_template('select_time.html')

    # A POST request
    #
    # You can fetch the parameters passed to the URL
    # by calling `web.input()' for **both** POST requests
    # and GET requests
    def POST(self):
        post_params = web.input()
        MM = post_params['MM']
        dd = post_params['dd']
        yyyy = post_params['yyyy']
        HH = post_params['HH']
        mm = post_params['mm']
        ss = post_params['ss'];
        enter_name = post_params['entername']

        selected_time = '%s-%s-%s %s:%s:%s' % (yyyy, MM, dd, HH, mm, ss)
        update_message = '(Hello, %s. Previously selected time was: %s.)' % (enter_name, selected_time)

        t = sqlitedb.transaction()
        try:
            sqlitedb.updateTime(selected_time)
        except:
            t.rollback()
            update_message = '(Hello, %s. Previously selected time was: %s. Current Time is not updated, as it does not move backward)' % (enter_name, selected_time)
            return render_template('select_time.html', message = update_message, type = 'danger')
        else:
            t.commit()
            return render_template('select_time.html', message = update_message, type = 'warning')

class search_db:
    def GET(self):
        return render_template('search.html')

    def POST(self):
        post_params = web.input()
        enc = getInputEnc(post_params)

        input_itemID = None
        input_userID = None
        input_minPrice = None
        input_maxPrice = None
        
        #print 'enc value is', enc

        if (enc & SEARCH_WITH_ONLY_ITEMID):
            item_id = post_params['itemID']
            input_itemID = '%s' % (item_id)
            #print 'input_itemID = ', input_itemID

        if (enc & SEARCH_WITH_ONLY_USERID):
            user_id = post_params['userID']
            input_userID = '%s' % (user_id)
            #print 'input_userID = ', input_userID

        if (enc & SEARCH_WITH_ONLY_MIN):
            min_price = post_params['minPrice']
            input_minPrice = '%s' % (min_price)
            #print 'input_minPrice = ', input_minPrice

        if (enc & SEARCH_WITH_ONLY_MAX):
            max_price = post_params['maxPrice']
            input_maxPrice = '%s' % (max_price)
            #print 'input_maxPrice = ', input_maxPrice

        input_status = post_params['status']            

        result_getItemById = sqlitedb.getItemById(input_itemID, input_userID, input_minPrice, input_maxPrice, input_status, enc)

        if (result_getItemById is not None):
#            final_result = {"itemInfoResult":result_getItemById}
            return render_template('search.html', search_result = result_getItemById)
        else:
            fail_message = 'No results found.'
            return render_template('search.html', message = fail_message)


class findWinner:
    def GET(self):
        return render_template('winner.html')
    
    def POST(self):
        post_params = web.input()
        item_id = post_params['itemID']
        winner_info = sqlitedb.getWinnerByItemId(item_id)
        if (sqlitedb.isAuctionOpen(item_id)):
            open_message = 'This auction is still open'
            return render_template('winner.html', message = open_message, status = 'OPEN')
        else:
            if not (winner_info is None):
                return render_template('winner.html', search_result = winner_info, status = 'CLOSED')
            else:
                win_message = 'No auction winner found'
                return render_template('winner.html', message = win_message, status = 'CLOSED')

class addBid:
    def GET(self):
        return render_template('add_bid.html')
    
    def POST(self):
        post_params = web.input()
        if (post_params.get('itemID') and post_params.get('userID') and post_params.get('price')):
            item_id = post_params['itemID']
            user_id = post_params['userID']
            price = post_params['price']
            addBid_status = sqlitedb.insertBid(item_id, user_id, price)
            if (addBid_status):
                return render_template('add_bid.html', add_result = 'Added Bid Successfully!', type = 'warning')
            else:
                return render_template('add_bid.html')
        else:
            fail_message = 'Please input all the values correctly: itemID, userID, and price(must be a number)!'
            return render_template('add_bid.html', message = fail_message, type = 'danger')


###########################################################################################
##########################DO NOT CHANGE ANYTHING BELOW THIS LINE!##########################
###########################################################################################

if __name__ == '__main__':
    web.internalerror = web.debugerror
    app = web.application(urls, globals())
    app.add_processor(web.loadhook(sqlitedb.enforceForeignKey))
    app.run()
