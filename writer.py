import sys
import os

class SubtitleWriter:
    """ Writer module for parsers
    """
    def __init__( self, font, fontsize, fillcolor, outlinecolor, outlinewidth,
                  resolution ):
        """ Initializer
        
            Parameters:
                font: Name of the font used for subtitles
                fontsize: Size of the font used for subtitles
                fillcolor: Color to fill the text with
                outlinecolor: Color for the outline of the text
                outlinewidth: Width of the texts' outline
                resolution: Resolution of the movie
        """
        # Template for convert command
        self.convert = (
            "convert -size %(resolution)s xc:none " +
            "-fill %(fillcolor)s -stroke %(strokecolor)s " +
            "-strokewidth %(strokewidth)s -font %(fontname)s " +
            "-pointsize %(fontsize)s +antialias -colors 4 -gravity south "
        ) % {
            "resolution": resolution,
            "fillcolor": fillcolor,
            "strokecolor": outlinecolor,
            "strokewidth": outlinewidth,
            "fontname": font,
            "fontsize": fontsize
        } + "-draw \"text 0,10 '%(subtext)s'\" %(filename)s"

        # Template for xml subtitle item
        self.spunode = (
            "\t<spu start=\"%(starttime)s\" end=\"%(endtime)s\" " +
            "image=\"%(filename)s\" />\n"
        )
        
    def open( self, outfilename ):
        """ Opens a file for xml output

            Parameters:
                outfilename: Name for output file or - for stdout

            Returns:
                True if outputfile was opened and written succesfully,
                False otherwise
        """
        if outfilename == "-":
            self.outfile = sys.stdout
        else:
            try:
                self.outfile = open( outfilename, "w" )
            except:
                return False
        try:
            self.outfile.write( "<subpictures>\n" )
            self.outfile.write( "    <stream>\n" )
        except:
            if self.outfile != sys.stdout:
                self.outfile.close()
            return False
        return True

    def write( self, number, starttime, endtime, text,
               filename="subtitle_%s.png" ):   
        """ Writer function that parsers should call
    
            Parameters:
              number: Running number for the subtitle
              starttime, endtime: start and end time of the subtitle
              text: subtitle's text
              filename: filename for subtitle image

            Returns:
                True if subtitle was written succesfully,
                False otherwise
        """
        # Fill in the templates
        command = self.convert % {
            "subtext": text.replace( "\'", "\\\'" ).replace( "\"", "\\\"" ),
            "filename": filename % number
        }

        node = self.spunode % {
            "starttime": starttime,
            "endtime": endtime,
            "filename": filename % number
        }
        
        print command
        os.system( command )
        try:
            self.outfile.write( node )
        except:
            return False
        return True

    def close( self ):
        """ Finalizer function which closes the output file

            Returns:
                True if output file was written and closed succesfully,
                False otherwise
        """
        try:
            self.outfile.write( "    </stream>\n" )
            self.outfile.write( "</subpictures>\n" )
        except:
            return False
        finally:
            if self.outfile != sys.stdout:
                self.outfile.close()
        return True

