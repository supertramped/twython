import json
from pymongo import MongoClient
import time
import numpy as np
import pandas as pd

results = pd.DataFrame(columns=('n','mrt','sd','fr','et','cr_at'))

conn = MongoClient()
db = conn["nps"]
coll = "tweets"

fp = open("chains.txt", "r")
lines = fp.readlines()
fp.close()
r = 0
for line in lines:
    ids = line.split(",")
    times = []
    first = True
    origin_ts = None
    closing_ts = None
    end = None
    st = None
    for id in ids:
        t = db[coll].find_one( { "id_str" :id }, { "created_at":1,'_id':0} )
        print t

        if t is not None and t['created_at'] is not None:
            t_sec = time.mktime(time.strptime(t['created_at'],"%a %b %d %H:%M:%S +0000 %Y"))
            if first == True:
                first_val = t_sec
                first = False
            else:
                times.append(first_val - t_sec)
                first_val = t_sec
        else:
            pass

    res = []
    ids.reverse()
    st = ids[0].strip()
    end = ids[1]
    t2 = db[coll].find_one( { "id_str" :end}, { "created_at":1,'_id':0} )
    t1 = db[coll].find_one( { "id_str" :st}, { "created_at":1,'_id':0} )
    st = time.mktime(time.strptime(t1['created_at'],"%a %b %d %H:%M:%S +0000 %Y"))
    end = time.mktime(time.strptime(t2['created_at'],"%a %b %d %H:%M:%S +0000 %Y"))

    res.append(len(times)+1)
    res.append(np.mean(times))
    res.append(np.std(times))
    res.append(end-st)
    res.append(np.sum(times))
    res.append(t1['created_at'])

    results.loc[r] = res
    r = r+1

    print "Total messages," , len(times)+1
    print "Mean response time," , np.mean(times) , " seconds"
    print "ST Dev,", np.std(times)
    print "Time taken to respond to a complaint," , (end-st)/60, " minutes"

    print "Total time taken to resolve query,", np.sum(times)/60 , " minutes"
    

    #get avg
    print results


    
