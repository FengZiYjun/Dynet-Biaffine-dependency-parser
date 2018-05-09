#!/usr/bin/env python
# -*- coding: UTF-8 -*-
 
# Copyright 2016 Timothy Dozat
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from collections import Counter

import numpy as np

#***************************************************************
class KMeans(object):
  """"""
  
  #=============================================================
  def __init__(self, k, len_cntr):
    """"""
    
    # Error checking
    if len(len_cntr) < k:
      raise ValueError('Trying to sort %d data points into %d buckets' % (len(len_cntr), k))
    
    # Initialize variables
    self._k = k
    self._len_cntr = len_cntr
    self._lengths = sorted(self._len_cntr.keys())
    self._splits = []
    self._split2len_idx = {}
    self._len2split_idx = {}
    self._split_cntr = Counter()
    
    # Initialize the splits evenly
    lengths = []
    for length, count in self._len_cntr.items():
      lengths.extend([length]*count)
    lengths.sort()
    self._splits = [np.max(split) for split in np.array_split(lengths, self._k)]
    
    i = len(self._splits)-1
    while i > 0:
      while self._splits[i-1] >= self._splits[i] or self._splits[i-1] not in self._len_cntr:
      #while self._splits[i-1] >= self._splits[i]:
        self._splits[i-1] -= 1
        # add 2 lines
        if self._splits[i-1] == 1:
            break
        #print(self._splits)
      i -= 1
    
    i = 1
    while i < len(self._splits)-1:
      while self._splits[i] <= self._splits[i-1] or self._splits[i] not in self._len_cntr:
        self._splits[i] += 1
      i += 1
    
    # Reindex everything
    split_idx = 0
    split = self._splits[split_idx]
    for len_idx, length in enumerate(self._lengths):
      count = self._len_cntr[length]
      self._split_cntr[split] += count
      if length == split:
        self._split2len_idx[split] = len_idx
        split_idx += 1
        if split_idx < len(self._splits):
          split = self._splits[split_idx]
          self._split_cntr[split] = 0
      elif length > split:
        raise IndexError()
    
    # Iterate
    old_splits = None
    #print('0) Initial splits: %s; Initial mass: %d' % (self._splits, self.get_mass()))
    i = 0
    while self._splits != old_splits:
      old_splits = list(self._splits)
      self.recenter()
      i += 1
    #print('%d) Final splits: %s; Final mass: %d' % (i, self._splits, self.get_mass()))
    
    self.reindex()
    return
  
  #=============================================================
  def recenter(self):
    """"""
    
    for split_idx in xrange(len(self._splits)):
      split = self._splits[split_idx]
      len_idx = self._split2len_idx[split]
      if split == self._splits[-1]:
        continue
      right_split = self._splits[split_idx + 1]
      
      # Try shifting the centroid to the left
      if len_idx > 0 and self._lengths[len_idx-1] not in self._split_cntr:
        new_split = self._lengths[len_idx - 1]
        left_delta = self._len_cntr[split]*(right_split-new_split) - self._split_cntr[split]*(split-new_split)
        if left_delta < 0:
          self._splits[split_idx] = new_split
          self._split2len_idx[new_split] = len_idx-1
          del self._split2len_idx[split]
          self._split_cntr[split] -= self._len_cntr[split]
          self._split_cntr[right_split] += self._len_cntr[split]
          self._split_cntr[new_split] = self._split_cntr[split]
          del self._split_cntr[split]
      
      # Try shifting the centroid to the right
      elif len_idx < len(self._lengths)-2 and self._lengths[len_idx+1] not in self._split_cntr:
        new_split = self._lengths[len_idx + 1]
        right_delta = self._split_cntr[split]*(new_split-split) - self._len_cntr[split]*(new_split-split)
        if right_delta <= 0:
          self._splits[split_idx] = new_split
          self._split2len_idx[new_split] = len_idx+1
          del self._split2len_idx[split]
          self._split_cntr[split] += self._len_cntr[split]
          self._split_cntr[right_split] -= self._len_cntr[split]
          self._split_cntr[new_split] = self._split_cntr[split]
          del self._split_cntr[split]
    return 
  
  #=============================================================
  def get_mass(self):
    """"""
    
    mass = 0
    split_idx = 0
    split = self._splits[split_idx]
    for len_idx, length in enumerate(self._lengths):
      count = self._len_cntr[length]
      mass += split * count
      if length == split:
        split_idx += 1
        if split_idx < len(self._splits):
          split = self._splits[split_idx]
    return mass
  
  #=============================================================
  def reindex(self):
    """"""
    
    self._len2split_idx = {}
    last_split = -1
    for split_idx, split in enumerate(self._splits):
      self._len2split_idx.update(dict(zip(range(last_split+1, split), [split_idx]*(split-(last_split+1)))))
    return 
  
  #=============================================================
  def __len__(self):
    return self._k
  
  def __iter__(self):
    return (split for split in self.splits)
  
  def __getitem__(self, key):
    return self._splits[key]
  
  #=============================================================
  @property
  def splits(self):
    return self._splits
  @property
  def len2split_idx(self):
    return len2split_idx
  
#***************************************************************
if __name__ == '__main__':
  """"""
  """  
  len_cntr = Counter()
  for i in xrange(10000):
    len_cntr[1+int(10**(1+np.random.randn()))] += 1
  kmeans = KMeans(10, len_cntr)
  """
  cnt = Counter({8: 88, 9: 85, 10: 67, 7: 61, 13: 59, 14: 59, 12: 56, 16: 53, 11: 52, 15: 52, 5: 40, 6: 39, 18: 37, 17: 34, 19: 30,
     20: 30, 23: 24, 24: 23, 22: 22, 21: 20, 25: 20, 26: 14, 4: 13, 27: 13, 30: 11, 28: 9, 34: 8, 36: 5, 3: 4, 29: 4,
     31: 4, 32: 4, 33: 4, 35: 3, 38: 3, 1: 2, 45: 2, 49: 2, 37: 1, 39: 1, 40: 1, 41: 1, 43: 1, 44: 1, 46: 1, 48: 1,
     53: 1, 55: 1, 58: 1, 60: 1})
  k = 40
  cnt2 = Counter({8: 88, 9: 85, 10: 67, 7: 61, 13: 59, 14: 59, 12: 56, 16: 53, 11: 52, 15: 52, 5: 40, 6: 39, 18: 37, 17: 34, 19: 300})
  cnt1 = Counter({1: 10, 2: 4, 3: 5, 4: 4, 5:50, 6:60, 7:70})
  kmeans = KMeans(40, cnt).splits
  print (kmeans)

# i == 13, A[i-1] -=1 leads to neg infinite
 # [5, 5, 6, 7, 7, 8, 8, 8, 8, 9, 9, 9, -31337514, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25, 27, 30, 35, 60]
