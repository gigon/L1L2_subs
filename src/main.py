#!/usr/bin/env python
# -*- coding: utf8 -*-

# Copyright gigon (https://github.com/gigon)

# This script mixes 2 subtitles files in different languages into one file
# where difficult lines are displayed in L1 and easy lines are displayed in L2
# or not at all.
# It can be used to facilitate 2nd language learning through watching movies or series episodes.

import sys
import argparse
import os
import errno

from makeL1L2 import makeL1L2

__description__ = """\
Create subtitles mixing some lines in L1 (your native language) and some lines 
in L2 (the language you want to learn) according to each line difficulty level. 
The program merges two SubRip SRT video subtitles into one.
Targeted at learners of a 2nd language. 

When L1 lines are hidden, display subtitles in L2, or don't display anything at all.
Set the desired level of text according to CEFR level, L1 Flesh-Kincade readability grade, or a mix of both.
Option to display both L1 and L2 subtitles simulataneously.

Example for a learner of ESL (English as 2nd language) who is a native French speaker.
Show the french translation of every line whose:
- CEFR level in english is >= B1 
- Flesh-Kincade grade in english >= 8 (english speakers who finished 8th grade should understand it): 

The program first synchronizes the L1 srt subtitle timings to match the L2 srt subtitles.
Add --save_sync to save the L1 srt and L2 srt with synchronized timings.

Add --L1_color yellow and L1_size 11 to format the L1 subtitles.
Add --L2_color yellow and L2_size 11 to format the L2 subtitles.

$ python ./src/makeL1L2.py "path-to/movie.subs.fr.srt" "path-to/movie.subs.en.srt" --out_srt "path-to/movie.subs.en-B1-fr.srt" --level 3 --save_sync --L2_color yellow

"""

def files_exist(*args):
    """Check if files exists in the file system.
    """
    do_exit = False
    for f in args:
        if not os.path.isfile(f):
            do_exit = True
            print("No such file: '{}'".format(f))

    if do_exit:
        sys.exit(1)

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def main():
    parser = argparse.ArgumentParser(
        description=__description__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("L1_srt", nargs=1, help="SRT file in L1.")
    parser.add_argument("L2_srt", nargs=1, help="SRT file in L2.")
    parser.add_argument("--out_srt", nargs="?", help="output SRT file. Folder will be created if not exists")
    parser.add_argument("--level", default="1,2,3,4,5,6", nargs="?", help="comma separated levels [0-6] to filter by (Will generate one srt for each level). 0 is no-level i.e. L1 will be displayed.")
    parser.add_argument("--show_L2", nargs="?", default="when_no_L1", help="Show L2 subtitles (when_no_L1, no, yes)")
    parser.add_argument("--encoding", nargs="?", default="utf-8-sig", help="Encoding of merged files (default=utf-8-sig)")    
    parser.add_argument("--L1_color", nargs="?", help="L1 subtitles color (yellow, green or #fefefe etc.)")
    parser.add_argument("--L1_size", nargs="?", help="L1 subtitles font size (11, 14 etc.)")
    parser.add_argument("--L2_color", nargs="?", help="L2 subtitles color (yellow, green or #fefefe etc.)")
    parser.add_argument("--L2_size", nargs="?", help="L2 subtitles font size (11, 14 etc.)")
    parser.add_argument("--save_sync", type=str2bool, nargs='?', const=True, default=False, help="save the synced srt files.")
    parser.add_argument("--save_boms", type=str2bool, nargs='?', const=True, default=False, help="save L1 srt fileconverted to utf8-BOM.")

    args = parser.parse_args()

    if args.L1_srt[0] == args.L2_srt[0]:
        print("Passed identical input files")
        sys.exit(1) 

    files_exist(args.L1_srt[0], args.L2_srt[0])
       
    levels = []
    if args.level:
        levels = args.level.split(',')
        for lev in levels:            
            if not lev in ("0", "1", "2", "3", "4", "5", "6"):
                print("Passed invalid level '{}'."
                    " Acceptable values are in the range 0 (none) through 1 (lowest) to 6 (highest).".
                    format(lev))
                sys.exit(1)        
        
    if args.out_srt:
        out_srt = os.path.abspath(args.out_srt[0])
        if len(levels) > 1:
            if not ("{{LEVEL}}" in out_srt):
                out_srt = out_srt.replace(".srt", "-{{LEVEL}}.srt")
    else:
        out_srt = args.L1_srt[0].replace(".srt", "-{{LEVEL}}.srt")

    out_dir = os.path.dirname(out_srt)
    if not os.path.exists(out_dir):
        try:
            os.makedirs(out_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    if args.save_boms:
        out_L1_utf8bom_srt = args.L1_srt[0].replace(".srt", ".utf8bom.srt")
        out_L2_utf8bom_srt = args.L2_srt[0].replace(".srt", ".utf8bom.srt")
    else:
        out_L1_utf8bom_srt = ""
        out_L2_utf8bom_srt = ""

    show_L2 = args.show_L2
    if not show_L2 in ("when_no_L1", "no", "yes"):
        print("Passed invalid show_L2 argument '{}'."
            " Acceptable values are 'when_no_L1', 'no', 'yes'.".
            format(show_L2))
        sys.exit(1)        

    makeL1L2(args.L1_srt[0], args.L2_srt[0], out_srt, levels, args.save_sync,\
        out_L1_utf8bom_srt, out_L2_utf8bom_srt, show_L2, args.encoding,\
        args.L1_color, args.L1_size, args.L2_color, args.L2_size)

if __name__ == '__main__':
    main()
