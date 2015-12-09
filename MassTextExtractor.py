# -*- coding: utf-8 -*-


import string                       # to split text into list of lines
import os                           # to create directories
import re                           # to use regex
import itertools                    # to get a subset of dicts
import ntpath                       # to extract filename from path


class FieldParser(object):
    """Field Parser for parsing a string of text. It can:
    - Flag lines of text;
    - Strip parts of text from lines;
    - Break and select chuncks of text from lines."""
    def __init__(self, text, flags, flags_regex = False):
        # original text
        self._text = text
        # List of flaggers
        self._flags = flags
        # list of all the lines from the text
        self._lines = self._get_lines()
        # the detected field lines
        self._flagged_lines = []
        # initialize _flagged_lines
        self._flag_field_lines(flags_regex)

        # list of tuples
        # first element of the tuple is the expression to be changed
        # second element of the tuple is the result expression
        self.switchers = []
        # list of tuples
        # first element of the tuple is the breaking point(s)
        # second element of the tuple is the index of the chunck
        self.breakers = []
        # list of expressions that when found drop that flagged line
        self.droppers = []
        # list of tuples
        # first element of the tuple is the flagger
        # second element of the tuple is the number of lines shifted
        self.shifters = []

    # get list of lines from text
    def _get_lines(self):
        # split text into a list of lines
        unindexed_lines = string.split(self._text, '\n')
        # index all the lines in a list of tuples
        indexed_lines = []
        for index, unindexed_line in enumerate(unindexed_lines):
            indexed_lines.append((unindexed_line, index))
        # return indexed lines
        self._lines = indexed_lines
        return self._lines

    # gets the field lines, returns "False" if not found
    def _flag_field_lines(self, regex = False):
        flagged_lines = []
        # iterate over lines
        for line, index in self._lines:
            stripped_line = line.strip()
            # iterate over field flags
            for flag in self._flags:
                # if field is found add it and it's index to the list
                # also if the field line found isn't repeated
                if regex:
                    found = re.search(flag, line)
                else:
                    found = flag in line
                repeated = (stripped_line, index) in flagged_lines
                if found and not repeated:
                    flagged_lines.append((stripped_line, index))
                else:
                    pass
        # if field lines list isn't empty return it.
        # return "False" otherwise
        if flagged_lines != []:
            self._flagged_lines = flagged_lines
        else:
            self._flagged_lines = False
        return self._flagged_lines

    # strip the lines where the fields where detected
    def switch_field_lines(self, regex = False):
        # update flagged lines by stripping them
        stripped_lines = []
        for line, index in self._flagged_lines:
            for origin, outcome in self.switchers:
                if regex:
                    line = re.sub(origin, outcome, line).strip()
                else:
                    line = line.replace(origin, outcome).strip()
            stripped_lines.append((line, index))
        self._flagged_lines = stripped_lines
        # return flagged field lines
        return self._flagged_lines

    # update flagged lines by splitting them
    def break_field_lines(self, regex = False):
        breaked_lines = []
        for line, line_index in self._flagged_lines:
            line_chunk = line
            for breaking_point, chunk_index in self.breakers:
                if breaking_point in line_chunk:
                    if regex:
                        line_chunks = re.split(breaking_point, line_chunk)
                        line_chunk = line_chunks[chunk_index].strip()
                    else:
                        line_chunks = line_chunk.split(breaking_point)
                        line_chunk = line_chunks[chunk_index].strip()
                else:
                    pass
                    #line_chunk = line
            breaked_lines.append((line_chunk, line_index))
        self._flagged_lines = breaked_lines
        # return flagged field lines
        return self._flagged_lines

    # drops field lines
    def drop_field_lines(self, regex = False):
        # create a shalow copy of the flagged lines list
        # that way self._flagged_lines won't change
        # if undropped_lines is edited
        undropped_lines = self._flagged_lines[:]
        for line, line_index in self._flagged_lines:
            for dropper in self.droppers:

                if regex:
                    found = re.search(dropper, line)
                else:
                    found = dropper in line

                if dropper in line:
                    try:
                        undropped_lines.remove((line, line_index))
                    except:
                        pass
                else:
                    pass
        self._flagged_lines = undropped_lines
        return self._flagged_lines

    # shifts field line from the original place
    def shift_field_lines(self, regex = False):
        shifted_lines = self._flagged_lines[:]
        for line, line_index in self._flagged_lines:
            for shifter, shift_pos in self.shifters:

                if regex:
                    found = re.search(shifter, line)
                else:
                    found = shifter in line

                if found:
                    try:
                        shifted_lines.remove((line, line_index))
                        shifted_line = self._lines[line_index + shift_pos]
                        shifted_content = shifted_line[0].strip()
                        shifted_index = shifted_line[1]
                        shifted_line = (shifted_content, shifted_index)
                        shifted_lines.append(shifted_line)
                    except:
                        print "error: shifted index possibly out of range."
                else:
                    pass
        self._flagged_lines = shifted_lines
        return self._flagged_lines

    # return text lines interval
    def get_sample_lines(self, start = 0, end = -1):
        # get all the lines from the text
        lines = []
        for line, index in self._lines:
            lines.append(line)
        # return the lines from the selected interval
        return lines[start:end]

    # returns text without flagged lines
    def get_unflagged_lines(self):
        text_lines = self._lines[:]
        flags = self._flags
        unflagged_lines = text_lines[:]
        for text_line in text_lines:
            for flag in flags:
                if self.flags_regex:
                    found = re.search(flag, text_line[0])
                else:
                    found = flag in text_line[0]

                if flag in text_line[0]:
                    try:
                        unflagged_lines.remove(text_line)
                    except:
                        pass
                else:
                    pass
        return unflagged_lines

    # finds matching flagged lines and returns their indexes
    # matcher: string to be matched with the flagged lines
    # match (boolean):
    # True - prints flagged lines that match "matcher" string
    # False - prints flagged lines that don't match "matcher" string
    # regex (boolean):
    # True - regex match between the flagged lines and "matcher" str
    # False - check if "matcher" str is the same has flagged lines
    # returns:
    # list with field and index of matched/unmatched flagged lines
    def match_flagged_lines(self, matcher, match = True, regex = False):
        field_index_list = []
        for field_line in self._flagged_lines:
            field = field_line[0]
            field_index = field_line[1]

            if regex:
                found = re.search(matcher, field)
            else:
                found = matcher == field
            #print field + " - " + matcher + " - " + str(found)

            if not match:
                found = not found
            else:
                pass
            #print field + " - " + matcher + " - " + str(found)

            if found:
                field_index_list.append((field, field_index))
            else:
                pass
        return field_index_list

    def return_flagged_lines(self):
        return self._flagged_lines


class TextsParser(FieldParser):
    """Texts Parser for parsing plain text or html files.
    1 - Iterates over an array of file directrories;
    2 - Uses the parent class (FieldParser) tools for parsing."""
    def __init__(self, file_dirs, flags, flags_regex = False):
        text = self._get_text(file_dirs[0])
        FieldParser.__init__(self, text, flags, flags_regex)
        # list of files directories
        self._file_dirs = file_dirs
        # dict with lists of field lines from each text
        # name of file as key
        self._texts_field_lines = self._flag_texts_field_lines()

    # get text from file
    def _get_text(self, file_dir):
        # open the local file
        text_file = open(file_dir)
        # read file's text into a variable
        text = text_file.read()
        # close file
        text_file.close()
        # update file's text
        self._text = text
        # return file's text
        return text

    # get list of lines from each text
    def _flag_texts_field_lines(self):
        texts_field_lines = {}
        for file_dir in self._file_dirs:
            #print file_dir
            self._get_text(file_dir)
            self._get_lines()
            text_field_lines = self._flag_field_lines()
            texts_field_lines[file_dir] = text_field_lines
        return texts_field_lines

    # strips lists of lines from each text
    def switch_texts_field_lines(self, regex = False):
        texts_field_lines = {}
        for file_dir, field_lines in self._texts_field_lines.iteritems():
            self._flagged_lines = field_lines
            if self._flagged_lines != False:
                texts_field_lines[file_dir] = self.switch_field_lines(regex)
            else:
                texts_field_lines[file_dir] = False
        self._texts_field_lines = texts_field_lines
        return self._texts_field_lines

    # splits flagged lines from each text
    def break_texts_field_lines(self, regex = False):
        texts_field_lines = {}
        for file_dir, field_lines in self._texts_field_lines.iteritems():
            self._flagged_lines = field_lines
            if self._flagged_lines != False:
                texts_field_lines[file_dir] = self.break_field_lines(regex)
            else:
                texts_field_lines[file_dir] = False
        self._texts_field_lines = texts_field_lines
        return self._texts_field_lines

    # drops flagged lines from each text
    def drop_texts_field_lines(self, regex = False):
        texts_field_lines = {}
        for file_dir, field_lines in self._texts_field_lines.iteritems():
            self._flagged_lines = field_lines
            if self._flagged_lines != False:
                texts_field_lines[file_dir] = self.drop_field_lines(regex)
            else:
                texts_field_lines[file_dir] = False
        self._texts_field_lines = texts_field_lines
        return self._texts_field_lines

    # shifts flagged lines from each text
    def shift_texts_field_lines(self, regex = False):
        texts_field_lines = {}
        for file_dir, field_lines in self._texts_field_lines.iteritems():
            self._flagged_lines = field_lines
            if self._flagged_lines != False:

                # load new text to find the shifted lines
                self._get_text(file_dir)
                self._get_lines()

                texts_field_lines[file_dir] = self.shift_field_lines(regex)
            else:
                texts_field_lines[file_dir] = False
        self._texts_field_lines = texts_field_lines
        return self._texts_field_lines

    # gets selected content from flagged texts
    def get_flagged_texts(self, start = 0, end = -1):
        flagged_texts = {}
        for file_dir, field_lines in self._texts_field_lines.iteritems():
            if field_lines:
                self._get_text(file_dir)
                self._get_lines()
                sample_lines = self.get_sample_lines(start, end)
                flagged_texts[file_dir] = sample_lines
        return flagged_texts

    # save into files each flagged text
    # path - output directory for the saved files
    # line = interval of lines indexes from each text
    # ex: line = (start_line, end_line)
    # text = interval of flagged texts indexes
    # ex: txt = (start_text, end_text)
    def save_flagged_texts(self, path = "./", line = (0, -1), txt = (0, -1)):
        start_line = line[0]
        end_line = line[1]
        start_text = txt[0]
        end_text = txt[1]
        flagged_texts = self.get_flagged_texts(start_line, end_line)
        texts_subset = dict(itertools.islice(flagged_texts.iteritems(),
                                                start_text, end_text))
        for file_dir, flagged_text in texts_subset.iteritems():
            filename = ntpath.basename(file_dir)
            out_file = open(path + filename, 'w')
            for flagged_line in flagged_text:
                out_file.write(flagged_line + "\n")
            out_file.close()

    # gets selected content from unflagged texts
    def get_unflagged_texts(self, start = 0, end = -1):
        unflagged_texts = {}
        for file_dir, field_lines in self._texts_field_lines.iteritems():
            if not field_lines:
                self._get_text(file_dir)
                self._get_lines()
                sample_lines = self.get_sample_lines(start, end)
                unflagged_texts[file_dir] = sample_lines
        return unflagged_texts

    # save into files each unflagged text
    # path - output directory for the saved files
    # line = interval of lines indexes from each text
    # ex: line = (start_line, end_line)
    # txt = interval of unflagged texts indexes
    # ex: txt = (start_text, end_text)
    def save_unflagged_texts(self, path = "./", line = (0, -1),
                                txt = (0, -1)):
        start_line = line[0]
        end_line = line[1]
        start_text = txt[0]
        end_text = txt[1]
        unflagged_texts = self.get_unflagged_texts(start_line, end_line)
        texts_subset = dict(itertools.islice(unflagged_texts.iteritems(),
                                                start_text, end_text))
        for file_dir, unflagged_text in texts_subset.iteritems():
            filename = ntpath.basename(file_dir)
            #print filename
            #print path + filename
            out_file = open(path + filename, 'w')
            for unflagged_line in unflagged_text:
                #print unflagged_line
                out_file.write(unflagged_line + "\n")
            out_file.close()

    # prints text without flagged lines from each text
    def get_texts_unflagged_lines(self):
        unflagged_lines_texts = {}
        for file_dir in self._file_dirs:
            self._get_text(file_dir)
            self._get_lines()
            unflagged_lines_texts[file_dir] = self.get_unflagged_lines()
        return unflagged_lines_texts

    # gets total number of unflagged texts
    def get_unflagged_texts_total(self):
        texts_total = 0
        for file_dir, text in self._texts_field_lines.iteritems():
            if not text:
                texts_total += 1
        return texts_total

    # gets total number of flagged texts
    def get_flagged_texts_total(self):
        texts_total = 0
        for file_dir, text in self._texts_field_lines.iteritems():
            if text:
                texts_total += 1
        return texts_total

    # prints matched flagged texts first line
    # matcher - string to be matched with the flagged lines
    # match (boolean):
    # True - prints flagged lines that match "matcher" string
    # False - prints flagged lines that don't match "matcher" string
    # regex (boolean):
    # True - regex match between the flagged lines and "matcher" str
    # False - check if "matcher" str is the same has flagged lines
    # returns dict of lists of 2 element tuples:
    # first field and index of (un/)matched flagged line from each text
    # ex:
    # {text_1: (field_1, index_1), text_2: ...}
    def match_texts_flagged_line(self, matcher, match = True, regex = False):
        texts_matched_field = {}
        for file_dir, text_field_lines in self._texts_field_lines.iteritems():
            self._flagged_lines = text_field_lines
            try:
                matched_fields = self.match_flagged_lines(matcher, match,
                                                            regex)
                #print matched_fields
                if matched_fields:
                    texts_matched_field[file_dir] = matched_fields[0]
                else:
                    pass
            except:
                pass
        return texts_matched_field

    # prints matched flagged texts lines
    # matcher - string to be matched with the flagged lines
    # match:
    # True - prints flagged lines that match "matcher" string
    # False - prints flagged lines that don't match "matcher" string
    # regex:
    # True - regex match between the flagged lines and "matcher" str
    # False - check if "matcher" str is the same has flagged lines
    # returns dict of lists of 2 element tuples:
    # list of (un/)matched flagged lines from each text
    # list of tuples with 2 elements: fields and indexes
    # ex:
    # {text_1: [(field_1, index_1), (field_2, index_2)], text_2: ...}
    def match_texts_flagged_lines(self, matcher, match = True, regex = False):
        texts_matched_fields = {}
        for file_dir, text_field_lines in self._texts_field_lines.iteritems():
            self._flagged_lines = text_field_lines
            try:
                matched_fields = self.match_flagged_lines(matcher, match,
                                                            regex)
                #print matched_fields
                if matched_fields:
                    texts_matched_fields[file_dir] = matched_fields
                else:
                    pass
            except:
                pass
        return texts_matched_fields

    def return_texts_field_lines(self):
        return self._texts_field_lines


# main function
if __name__ == "__main__":
    pass
