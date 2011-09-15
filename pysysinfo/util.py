"""Implements generic utilities for monitoring classes.

"""

import re


__author__ = "Ali Onur Uyar"
__copyright__ = "Copyright 2011, Ali Onur Uyar"
__credits__ = []
__license__ = "GPL"
__version__ = "0.9"
__maintainer__ = "Ali Onur Uyar"
__email__ = "aouyar at gmail.com"
__status__ = "Development"


buffSize = 4096


def parse_value(val, parsebool=False):
    """Parse input string and return int, float or str depending on format.
    
    @param val:       Input string.
    @param parsebool: If True parse yes / no, on / off as boolean.
    @return:          Value of type int, float or str.
        
    """
    if re.match('-{0,1}\d+$',  str(val)):
            return int(val)
    elif re.match('-{0,1}\d*\.\d+$',  str(val)):
        return float(val)
    elif parsebool and re.match('yes|on', str(val), re.IGNORECASE):
        return True
    elif parsebool and re.match('no|off', str(val), re.IGNORECASE):
        return False
    else:
        return val
    

def safe_sum(seq):
    """Returns the sum of a sequence of numbers. Returns 0 for empty sequence 
    and None if any item is None.
    
    @param seq: Sequence of numbers or None.
    
    """
    if None in seq:
        return None
    else:
        return sum(seq)


def socket_read(fp):
    """Buffered read from socket. Reads all data available from socket.
    
    @fp:     File pointer for socket.
    @return: String of characters read from buffer.
    
    """
    response = ''
    oldlen = 0
    newlen = 0
    while True:
        response += fp.read(buffSize)
        newlen = len(response)
        if newlen - oldlen == 0:
            break
        else:
            oldlen = newlen
    return response


class NestedDict(dict):
    """Dictionary class facilitates creation of nested dictionaries.
    
    This works:
        NestedDict d
        d[k1][k2][k3] ... = v
        
    """
    def __getitem__(self, key):
        """x.__getitem__(y) <==> x[y]"""
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            value = self[key] = type(self)()
            return value
        
    def set_nested(self, klist, value):
        """D.set_nested((k1, k2,k3, ...), v) -> D[k1][k2][k3] ... = v"""
        keys = list(klist)
        if len(keys) > 0:
            curr_dict = self
            last_key = keys.pop()
            for key in keys:
                if not curr_dict.has_key(key) or not isinstance(curr_dict[key], 
                                                                NestedDict):
                    curr_dict[key] = type(self)()
                curr_dict = curr_dict[key]
            curr_dict[last_key] = value

    
class SoftwareVersion(tuple):
    """Class for parsing, storing and comparing version strings. 
    
    Version strings must begin with integer numbers separated by dots and may 
    and with any string. The version string is broken down into its components
    and stored as a tuple.All standard operations for tuple class are supported.
    
    """
    def __init__(self, versionstr):
        self._versionstr = versionstr
        
    def __new__(cls, versionstr):
        mobj = re.match('(?P<version>\d+(\.\d+)*)(?P<suffix>.*)$', versionstr)
        if mobj:
            version = [int(i) for i in mobj.groupdict()['version'].split('.')]
            suffix = mobj.groupdict()['suffix'].strip()
            if len(suffix) > 0:
                version.append(suffix)
            return tuple.__new__(cls, version)
        else:
            raise ValueError('Invalid version string format.')
        
    def __str__(self):
        return self._versionstr
