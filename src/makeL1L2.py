import os    

from pysrt import SubRipFile  # https://github.com/byroot/pysrt
from pysrt import SubRipItem
from pysrt import SubRipTime

from textAnalyse import analyzeSubLevel

from fixEncoding import makeFileUtf8Bom
from syncSrts import syncSrts

delta = SubRipTime(milliseconds=500)
encoding = "utf_8"


level_criterias = {
    '1': { 
        'max_CEFR_level': 'A1',         # lines with CEFR level > this will not be hidden
        'max_flesh_kincade_grade': 4,   # lines with fk grade > this will not be hidden
        'max_characters': 30,           # lines with more characters than this will never be hidden
        'max_words': 8,                 # lines with more words than this will never be hidden
    },
    '2': { 
        'max_CEFR_level': 'A2', 
        'max_flesh_kincade_grade': 5,
        'max_characters': 40,
        'max_words': 9,
    },
    '3': { 
        'max_CEFR_level': 'B1', 
        'max_flesh_kincade_grade': 6,
        'max_characters': 50,
        'max_words': 10,
    },
    '4': { 
        'max_CEFR_level': 'B2', 
        'max_flesh_kincade_grade': 7,
        'max_characters': 50,
        'max_words': 11,
    },
    '5': { 
        'max_CEFR_level': 'C1', 
        'max_flesh_kincade_grade': 8,
        'max_characters': 60,
        'max_words': 12,
    },
    '6': { 
        'max_CEFR_level': 'C2', 
        'max_flesh_kincade_grade': 9,
        'max_characters': 70,
        'max_words': 14,
    }
}    

def log(*values):
    print(values)

def joinLines(txtsub1, txtsub2):
    if (len(txtsub1) > 0) & (len(txtsub2) > 0):
        return txtsub1 + '\n' + txtsub2
    else:
        return txtsub1 + txtsub2

# Returns true if line difficulty level of this L2 line is ok for the user
# Checks line num of chars, flesch-kincaid grade level, CEFR level
# Given max levels to check against, disregards max level <= 0 
def isTextNotAboveLevel(level, cefr_level, flesh_kincade_grade, num_words, lineLen):
    level_criteria = level_criterias[level]

    is_readable = True
    if (level_criteria["max_characters"] > 0 and lineLen > level_criteria["max_characters"]):
        is_readable = False
    if (level_criteria["max_words"] > 0 and num_words > level_criteria["max_words"]):
        is_readable = False
    if (level_criteria["max_flesh_kincade_grade"] > 0 and flesh_kincade_grade > level_criteria["max_flesh_kincade_grade"]):
        is_readable = False
    if (level_criteria["max_CEFR_level"] != "" and cefr_level > level_criteria["max_CEFR_level"]):
        is_readable = False

    # log("{} |{}| Chars: {} | words: {} | F-K Grade: {} | CEFR: {} |".format(
    #     "X" if is_readable else "-", 
    #     line.replace("\n", " "), 
    #     len(line), 
    #     str(readability_statistics["num_words"]),
    #     str(flesh_kincade_grade),
    #     cefr_level) 
    # )
    return is_readable

# if the current L2 (i.e. original language) level is not higher than the given level,
# filter the current L1 subtitle - i.e. it will not be displayed
def processSub(sub_L1, sub_L2, levels, outs, removed_lines, show_L2):
    text_L1 = sub_L1.text
    text_L2 = sub_L2.text

    if (text_L2 is not None) and (len(text_L2) > 0):
        cefr_level, flesh_kincade_grade, n_words = analyzeSubLevel(text_L2)
    else:
        flesh_kincade_grade = ""
        cefr_level = ""
        n_words = 0

    for level in levels:
        if (text_L2 is not None) and (len(text_L2) > 0) and isTextNotAboveLevel(level, cefr_level, flesh_kincade_grade, n_words, len(text_L2)):
            removed_lines[level] = removed_lines[level] + 1            
            text = "" if show_L2 == "no" else text_L2
        else:
            text = joinLines(text_L2, text_L1) if show_L2 == "yes" else text_L1

        if len(text) > 0:
            item = SubRipItem(sub_L2.index, sub_L2.start, sub_L2.end, text)
            outs[level].append(item)        

def makeL1L2(L1_srt, L2_srt, out_srt, levels, out_synced_srt, out_L1_utf8bom_srt, out_L2_utf8bom_srt, show_L2, encoding):
    """
    Joins L1_srt and L2_srt subtitles and saves the result to out_srt.
    If out_synced_srt is not empty, saves the synced L1 srt file to that path.
    If out_L1_utf8bom_srt is not empty, saves the L1 srt file converted to utf8-BOM to that path.
    If out_L2_utf8bom_srt is not empty, saves the L2 srt file converted to utf8-BOM to that path.
    """

    log("L1_srt: " + L1_srt)
    log("L2_srt: " + L2_srt)
    log("show_L2: " + show_L2)
    log("encoding: " + encoding)
    log("out_synced_srt: ", out_synced_srt)
    log("out_L1_utf8bom_srt: ", out_L1_utf8bom_srt)
    log("out_L2_utf8bom_srt: ", out_L2_utf8bom_srt)
    log("levels: ", levels)

    # try to decode and save as utf8-bom
    L1_srt_bom = L1_srt + ".utf8bom"
    L2_srt_bom = L2_srt + ".utf8bom"

    makeFileUtf8Bom(L1_srt, L1_srt_bom)
    makeFileUtf8Bom(L2_srt, L2_srt_bom)

    subs_L1_orig = SubRipFile.open(L1_srt_bom)
    subs_L2 = SubRipFile.open(L2_srt_bom)

    subs_L1, dupes, fixed = syncSrts(subs_L1_orig, subs_L2)

    if out_synced_srt:
        subs_L1.save(out_synced_srt, encoding=encoding)
        log("Saved {}. Duplicate lines: {} Fixed: {}".format(out_synced_srt, dupes, fixed))

    outs = {}
    removed_lines = {}
    out_srts = {}
    for level in levels:
        out_srts[level] = out_srt.replace("{{LEVEL}}", level)
        outs[level] = SubRipFile()
        removed_lines[level] = 0

    for i in range(0, len(subs_L2)-1):
        processSub(subs_L1[i], subs_L2[i], levels, outs, removed_lines, show_L2)

    for level in levels:
        summary = "level_criteria: {}. Hidden L1 lines: {} out of {}".format(level_criterias[level], removed_lines[level], len(subs_L2))
        summaryItem = SubRipItem(1, {'milliseconds': 0}, {'milliseconds': 1}, summary)
        outs[level].append(summaryItem)
        outs[level].clean_indexes()        
        outs[level].save(path=out_srts[level], encoding=encoding)
        log("Saved {}. {} ".format(out_srts[level], summary))

    if (out_L1_utf8bom_srt):
        if os.path.isfile(out_L1_utf8bom_srt):
            os.remove(out_L1_utf8bom_srt)
        os.rename(L1_srt_bom, out_L1_utf8bom_srt)
    else:
        os.remove(L1_srt_bom)

    if (out_L2_utf8bom_srt):
        if os.path.isfile(out_L2_utf8bom_srt):
            os.remove(out_L2_utf8bom_srt)
        os.rename(L2_srt_bom, out_L2_utf8bom_srt)
    else:
        os.remove(L2_srt_bom)
