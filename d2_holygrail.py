import re

item_groups = []
fname = 'd2_items.txt'
fname_start = 'd2_items_start.txt'

#0-9 is misc stuff, normal armors, socketed stuff, runewords, etc
#10-19 is essences, keys, runes
#20-29 is gems
#30-39 is overflow uniques

# start putting the storage after
startPage = 40

itemCt = 0
itemCtEth = 0

itemsLeft = 0
itemsLeftEth = 0

NAME = 0
TYPE = 1
ITEM_WD = 2
ITEM_HT = 3
TIER = 4
ETH = 5
FOUND = 6
FOUND_ETH = 7
COMMENT = 8
PAGE = 9
X_OFFSET = 10
Y_OFFSET = 11

TIER_NORMAL = 1
TIER_EXCEPTIONAL = 2
TIER_ELITE = 3

ETH_BOTH = 1
ETH_NORMAL_ONLY = 2
ETH_ETH_ONLY = 3


# for tier, 1/2/3 means normal/exceptional/elite
# for eth, 1 means has both normal/eth, 2 means normal only, 3 means eth only

def calculateoffsets():
    global item_groups
    global itemCt
    global itemCtEth
    global itemsLeft
    global itemsLeftEth
    global startPage
    
    currentPage = startPage
    currentX = 0
    currentY = 0
    
    setsPerPage = 2
    for (gname, group) in item_groups:
        for (sgname, subgroup) in group:
        
            # count items left
            for item in subgroup:
                eth = item[ETH]
                
                if eth == 1:
                    itemCt += 1
                    itemCtEth += 1
                    if not item[FOUND]:
                        itemsLeft += 1
                    if not item[FOUND_ETH]:
                        itemsLeftEth += 1
                elif eth == 2:
                    itemCt += 1
                    if not item[FOUND]:
                        itemsLeft += 1
                else:
                    itemCt += 1
                    if not item[FOUND_ETH]:
                        itemsLeft += 1
        
            # mark misc/sets and increment pages in a specific way.
            if gname == 'Misc' or gname == 'Sets':
                    
                for item in subgroup:
                    item[PAGE] = currentPage
                    item[X_OFFSET] = currentX + 1
                    item[Y_OFFSET] = currentY + 1
                    
                pageIncVal = 1
                if gname == 'Sets':
                    setsPerPage -= 1
                    if setsPerPage == 0:
                        setsPerPage = 2
                        currentX = 0
                        currentY = 0
                    else:
                        currentX = 0
                        currentY = 5
                        pageIncVal = 0
                    
                currentPage += pageIncVal
                
            # for all others, try to pack based on the largest item in the group
            else:
                
                maxHt = 0
                for item in subgroup:
                    maxHt = max(maxHt, item[ITEM_HT])
                   
                for item in subgroup:
                    reqWd = item[ITEM_WD]
                    if item[ETH] == ETH_BOTH:
                        reqWd *= 2
                    
                    if currentX + reqWd > 10:
                        currentX = 0
                        currentY += maxHt
                    if currentY + maxHt > 10:
                        currentY = 0
                        currentPage += 1
                    
                    item[PAGE] = currentPage
                    item[X_OFFSET] = currentX + 1
                    item[Y_OFFSET] = currentY + 1
                    
                    currentX += reqWd

                currentPage += 1
                currentX = 0
                currentY = 0
        
        #always jump 10 pages between groups
        currentPage += 10
        currentPage -= currentPage % 10
    

def readfile():
    global item_groups
    global fname
    global fname_start
    
    try:
        f = open(fname, 'r')
    except:
        f = open(fname_start, 'r')
    
    groupname = ''
    currentgroup = []
    
    subgroupname = ''
    currentsubgroup = []
    
    for line in f.readlines():
        line = line.strip('\n')
        line = re.sub(', ', ',', line)
        members = line.split(',')
        
        if len(members) == 1 and members[0] == '':
            if len(currentsubgroup):
                nsg = []
                for i in currentsubgroup:
                    nsg.append(i)
                currentgroup.append((subgroupname, nsg))
                
                subgroupname = ''
                currentsubgroup = []
            elif len(currentgroup):
                ng = []
                for i in currentgroup:
                    ng.append(i)
                item_groups.append((groupname, ng))
                
                groupname = ''
                currentgroup = []
        elif len(members) == 1 and members[0] != '':
            if groupname == '':
                groupname = members[0]
            elif subgroupname == '':
                subgroupname = members[0]

        elif len(members) >= 6:
            name = members[NAME]
            type = members[TYPE]
            w = int(members[ITEM_WD])
            h = int(members[ITEM_HT])
            tier = int(members[TIER])
            eth = int(members[ETH])
            
            found = False
            foundEth = False
            
            if len(members) >= 8:
                if members[FOUND] == '1':
                    found = True
                if members[FOUND_ETH] == '1':
                    foundEth = True
            
            comment = 'None'
            if len(members) >= 9:
                comment = members[COMMENT]                
                    
            # we'll calculate this each time
            page = 0
            x = 0
            y = 0
                    
            currentsubgroup.append([name, type, w, h, tier, eth, found, foundEth, comment, page, x, y])
        
        elif len(members) > 1:
            print 'malformed INPUT!!!!', members

    if len(currentsubgroup):
        currentgroup.append(currentsubgroup)
    if len(currentgroup):
        item_groups.append((groupname, currentgroup))
    
    calculateoffsets()
    
    f.close()
    
def writefile():
    global item_groups
    global fname
    
    f = open(fname, 'w')
    
    for (name, subgroups) in item_groups:
        f.write(name + '\n')
        
        for (name2, subgroup) in subgroups:
            f.write('\n')
            f.write(name2 + '\n')
            for item in subgroup:
                out = item[NAME] #name
                out += ', ' + item[TYPE] #type
                out += ', ' + str(item[ITEM_WD]) #wd
                out += ', ' + str(item[ITEM_HT]) #ht
                out += ', ' + str(item[TIER]) #tier
                out += ', ' + str(item[ETH]) #eth

                if item[FOUND]: # found
                    out += ', 1'
                else:
                    out += ', 0'
                    
                if item[FOUND_ETH]: # foundEth
                    out += ', 1'
                else:
                    out += ', 0'
                out += ', ' + item[COMMENT] # comment
                f.write(out + '\n')
            
        f.write('\n\n')
        
    f.close()
    
    
def clean(str):
    s = re.sub(' ', '', str)
    s = re.sub("'", '', s)
    s = re.sub('-', '', s)
    s = s.lower()
    return s
    
def searchItems(name):
    
    global item_groups
    
    sname = clean(name)
    
    results = []
    
    for (_, group) in item_groups:
        for (_, subgroup) in group:
            for item in subgroup:
                n = clean(item[NAME])
                
                if re.search(sname, n):
                    results.append(item)
                    
    return results
    
PRINT_LONG = 0
PRINT_SHORT = 1
PRINT_SHORT_NO_FOUND = 2
    
def printItem(item, pr = PRINT_LONG, printEthLoc = False):
    name = item[NAME]
    type = item[TYPE]
    w = item[ITEM_WD]
    h = item[ITEM_HT]
    tier = item[TIER]
    if tier == TIER_NORMAL:
        tier = 'Normal'
    elif tier == TIER_EXCEPTIONAL:
        tier = 'Exceptional'
    elif tier == TIER_ELITE:
        tier = 'Elite'
    eth = item[ETH]
    found = item[FOUND]
    foundEth = item[FOUND_ETH]
    comment = item[COMMENT]
    page = item[PAGE]
    x = item[X_OFFSET]
    y = item[Y_OFFSET]
    
    if eth == ETH_BOTH:
        if found:
            found = 'Y'
        else:
            found = 'n'
        if foundEth:
            foundEth = 'Y'
        else:
            foundEth = 'n'
    elif eth == ETH_NORMAL_ONLY:
        if found:
            found = 'Y'
        else:
            found = 'n'
        foundEth = '_'
    elif eth == ETH_ETH_ONLY:
        if foundEth:
            foundEth = 'Y'
        else:
            foundEth = 'n'
        found = '_'
        
    px = x
    if printEthLoc:
        px += item[ITEM_WD]
    
    if pr == PRINT_SHORT:
        print '  ' + name + ', ' + type + ' (' + tier + '), Loc: ' + str(page) + ' (' + str(px) + ',' + str(y) + '), Found: %s, %s' % (found, foundEth) + ', Com: ' + comment
    elif pr == PRINT_SHORT_NO_FOUND:
        print '  ' + name + ', ' + type + ' (' + tier + '), Loc: ' + str(page) + ' (' + str(px) + ',' + str(y) + '), Com: ' + comment
    else:
        print '  ' + name
        print '  ' + type + ' (' + tier + '), ' + str(w) + 'x' + str(h)
        print '  Found Reg: %s    Found Eth: %s' % (found, foundEth)
        print '  Comment:'
        print '    ' + comment  
        print '  Location      :  Page ' + str(page) + ', Offset (' + str(x) + ', ' + str(y) + ')'
        if eth == ETH_BOTH:
            print '  Location (eth):  Page ' + str(page) + ', Offset (' + str(x + item[ITEM_WD]) + ', ' + str(y) + ')'
    
def process(cmdStr):
 
    global item_groups
    global itemCt
    global itemCtEth
    global itemsLeft
    global itemsLeftEth
 
    tokens = cmdStr.split()
    
    rv = True;
    
    if len(tokens) == 0:
        print '  Invalid 0-length command.'
    else:
        cmd = tokens[0]
        cmd = cmd.lower()
        
        if cmd == 'q' or cmd == 'quit':
        
            print '  Quitting...'
            rv = False
            
        elif cmd == 'h' or cmd == 'help':    

            print ''
            print '  quit/q = quit'
            print '  help/h = help'
            print '  listgroups/lg = list item group names'
            print '  listsubgroups/lsg <group> = list subgroups from a group, prints first group it finds'
            print '  list/l <subgroup> = list items from a subgroup, prints first subgroup it finds'
            print '  listfoundall/lfa <found, optional> = list all unfound items'
            print '  listfoundalleth/lfae <found, optional> = list all unfound eth items'
            print '  listfound/lf <subgroup> <found, optional> = list found items from a subgroup, prints first subgroup it finds'
            print '  listfound/lfe <subgroup> <found, optional> = list found eth items from a subgroup, prints first subgroup it finds'
            print '  print/p <name> = print item(s) with that name, prints location in stash'
            print '  markfind/mf <name> <unfound, optional> = mark item as found, prints location in stash'
            print '  markfindeth/mfe <name> <unfound, optional> = mark eth item as found, prints location in stash'
            print '  comment/c <name> = updates comment field for name'
            
        elif cmd == 'lg' or cmd == 'listgroups':
        
            print ''
            for (name, _) in item_groups:
                print '  ' + name
                
        elif cmd == 'lsg' or cmd == 'listsubgroups':
        
            if len(tokens) >= 2:
                grp = tokens[1]
                grp = clean(grp)
                
                found = False
                for (name, group) in item_groups:
                    n = clean(name)
                    if re.search(grp, n):
                        found = True
                        print ''
                        for (sname, _) in group:
                            print '  ' + sname
                        break
                if not found:
                    print '  Group not found...'
            else:
                print '  Not enough arguments, missing group name...'
                
        elif cmd == 'l' or cmd == 'list':
        
            if len(tokens) >= 2:
                grp = tokens[1]
                grp = clean(grp)
                
                found = False
                for (_, group) in item_groups:
                    for (name, subgroup) in group:
                        n = clean(name)
                        if re.search(grp, n):
                            print ''
                            print name
                            found = True
                            for item in subgroup:
                                printItem(item, PRINT_SHORT)
                            break
                    if found:
                        break
                if not found:
                    print '  Subgroup not found...'
            else:
                print '  Not enough arguments, missing subgroup name...'

        elif cmd == 'lfa' or cmd == 'listfoundall':

            unfound = True
            if len(tokens) >= 2:
                found = tokens[1].lower()
                unfound = found != 'found'
            
            for (_, group) in item_groups:
                for (gname, subgroup) in group:
                    items = []
                    for item in subgroup:
                        if unfound and item[ETH] != ETH_ETH_ONLY and not item[FOUND]:
                            items.append(item)
                        elif unfound and item[ETH] == ETH_ETH_ONLY and not item[FOUND_ETH]:
                            items.append(item)
                        elif not unfound and item[ETH] != ETH_ETH_ONLY and item[FOUND]:
                            items.append(item)
                        elif not unfound and item[ETH] == ETH_ETH_ONLY and item[FOUND]:
                            items.append(item)
                    if len(items):
                        print gname
                        for item in items:
                            printItem(item, PRINT_SHORT_NO_FOUND)

            print ''
            if unfound:
                print '  Total: ' + str(itemsLeft) + ' / ' + str(itemCt)
            else:
                print '  Total: ' + str(itemCt - itemsLeft) + ' / ' + str(itemCt)
            
        elif cmd == 'lfae' or cmd == 'listfoundalleth':

            unfound = True
            if len(tokens) >= 2:
                found = tokens[1].lower()
                unfound = found != 'found'
                
            for (_, group) in item_groups:
                for (gname, subgroup) in group:
                    
                    items = []                    
                    for item in subgroup:
                        if unfound and item[ETH] == ETH_BOTH and not item[FOUND_ETH]:
                            items.append(item)
                        elif not unfound and item[ETH] == ETH_BOTH and item[FOUND_ETH]:
                            items.append(item)
                    if len(items):
                        print gname
                        for item in items:
                            printItem(item, PRINT_SHORT_NO_FOUND, True)
                            
            print ''
            if unfound:
                print '  Total: ' + str(itemsLeftEth) + ' / ' + str(itemCtEth)
            else:
                print '  Total: ' + str(itemCtEth - itemsLeftEth) + ' / ' + str(itemCtEth)
            
        elif cmd == 'lf' or cmd == 'listfound':
        
            if len(tokens) >= 2:
            
                unfound = True
                if len(tokens) >= 3:
                    found = tokens[2].lower()
                    unfound = found != 'found'
            
                grp = tokens[1]
                grp = clean(grp)
                
                hit = False
                ct = 0
                for (_, group) in item_groups:
                    for (name, subgroup) in group:
                        n = clean(name)
                        if re.search(grp, n):
                            print ''
                            print name
                            hit = True
                            for item in subgroup:
                                if unfound:
                                    if not item[FOUND] or (item[ETH] == ETH_ETH_ONLY and not item[FOUND_ETH]):
                                        printItem(item, PRINT_SHORT_NO_FOUND)
                                        ct += 1
                                else:
                                    if item[FOUND] or (item[ETH] == ETH_ETH_ONLY and item[FOUND_ETH]):
                                        printItem(item, PRINT_SHORT_NO_FOUND)
                                        ct += 1
                            break
                    if hit:
                        break
                if not hit:
                    print '  Subgroup not found...'
                else:
                    print ''
                    if unfound:
                        print '  Reg items left to find: ' + str(ct)
                    else:
                        print '  Reg items found: ' + str(ct)
            else:
                print '  Not enough arguments, missing subgroup name...'
                
        elif cmd == 'lfe' or cmd == 'listfoundeth':
        
            if len(tokens) >= 2:
                grp = tokens[1]
                grp = clean(grp)
                
                unfound = True
                if len(tokens) >= 3:
                    found = tokens[2].lower()
                    unfound = found != 'found'
                
                hit = False
                ct = 0
                for (_, group) in item_groups:
                    for (name, subgroup) in group:
                        n = clean(name)
                        if re.search(grp, n):
                            print ''
                            print name
                            hit = True
                            for item in subgroup:
                                if unfound:
                                    if item[ETH] == ETH_BOTH and not item[FOUND_ETH]:
                                        printItem(item, PRINT_SHORT_NO_FOUND, True)
                                        ct += 1
                                else:
                                    if item[ETH] == ETH_BOTH and item[FOUND_ETH]:
                                        printItem(item, PRINT_SHORT_NO_FOUND, True)
                                        ct += 1
                            break
                    if hit:
                        break
                if not hit:
                    print '  Subgroup not found...'
                else:
                    print ''
                    if unfound:
                        print '  Eth items left to find: ' + str(ct)
                    else:
                        print '  Eth items found: ' + str(ct)
            else:
                print '  Not enough arguments, missing subgroup name...'
                
        elif cmd == 'p' or cmd == 'print':
        
            if len(tokens) >= 2:
                name = tokens[1]                
                res = searchItems(name)
                
                if len(res) == 1:
                    printItem(res[0])
                elif len(res) == 0:
                    print '  No items found...'
                else:
                    for i in res:
                        printItem(i, PRINT_SHORT)
            else:
                print '  Not enough arguments, missing item name...'
                
        elif cmd == 'mf' or cmd == 'markfind':
        
            if len(tokens) >= 2:
                name = tokens[1]                
                res = searchItems(name)
                
                markFound = True
                if len(tokens) >= 3:
                    markFound = tokens[2].lower()
                    markFound = markFound != 'unfound'
                
                if len(res) == 1:
                    item = res[0]
                    eth = item[ETH]
                    if eth == ETH_ETH_ONLY:
                        print '  Cannot mark non-eth item for eth only item...'
                    else:
                        if item[FOUND] == markFound:
                            printItem(item, PRINT_SHORT_NO_FOUND)
                            print ''
                            if markFound:
                                print '  Already marked as found...'
                            else:
                                print '  Already marked as unfound...'
                        else:
                            if markFound:
                                itemsLeft -= 1
                            else:
                                itemsLeft += 1
                            item[FOUND] = markFound
                            printItem(item, PRINT_SHORT_NO_FOUND)
                            print ''
                            print '  Updated...  Items Left: ' + str(itemsLeft)
                elif len(res) == 0:
                    print '  No item found...'
                else:
                    num = min(len(res), 10)
                    for i in range(num):
                        printItem(res[i], PRINT_SHORT_NO_FOUND)
                    if num < len(res):
                        print '  ...'
                    print ''
                    print '  Narrow search...'
                    
            else:
                print '  Not enough arguments, missing item name...'
                
        elif cmd == 'mfe' or cmd == 'markfindeth':
        
            if len(tokens) >= 2:
                name = tokens[1]                
                res = searchItems(name)
                
                markFound = True
                if len(tokens) >= 3:
                    markFound = tokens[2].lower()
                    markFound = markFound != 'unfound'
                
                if len(res) == 1:
                    item = res[0]
                    eth = item[ETH]
                    if eth == ETH_NORMAL_ONLY:
                        print '  Cannot mark eth item for non-eth only item...'
                    else:
                        if item[FOUND_ETH]:
                            printItem(item, PRINT_SHORT_NO_FOUND, True)
                            print ''
                            if markFound:
                                print '  Already marked as found...'
                            else:
                                print '  Already marked as unfound...'
                        else:
                            if eth == ETH_BOTH:
                                if markFound:
                                    itemsLeftEth -= 1
                                else:
                                    itemsLeftEth += 1
                            else:
                                if markFound:
                                    itemsLeft -= 1
                                else:
                                    itemsLeft += 1
                            item[FOUND_ETH] = True
                            printItem(item, PRINT_SHORT_NO_FOUND, True)
                            print ''
                            print '  Updated...  Items Left (eth): ' + str(itemsLeftEth)
                            
                elif len(res) == 0:
                    print '  No item found...'
                else:
                    num = min(len(res), 10)
                    for i in range(num):
                        printItem(res[i], PRINT_SHORT_NO_FOUND)
                    if num < len(res):
                        print '  ...'
                    print ''
                    print '  Narrow search...'
            else:
                print '  Not enough arguments, missing item name...'
                
        elif cmd == 'c' or cmd == 'comment':
        
            if len(tokens) >= 2:
                name = tokens[1]                
                res = searchItems(name)
                
                if len(res) == 1:
                    item = res[0]
                    
                    comment = ''
                    for i in range(2, len(tokens)):
                        if i == 2:
                            comment += tokens[i]
                        else:
                            comment += ' ' + tokens[i]
                        
                    if comment != '':
                        item[COMMENT] = comment
                        printItem(item)
                        print ''
                        print '  Updated...'
                    else:
                        print '  No comment to update...'
                elif len(res) == 0:
                    print '  no item found...'
                else:
                    num = min(len(res), 10)
                    for i in range(num):
                        printItem(res[i], PRINT_SHORT_NO_FOUND)
                    if num < len(res):
                        print '  ...'
                    print ''
                    print '  Narrow search...'
            else:
                print '  Not enough arguments, missing item name...'
                
        else:
        
            print '  Unhandled command... (h = help, q = quit)'
            
    writefile()
    
    print ''
    return rv
    
d = readfile()
result = True

print ''
print 'Holy Grail Tracking Program'
print ''
print '  Items Left:       ' + str(itemsLeft)
print '  Items Left (eth): ' + str(itemsLeftEth)
print ''

while result:
    cmd = raw_input('>>>  ')
    result = process(cmd)