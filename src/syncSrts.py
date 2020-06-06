from pysrt import SubRipFile  # https://github.com/byroot/pysrt
from pysrt import SubRipItem
from pysrt import SubRipTime

from datetime import datetime, date, timedelta

# given two SrtTime objects returns datetime in the middle (based on date.min)
def findMidTime(start, end):
    dstart = datetime.combine(date.min, start.to_time())
    dend = datetime.combine(date.min, end.to_time())
    dmid = dstart + ((dend - dstart) / 2)
    return dmid

def isSubMatch(sub, from_t, to_t):
    if ((sub.start <= from_t) & (sub.end >= from_t)) or ((sub.start >= from_t) & (sub.start <= to_t)):
        return True

    if (sub.end <= to_t) & (sub.end >= to_t):
        return True

    return False
    
def matchSubtitle(subtitle, from_t, to_t, lo=0):
    i = lo
    mid = findMidTime(from_t, to_t)
    minDiff = timedelta.max
    curr_i = -1

    while (i < len(subtitle)):
        mid2 = findMidTime(subtitle[i].start, subtitle[i].end)
        diff = abs(mid2 - mid)
        if diff > minDiff:
            break

        if diff < minDiff:
            curr_i = i
            minDiff = diff

        i += 1

    if curr_i > -1:
        if not isSubMatch(subtitle[curr_i], from_t, to_t):
            curr_i = -1

    return curr_i

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
    subs_L2_out = SubRipFile()

    j = 0
    last_j = -1
    dupes = 0
    L2_ind = -1

    for L2_sub in subs_L2:
        L2_ind = L2_ind + 1
        start = L2_sub.start
        end = L2_sub.end
        j = matchSubtitle(subs_L1, start, end, max(last_j, 0))
        L1_sub = subs_L1[j] if (j > -1) else None

        if L1_sub is None:
            text = L2_sub.text
            print("---- Missing: {}: {}".format(L2_sub.index, L2_sub.text.replace("\n","[[NL]]")))
        else:
            text = L1_sub.text
            
            if j - 1 > last_j and last_j > -1:
                # we skipped a sub in L1_subs
                if isSubMatch(subs_L1[j-1], subs_L2[L2_ind-1].start, subs_L2[L2_ind-1].end):
                    out[len(out)-1].text = out[len(out)-1].text + "\n" + subs_L1[j-1].text
                elif isSubMatch(subs_L1[j-1], start, end):
                    text = subs_L1[j-1].text + "\n" + text
                else:
                    # A sub line in L1 does not match any in L2
                    # We add it to synced L1, and add an empty one to subs L2
                    item = SubRipItem(0, subs_L1[j-1].start, subs_L1[j-1].end, subs_L1[j-1].text)
                    out.append(item)
                    item2 = SubRipItem(0, subs_L1[j-1].start, subs_L1[j-1].end, " ")
                    subs_L2_out.append(item2)

            if j == last_j:
                dupes = dupes + 1
                #print("---- OOPS. {}: {} - {}".format(L2_sub.index, L2_sub.text.replace("\n",""), L1_sub.text.replace("\n","")))
            last_j = j

        item = SubRipItem(0, start, end, text)
        out.append(item)

        item2 = SubRipItem(0, start, end, L2_sub.text)
        subs_L2_out.append(item2)

    out.clean_indexes()
    subs_L2_out.clean_indexes()

    fixed = 0
    for i in range(1, len(out)):
        sub1 = out[i-1].text
        sub2 = out[i].text
        if ((sub1 == sub2) and (subs_L2_out[i-1].text != subs_L2_out[i].text)):            
            if (trySplitLine(out, i, sub1)):
                fixed = fixed + 1
                i = i + 1
            else:
                print("---- Oy. {}: {} not fixed".format(i, sub1.replace("\n","[[NL]]")))

    return out, dupes, fixed, subs_L2_out
