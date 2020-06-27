# L1L2-subs-maker

Create subtitles mixing some lines in L1 (your native language) and some lines 
in L2 (the language you want to learn) according to each line difficulty level. 
The program merges two SubRip SRT video subtitles into one.   
Targeted at learners of a 2nd language. 

When L1 lines are hidden, display subtitles in L2, or don't display anything at all.   
Select each subtitle line displayed language according to a difficulty measure, 
calculated by L2 CEFR, L2 readability test (Flesh-Kincade), number of words, number of characters. 

Option to display both L1 and L2 subtitles simulataneously, only L1, or L1 and L2 alternately.

The program first attempts to convert the input srt files to UTF-8-BOM format.   
Add --save-boms flag to save these intermediate files.   

The program then attempts to synchronize the 1st input file (L1) subtitle times to the 2nd file (L2).   

## Levels
The levels 1-6 from lowest to highest, are based on CEFR grade and Flesh-Kincade difficulty of each sub line, in addition to number of characters and number of words:       
1: CEFR: A1, FK: 4, max characters: 30, max words: 8
2: CEFR: A2, FK: 5, max characters: 40, max words: 9
3: CEFR: B1, FK: 6, max characters: 50, max words: 11
4: CEFR: B2, FK: 7, max characters: 50, max words: 11
5: CEFR: C1, FK: 8, max characters: 60, max words: 12
6: CEFR: C2, FK: 9, max characters: 70, max words: 14

Set --level 2,4 to generate srts for these levels.   
Set --level 0 to generate an srt for no level i.e. all lines in L1 will be shown (useful e.g. to mix L1 and l2)
The default value is 1,2,3,4,5,6.

Add --L1_color yellow and L1_size 11 to format the L1 subtitles.
Add --L2_color yellow and L2_size 11 to format the L2 subtitles.

Add --save-sync flag to save this intermediate file.
* Note the two input subtitles times must be close enough for this to succeed.   
If they differ too much, i.e. there is no overlap in may subtitles display times, there will be 
many missing lines in the result.   

Add --encoding flag to save the result in a specific encoding e.g. "--encoding utf8".

## How-to

In order to run in a Python virtual environment, install pipenv.   
Run this to get the packages and spacy english data file:
```sh
pipenv install 
pipenv run python -m spacy download en
```
Run the program:
```
$ pipenv run python ./src/main.py "/path-to/movie.subs.fr.srt" "/path-to/movie.subs.en.srt" --level 3,5 --save_sync
```

## Build an installation
```
pipenv run setup.py install
```

## Build win exe with pyinstaller:

Replace file in %appdata%\..\.virtualenvs\L1L2_subs-75Ang_a8\Lib\site-packages\PyInstaller\hooks\hook-nltk.py  
with pyinstaller-hooks-to-replace\hook-nltk.py

Use the following script if you installed pipenv as python virtual envirnment.  
```
./run-pyinstaller.sh
```

## Notes

* The two srt files are expected to be synchronized betweem them, to the level of 500 ms.   
Otherwise the results are unexpected.   
<b>subsync</b> is a good utility to sync two srt files: ([Online Tool](https://subsync.online/en/online.html))  ([Sources on github](https://github.com/sc0ty/subsync))

* Installation on Windows  
On windows 10, if textacy fails to install, try to install Win10 Sdk.   
