#!/usr/bin/env python

import db
import api
import time

access_token = ''

while True:

    if len(access_token) == 0:
        print "Obtaining Access token, please wait..."
        access_token = api.getAccessToken()
    
        if len(access_token) == 0:
            print "Access token could not be obtained, waiting for 5 seconds"
            time.sleep(5)
            continue
        else:
            print "Access token obtained: " + access_token
    
    # Check if there are items in the queue
    scan = db.frontQueueItem()
    if scan is not None:
        print scan;
    
        # Attempt to POST to API
        print "Attempting POST to API"
        response_code = api.record(access_token, scan["shop_code"], scan["isbn"])
        if response_code == 403:
            # Blank access_token to trigger obtaining of new one
            access_token = ''
            print "Request forbidden, waiting for 5 seconds..."
            time.sleep(5)
        elif response_code == 405:
            print "405 Method not allowed, waiting for 5 minutes..."
            time.sleep(300)
        elif response_code == 201:
            print "POST to API successful, deleting item from queue"

            # Delete the item from the queue
            db.deleteQueueItem( scan["id"] )
        else:
            # Internet connection not available
            print "POST to API failed, waiting for 5 seconds..."
            time.sleep(5)
    else:
        print "Nothing in queue, waiting for 5 seconds..."
        time.sleep(5)
