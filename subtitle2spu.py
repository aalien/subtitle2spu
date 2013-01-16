#!/usr/bin/python
#
#   subtitle2spu.
#   Creates png images and an xml file from subtitles for use with spumux.
#   Copyright (C) 2008  Antti Laine <antti.a.laine@iki.fi>

import os
import sys
import getopt

from writer import SubtitleWriter

def showUsage():
    print """
Usage: subtitle2spu [OPTION] FILE

  --font=FONT\tsubtitle font
\t\t\tdefault is Arial-Bold
\t\t\tconvert -list font for available fonts
  --fill=COLOR\tfill color
\t\t\tdefault is white
  --outline=COLOR\toutline color
\t\t\tdefault is black
\t\t\tconvert -list color for available colors
  --resolution=WIDTHxHEIGHT\tresolution of the movie
\t\t\tdefault is 720x576 (PAL)
  --type=TYPE\tType of the input file
\t\t\tDefault is srt
\t\t\tSupported values: srt

  --help, -h\t\tdisplay this help text
  --version, -v\t\tdisplay version information
"""

def showVersion():
    print """
subtitle2spu 0.2
Copyright (C) 2008 Antti Laine <antti.a.laine@tut.fi>
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY. See COPYING for details.
"""

def main():
    # default values for options
    font = "Arial-Bold"
    fontsize = "28"
    fillcolor = "White"
    outlinecolor = "Black"
    outlinewidth = "2"
    resolution = "720x576"
    type = "srt"
    outputfilename = "-"

    try:
        options, arguments = getopt.getopt(
            sys.argv[1:],
            "hvo:", 
            ["font=", "fill=", "outline=", "resolution=", "type=",
             "output=", "help", "version"]
        )
    except:
        showUsage()
        return 1

    print options
    print arguments

    for option, value in options:
        if option == "--font":
            font = value
        elif option == "--fill":
            fillcolor = value
        elif option == "--outline":
            outlinecolor = value
        elif option == "--resolution":
            resolution = value
        elif option == "--type":
            type = value
        elif option in ("--output", "-o"):
            outputfilename = value
        elif option in ("--help", "-h"):
            showUsage()
            return 0
        elif option in ("--version", "-v"):
            showVersion()
            return 0
        else:
            showUsage()
            return 1

    if len(arguments) == 0:
        inputfilename = "stdin"
        inputfile = sys.stdin
    elif len(arguments) == 1:
        inputfilename = arguments[0]
        try:
            inputfile = open( inputfilename, "r" )
        except:
            print "Failed open %s" %(inputfilename)
            return 1
    else:
        print "Provide exactly ONE input file."
        return 1
    
    if type not in ( "srt" ):
        print "Only Subrip format is supported at the moment."
        return 1
    import parsesrt

    subtitlewriter = SubtitleWriter( font, fontsize, fillcolor, outlinecolor,
                                     outlinewidth, resolution ) 
    if not subtitlewriter.open(outputfilename):
        print "Failed to open %s" %( subtitlewriter.outputfile )
        return 1
    if not parsesrt.parse( inputfile, subtitlewriter ):
        print "Failed to parse %s" %( inputfilename )
    if inputfilename != "stdin":
        inputfile.close()
    if not subtitlewriter.close():
        print "Failed to write to %s after parsing" %( subtitlewriter.outputfile )
        return 1
    return 0

if __name__ == "__main__":
    sys.exit( main() )
