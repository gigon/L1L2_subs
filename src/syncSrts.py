from pysrt import SubRipFile  # https://github.com/byroot/pysrt
from pysrt import SubRipItem
from pysrt import SubRipTime

def isSubMatch(sub, from_t, to_t):
    if ((sub.start <= from_t) & (sub.end >= from_t)) or ((sub.start >= from_t) & (sub.start <= to_t)):
        return True

    if (sub.end <= to_t) & (sub.end >= to_t):
        return True

    return False
    
def matchSubtitle(subtitle, from_t, to_t, lo=0):
    i = lo

    while (i < len(subtitle)):
        if (subtitle[i].start >= to_t):
            break

        if (isSubMatch(subtitle[i], from_t, to_t)):
            if (i+1 < len(subtitle) and isSubMatch(subtitle[i+1], from_t, to_t)):
                return subtitle[i+1], i+1 

            return subtitle[i], i

        i += 1

    return None, i

def trySplitLineByDelim(subs, ind, text, delimiter):
    if (delimiter in text):
        parts = text.rsplit(delimiter, 1)
        subs[ind-1].text = parts[0]
        subs[ind].text = parts[1]
        return True

def trySplitLine(subs, ind, text):
    for delim in ['\n','\t', '.', ';', ',']:
        if (trySplitLineByDelim(subs, ind, text, delim)):
            return True

def syncSrts(subs_L1, subs_L2):
    """Sync subs_L1 by subs_L2 timings and return a SubRipFile.
    """

    out = SubRipFile()   

    j = 0
    last_j = -1
    dupes = 0

    for L2_sub in subs_L2:
        start = L2_sub.start
        end = L2_sub.end
        L1_sub, j = matchSubtitle(subs_L1, start, end, j)

        if L1_sub is None:
            text = L2_sub.text
            print("---- Missing: {}: {}".format(L2_sub.index, L2_sub.text.replace("\n","[[NL]]")))
        else:
            text = L1_sub.text
            if j == last_j:
                dupes = dupes + 1
                #print("---- OOPS. {}: {} - {}".format(L2_sub.index, L2_sub.text.replace("\n",""), L1_sub.text.replace("\n","")))
            last_j = j

        item = SubRipItem(0, start, end, text)
        out.append(item)

    out.clean_indexes()

    fixed = 0
    for i in range(1, len(out)):
        sub1 = out[i-1].text
        sub2 = out[i].text
        if ((sub1 == sub2) and (subs_L2[i-1].text != subs_L2[i].text)):            
            if (trySplitLine(out, i, sub1)):
                fixed = fixed + 1
                i = i + 1
            else:
                print("---- Oy. {}: {} not fixed".format(i, sub1.replace("\n","[[NL]]")))

    return out, dupes, fixed
