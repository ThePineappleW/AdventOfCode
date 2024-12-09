#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from io import StringIO


# In[2]:


given = "2333133121414131402"


# In[68]:


class Block:
    def __init__(self, id):
        self.id = id

    def free(self):
        return self.id is None

    def can_swap(self, other):
        return self.free() ^ other.free()
    
    def swap(self, other):
        self.id, other.id = other.id, self.id

    def __repr__(self):
        return '.' if self.free() else str(self.id)


# In[284]:


class File:
    def __init__(self, id, length):
        self.id = id
        self.length = length

    def free(self):
        return self.id is None

    def can_swap(self, other):
        # left-associative
        return self.free() and (not other.free()) and (self.length >= other.length)

    def swap(self, other):
        self.id, other.id = other.id, self.id
        d = self.length - other.length
        if d > 0:
            # There is left-over free space. Let's make a new File to account for that.
            self.length -= d
            return File(None, d)

    def can_merge(self, other):
        return self.id == other.id
    
    def merge(self, other):
        return File(self.id, self.length + other.length)

    def __repr__(self):
        return ('.' if self.free() else str(self.id)) * self.length


# In[285]:


def checksum(blocks):
    total = 0
    cur_idx = 0
    for block in blocks:
        for _ in range(block.length):
                total += cur_idx * (block.id or 0)
                cur_idx += 1
    return total


# In[286]:


def build_blocks(diskmap, files=False):
    blocks = []
    cur_id = 0
    free = False
    for item in diskmap:
        if files:
            blocks.append(File(None if free else cur_id, int(item)))
        else:
            for _ in range(int(item)):
                blocks.append(File(None if free else int(cur_id), 1))
        if not free:
            cur_id += 1
        free = not free
    return blocks


# In[287]:


def compact_disk(blocks, verbose=False):
    l, r = 0, len(blocks) - 1 # two pointers
    if verbose:
        print(blocks)
    while l < r:
        lblock = blocks[l]
        rblock = blocks[r]

        if lblock.free():
            if rblock.free():
                r -= 1
                l = 0
            else:
                if lblock.can_swap(rblock):
                    leftover = lblock.swap(rblock)
                    
                    if leftover:
                        if leftover.can_merge(blocks[l + 1]):
                            blocks[l + 1] = leftover.merge(blocks[l + 1])
                        else:
                            blocks.insert(l + 1, leftover)
                    l = 0
                    r -= 1
            
                else:
                    # r is not free, but they can't swap. 
                    if l == r - 1:
                        l = 0
                        r -= 1
                    else:
                        l += 1
            
        elif l == r - 1:
            l = 0
            r -= 1
        else:
            l += 1
        if verbose:
            print(f'[{lblock} {rblock}] :\t', blocks)
    return blocks


# In[288]:


def solve(src: str, files=False, verbose=False):
    if src.endswith('.txt'):
        with open(src, 'r') as f:
            diskmap = f.read().strip()
    else:
        diskmap = src

    return checksum(compact_disk(build_blocks(diskmap, files=files), verbose=verbose))


# In[289]:


solve('input/day8.txt', False)


# In[292]:


solve(given, True)


# In[270]:


print(str(compact_disk(build_blocks(given, True))).replace())


# In[218]:


print(build_blocks(given, False))

