from reverence import blue
from operator import attrgetter

eve = blue.EVE("/home/aragaer/.wine/drive_c/Program Files/CCP/EVE")
c = eve.getcachemgr()
cfg = eve.getconfigmgr()
cmc = c.LoadCacheFolder("CachedMethodCalls")
cmcr = c.LoadCacheFolder("CachedMethodCallResults")
my_stuff = {"GetCharOrders": {}, "GetPublicInfo": {}, "GetOrders": {}}
for key, obj in cmc.iteritems():
    if key[1] not in my_stuff.keys():
        continue
    my_stuff[key[1]][key[2]] = obj

char_id_to_name = {}
char_name_to_id = {}

chlist = my_stuff["GetPublicInfo"]
for key, obj in chlist.iteritems():
    name =  obj['lret'].characterName
    char_id_to_name[key] = name
    char_name_to_id[name] = key
del chlist

def get_orders_for(charname):
    char_id = char_name_to_id[charname]
    if char_id is None:
        return []
    return my_stuff["GetCharOrders"][char_id]['lret']

def get_concurrent_orders(order):
    all_orders = cmc[('marketProxy', 'GetOrders',
                      order.regionID, order.typeID)]['lret']
    if (order.bid):
        all_orders = all_orders[1]
    else:
        all_orders = all_orders[0]
    all_orders.sort(key = attrgetter('price'), reverse = order.bid)
    return all_orders

def check_orders_for(charname):
    char_orders = get_orders_for(charname)
    for order in char_orders:
        print 'Concurrents for %(item)s:' % {'item': cfg.invtypes.Get(order.typeID).name}
        conc = get_concurrent_orders(order)
        if (conc[0].orderID == order.orderID):
            print "Is on the top"
        else:
            new_price = conc[0].price
            if order.bid:
                new_price += .01
            else:
                new_price -= .01
            print "Is losing! Update it to %10.2f" % new_price

