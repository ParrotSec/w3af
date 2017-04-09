# -*- encoding: utf-8 -*-
'''
bloomfilter.py

Copyright 2011 Andres Riancho

This file is part of w3af, w3af.sourceforge.net .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

'''

from core.data.db.disk_set import disk_set


class generic_bloomfilter(object):
    '''
    A simple "interface like" class to define how a bloom filter should look
    like, methods, attributes, etc.
    
    The idea is to give a consistent API to all the other sections of the code
    and allow the use of different bloom filter implementations.
    '''
    def __init__(self, capacity, error_rate=0.01):
        self.capacity = capacity
        self.error_rate = error_rate
    
    def __contains__(self, key):
        raise NotImplementedError()
        
    def __len__(self):
        raise NotImplementedError()
        
    def add(self, key):
        raise NotImplementedError()

class disk_set_filter_wrapper(generic_bloomfilter):
    def __init__(self, capacity, error_rate=0.01):
        generic_bloomfilter.__init__(self, 10**1024, 0.0)
        
        self.ds = disk_set()

    def __contains__(self, key):
        return key in self.ds
        
    def __len__(self):
        return len(self.ds)
        
    def add(self, key):
        return self.ds.add( key )
        
bloomfilter = disk_set_filter_wrapper
scalable_bloomfilter = disk_set_filter_wrapper

class scalable_bloomfilter(disk_set_filter_wrapper):
    SMALL_SET_GROWTH = 2 # slower, but takes up less memory
    LARGE_SET_GROWTH = 4 # faster, but takes up more memory faster

    def __init__(self, initial_capacity=1000, error_rate=0.001,
                 mode=SMALL_SET_GROWTH):
        disk_set_filter_wrapper.__init__(self, 10**1024, 0.0)