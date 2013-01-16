#   Copyright (C) 2008  Antti Laine <antti.a.laine@tut.fi>
#
#   This file is part of subtitle2spu.
#
#   subtitle2spu is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   subtitle2spu is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with subtitle2spu.  If not, see <http://www.gnu.org/licenses/>.

import sys

# States
READNUMBER = 1
READTIME = 2
READTEXT = 3

def parse( file, writer ):
    state = READNUMBER
    linecount = 0
    lines = ""

    for buf in file:
        if not buf:
            continue
        if state == READNUMBER:
            number = buf.split()[0]
            state = READTIME
            continue
        if state == READTIME:
            starttime = buf.split()[0]
            endtime = buf.split()[2]
            state = READTEXT
            continue
        if state == READTEXT:
            if buf[0] not in ("\n", "\r"):
                linecount += 1
                lines += buf
            else:
                print "Writing subtitle %s" %(number)
                if not writer.write( number, starttime, endtime, lines ):
                    return False
                state = READNUMBER
                linecount = 0
                lines = ""
    return True

