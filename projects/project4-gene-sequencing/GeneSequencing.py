#!/usr/bin/python3

from abc import ABC, abstractmethod

from which_pyqt import PYQT_VER

if PYQT_VER == 'PYQT5':
    from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
    from PyQt4.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT6':
    from PyQt6.QtCore import QLineF, QPointF
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import random

# Used to compute the bandwidth for banded version
MAXINDELS = 3
BANDWIDTH = 2 * MAXINDELS + 1

# Used to implement Needleman-Wunsch scoring
MATCH = -3
INDEL = 5
SUB = 1


class Cell:
    def __init__(self, value, prev):
        self.value = value
        self.prev = prev

    def get_value(self):
        return self.value

    def get_prev(self):
        return self.prev

    def set_prev(self, prev):
        self.prev = prev

    def set_value(self, value):
        self.value = value


# 		prev = self.at(i, j).get_prev()
# 		# ins
# 		if prev == -1:
# 			return self.at(i, j-1).get_value() + INDEL
# 		# match
# 		elif prev == 0:
# 			return self.at(i-1, j-1).get_value() + MATCH
# 		# swap
# 		elif prev == 1:
# 			return self.at(i-1, j-1).get_value() + SUB
# 		# del
# 		elif prev == 2:
# 			return self.at(i-1, j).get_value() + INDEL

class Table(ABC):
    def __init__(self, cols, rows):
        self.table = [[Cell(None, None) for i in range(cols)] for j in range(rows)]

    def get_delete(self, i, j):
        return self.at(i - 1, j).get_value() + INDEL

    def get_insert(self, i, j):
        return self.at(i, j - 1).get_value() + INDEL

    def get_match(self, i, j):
        return self.at(i - 1, j - 1).get_value() + MATCH

    def get_swap(self, i, j):
        return self.at(i - 1, j - 1).get_value() + SUB

    def get_alignment(self):
        if self.table[-1][-1] is None:
            return None

        i = len(self.table) - 1
        j = len(self.table[0]) - 1
        instruction_list = []
        prev = self.at(i, j).get_prev()
        while prev is not None:
            instruction_list.insert(0, prev)
            # ins
            if prev == -1:
                j -= 1
            # match or swap
            elif prev == 0 or prev == 1:
                i -= 1
                j -= 1
            # del
            elif prev == 2:
                i -= 1
            prev = self.at(i, j).get_prev()
        return instruction_list

    def set_delete(self, i, j):
        self.at(i, j).set_prev(2)
        self.at(i, j).set_value(self.get_delete(i, j))

    def set_insert(self, i, j):
        self.at(i, j).set_prev(-1)
        self.at(i, j).set_value(self.get_insert(i, j))

    def set_match(self, i, j):
        self.at(i, j).set_prev(0)
        self.at(i, j).set_value(self.get_match(i, j))

    def set_swap(self, i, j):
        self.at(i, j).set_prev(1)
        self.at(i, j).set_value(self.get_swap(i, j))

    def at(self, i, j):
        return self.table[i][j]

    def end(self):
        return self.table[-1][-1]


class TableBanded(Table):
    def __init__(self, cols, rows):
        super().__init__(cols, rows)
        self.length = None

    def get_alignment(self):
        i = len(self.table) - 1
        j = MAXINDELS
        if self.at(i, j) is None:
            return None

        instruction_list = []
        prev = self.at(i, j).get_prev()
        while prev is not None:
            instruction_list.insert(0, prev)
            # ins
            if prev == -1:
                j -= 1
            # match or swap
            elif prev == 0 or prev == 1:
                i -= 1
            # del
            elif prev == 2:
                i -= 1
                j += 1
            prev = self.at(i, j).get_prev()
        return instruction_list

    def set_length(self, length):
        self.length = length

    def get_delete(self, i, j):
        if j == BANDWIDTH - 1:
            return float('inf')
        return self.at(i - 1, j + 1).get_value() + INDEL

    def get_insert(self, i, j):
        if j == 0:
            return float('inf')
        return self.at(i, j - 1).get_value() + INDEL

    def get_match(self, i, j):
        return self.at(i - 1, j).get_value() + MATCH

    def get_swap(self, i, j):
        return self.at(i - 1, j).get_value() + SUB

    def set_delete(self, i, j):
        self.at(i, j).set_prev(2)
        self.at(i, j).set_value(self.get_delete(i, j))

    def set_insert(self, i, j):
        self.at(i, j).set_prev(-1)
        self.at(i, j).set_value(self.get_insert(i, j))

    def set_match(self, i, j):
        self.at(i, j).set_prev(0)
        self.at(i, j).set_value(self.get_match(i, j))

    def set_swap(self, i, j):
        self.at(i, j).set_prev(1)
        self.at(i, j).set_value(self.get_swap(i, j))

    def at(self, i, j):
        return self.table[i][j]

    def end(self):
        i = len(self.table) - 1
        # j = self.length - i
        j = MAXINDELS
        return self.at(i, j)


class GeneSequencing:
    def __init__(self):
        self.MaxCharactersToAlign = None
        self.banded = None

    # This is the method called by the GUI.  _seq1_ and _seq2_ are two sequences to be aligned, _banded_ is a boolean that tells
    # you whether you should compute a banded alignment or full alignment, and _align_length_ tells you
    # how many base pairs to use in computing the alignment

    def align(self, seq1, seq2, banded, align_length):
        self.banded = banded
        self.MaxCharactersToAlign = align_length
        if len(seq1) > align_length:
            seq1 = seq1[:align_length]
        if len(seq2) > align_length:
            seq2 = seq2[:align_length]

        ###################################################################################################
        # your code should replace these three statements and populate the three variables: score, alignment1 and alignment2
        table = None
        rows = None
        cols = None
        if banded:
            rows = len(seq2) + 1
            cols = BANDWIDTH
            if len(seq1) > (BANDWIDTH * rows) or len(seq2) > (BANDWIDTH * len(seq1)) + MAXINDELS:
                return {'align_cost': float('inf'), 'seqi_first100': 'No Alignment Possible.',
                        'seqj_first100': 'No Alignment Possible.'}
            table = TableBanded(cols, rows)
            table.set_length(len(seq1))

        else:
            rows = len(seq2) + 1
            cols = len(seq1) + 1
            table = Table(cols, rows)

        # Go row by row, check if it's a base case and fill it in, then do the other checks if not
        for i in range(rows):
            for j in range(cols):
                if banded:
                    # Base case banded
                    if j > len(seq1) - i + MAXINDELS or j - MAXINDELS + i < 0:
                        table.at(i, j).set_value(float('inf'))
                        continue
                    if i == 0:
                        if j < MAXINDELS:
                            table.at(i, j).set_value(float('inf'))
                        elif j == MAXINDELS:
                            table.at(i, j).set_value(0)
                        else:
                            table.set_insert(i, j)
                        continue
                    if j - MAXINDELS + i == 0:
                        table.set_delete(i, j)
                else:
                    # Base case unrestricted
                    if i == 0 and j == 0:
                        table.at(i, j).set_value(0)
                        continue
                    if i == 0:
                        table.set_insert(i, j)
                        continue
                    elif j == 0:
                        table.set_delete(i, j)
                        continue

                # Check ins, del, swap, match, see which one is lowest
                ins = table.get_insert(i, j)
                delete = table.get_delete(i, j)
                swap = table.get_swap(i, j)
                match = float('inf')
                if banded and j - MAXINDELS + i > 0:
                    if seq1[j - MAXINDELS + i - 1] == seq2[i - 1]:
                        match = table.get_match(i, j)
                else:
                    if seq1[j - 1] == seq2[i - 1]:
                        match = table.get_match(i, j)
                smallest = min(ins, delete, swap, match)
                if ins == smallest:
                    table.set_insert(i, j)
                elif delete == smallest:
                    table.set_delete(i, j)
                elif match == smallest:
                    table.set_match(i, j)
                elif swap == smallest:
                    table.set_swap(i, j)

        score = table.end().get_value()

        # score = random.random() * 100;
        alignment_list = table.get_alignment()
        # if len(alignment_list) > align_length:
        #     alignment_list = alignment_list[:align_length]
        alignment1 = ''
        alignment2 = ''
        pos1 = 0
        pos2 = 0
        for edit in alignment_list:
            # ins
            if edit == -1:
                alignment2 += '-'
                alignment1 += seq1[pos1]
                pos1 += 1
            # match or swap
            elif edit == 0 or edit == 1:
                alignment1 += seq1[pos1]
                alignment2 += seq2[pos2]
                pos1 += 1
                pos2 += 1
            # del
            elif edit == 2:
                alignment2 += seq2[pos2]
                alignment1 += '-'
                pos2 += 1

        # alignment1 = 'abc-easy  DEBUG:({} chars,align_len={}{})'.format(len(seq1), align_length, ',BANDED' if banded else '')
        # alignment2 = 'as-123--  DEBUG:({} chars,align_len={}{})'.format(len(seq2), align_length, ',BANDED' if banded else '')
        ###################################################################################################
        return {'align_cost': score, 'seqi_first100': alignment1[:100], 'seqj_first100': alignment2[:100]}


def loadSequencesFromFile():
    FILENAME = 'genomes.txt'
    raw = open(FILENAME, 'r').readlines()
    sequences = {}

    i = 0
    cur_id = ''
    cur_str = ''
    for liner in raw:
        line = liner.strip()
        if '#' in line:
            if len(cur_id) > 0:
                sequences[i] = (i, cur_id, cur_str)
                cur_id = ''
                cur_str = ''
                i += 1
            parts = line.split('#')
            cur_id = parts[0]
            cur_str += parts[1]
        else:
            cur_str += line
    if len(cur_str) > 0 or len(cur_id) > 0:
        sequences[i] = (i, cur_id, cur_str)
    return sequences


sequences2 = loadSequencesFromFile()
gene = GeneSequencing()
gene.align(sequences2[2][2], sequences2[3][2], True, 5)
