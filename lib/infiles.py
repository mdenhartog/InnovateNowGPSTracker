# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Linter
# pylint: disable=E0401,C0103,E1101

""" InnovateNow storage for data on SD cards """

import os

class File(object):
    """ Class for easy reading and writing files """
    
    @staticmethod
    def read(file=None, encoding='UTF-8'):
        """ Read the file at once """
        fh = open(file, mode='r', encoding=encoding)
        data = fh.read()
        fh.close()

        return data

    @staticmethod
    def write(file=None, data=None, encoding='UTF-8'):    
        """ Write the file at once """
        fh = open(file, mode='w', encoding=encoding)
        fh.write(data)
        fh.close()

    @staticmethod
    def delete(file=None):
        """ Delete the specified file """
        if file:
            os.remove(file)
        
class Directory(object):    
    """ Class for directory related actions """

    @staticmethod
    def create(path=None):
        """ Create new directory """
        if path:
            os.mkdir(path)

    @staticmethod
    def exists(path=None):
        """ Check if path exists """
        res = False
        try:
            if path:
                os.chdir(path)
                res = True
        except:
            pass
        
        return res

    @staticmethod
    def delete(path=None):
        """ Delete directory """
        if path:
            os.rmdir(path)
            
    @staticmethod
    def mount(path='/sd'):
        """ Mount a sd card to specified path """
        from machine import SD
        sd = SD()
        os.mount(sd, path)

    @staticmethod
    def unmount(path='/sd'):        
        """ Unmount a sd card from specified path """
        import uos
        uos.unmount(path)