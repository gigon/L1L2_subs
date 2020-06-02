import os    
from chardet import detect

# get file encoding type
def getEncodingType(file):
    with open(file, 'rb') as f:
        rawdata = f.read()
    return detect(rawdata)['encoding']

def makeFileUtf8Bom(srcfile, trgfile):
    from_codec = getEncodingType(srcfile)

    try: 
        with open(srcfile, 'r', encoding=from_codec) as f, open(trgfile, 'w', encoding='utf-8-sig') as e:
            text = f.read() # for small files, for big use chunks
            e.write(text)
    except UnicodeDecodeError:
        print('Decode Error')
    except UnicodeEncodeError:
        print('Encode Error')
