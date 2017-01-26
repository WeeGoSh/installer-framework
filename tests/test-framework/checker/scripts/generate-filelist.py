#!/usr/bin/env python
#############################################################################
##
## Copyright (C) 2017 The Qt Company Ltd.
## Contact: https://www.qt.io/licensing/
##
## This file is part of the Qt Installer Framework.
##
## $QT_BEGIN_LICENSE:GPL-EXCEPT$
## Commercial License Usage
## Licensees holding valid commercial Qt licenses may use this file in
## accordance with the commercial license agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and The Qt Company. For licensing terms
## and conditions see https://www.qt.io/terms-conditions. For further
## information use the contact form at https://www.qt.io/contact-us.
##
## GNU General Public License Usage
## Alternatively, this file may be used under the terms of the GNU
## General Public License version 3 as published by the Free Software
## Foundation with exceptions as appearing in the file LICENSE.GPL3-EXCEPT
## included in the packaging of this file. Please review the following
## information to ensure the GNU General Public License requirements will
## be met: https://www.gnu.org/licenses/gpl-3.0.html.
##
## $QT_END_LICENSE$
##
#############################################################################


import optparse, os, sys
from testrunner import files, testrunner

class GenerateException( Exception ):
  def __init__( self, value ):
      self.value = value
  def __str__( self ):
      return repr( self.value )

def relpath( path, prefix ):
    if prefix != None:
        return os.path.relpath( path, prefix )
    else:
        return path;

out = sys.stdout

def walker( prefix, current_dir, children ):
    for c in children:
        child = current_dir + os.sep + c
        if os.path.isdir( child ):
            continue
        fileObj = file( child, 'rb' )
        md5 = files.md5sum( fileObj )
        out.write( "{0}; {1}; {2}\n".format( relpath( child, prefix ), os.path.getsize( child ), md5 ) )

optionParser = optparse.OptionParser(usage="%prog [options] directory", version="%prog 0.1")
optionParser.add_option("-p", "--omit-prefix", dest="prefix", help="make entries relative to this prefix", metavar="PREFIX" )
optionParser.add_option("-o", "--output", dest="output", help="save file list to file (instead of stdout)", metavar="OUTPUT" )
(options, args) = optionParser.parse_args()
     
try:
    directory = args[0]
except IndexError:
    raise GenerateException( "No directory given.")

if options.output != None:
    out = file( options.output, 'wb' )

os.path.walk( directory, walker, options.prefix )
