# Change the following settings to suit your needs:
 
EVEROOT = r"E:/EVE"
OUTPATH = r"N:/temp"

import time
import os
from reverence import blue

def evetime2date(evetime):
    s = (evetime - 116444736000000000) / 10000000 
    return time.strftime("%Y-%m-%d", time.gmtime(s))

eve = blue.EVE(EVEROOT)
cfg = eve.getconfigmgr()
cachemgr = eve.getcachemgr()
cmc = cachemgr.LoadCacheFolder("CachedMethodCalls")

print "Deleting old records... \n"
for root, dirs, files in os.walk(OUTPATH, topdown=False):
    for name in files:
        os.remove(os.path.join(root, name))


for key, obj in cmc.iteritems():
    if key[1]=="GetOldPriceHistory":
        item = cfg.invtypes.Get(key[3])
        region = cfg.evelocations.Get(key[2])
        print "Processing " + item.name + " [" + region.locationName +"]... \n"
        csvfile = open(os.path.join(OUTPATH, item.name+"-"+region.locationName+".csv"), 'w')
        csvfile.write("historyDate, lowPrice, highPrice, avgPrice, volume, orders\n")
        for history_item in obj['lret']:
            line = "%(historyDate)s, %(lowPrice).2f, %(highPrice).2f, %(avgPrice).2f, %(volume)i, %(orders)i" % \
                    {'historyDate': evetime2date(history_item['historyDate']), \
                    'lowPrice': history_item['lowPrice']/1000, \
                    'highPrice': history_item['highPrice']/1000, \
                    'avgPrice': history_item['avgPrice']/1000, \
                    'volume': history_item['volume'], \
                    'orders': history_item['orders']}
            csvfile.write(line+"\n")
        csvfile.close()
