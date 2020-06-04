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
Add --save-sync flag to save this intermediate file.
* Note the two input subtitles times must be close enough for this to succeed.   
If they differ too much, i.e. there is no overlap in may subtitles display times, there will be 
many missing lines in the result.   

Add --encoding flag to save the result in a specific encoding e.g. "--encoding utf8".

## How-to

$ python ./src/main.py "/path-to/movie.subs.fr.srt" "/path-to/movie.subs.en.srt" --level 3 --save_sync

## Notes

* The two srt files are expected to be synchronized betweem them, to the level of 500 ms.   
Otherwise the results are unexpected.   
<b>subsync</b> is a good utility to sync two srt files: ([Online Tool](https://subsync.online/en/online.html))  ([Sources on github](https://github.com/sc0ty/subsync))

* Installation on Windows  
On windows 10, if textacy fails to install, try to install Win10 Sdk

