# MassTextExtractor
Library used for extracting text. It's composed by 2 classes:
* [FieldParser](#FieldParser)
* [TextsParser](#TextsParser)

## FieldParser
Class used for extracting parts from a single text.

### Required fields:
* [text](#text)
* [flags](#flags)
* [flags_regex](#flags_regex)

#### <a name="text"></a>text
Original text to be edited. It's a string.

#### <a name="flags"></a>flags
List flagging elements that are compared against each text line for
filtering purposes. It's a list of strings.

#### <a name="flags_regex"></a>flags_regex
Boolean that indicates if the flagging elements, to be compared, are
regex expressions or normal strings. Default is 'False'.

#### Example:
```
from MassTextExtractor import FieldParser

text = "Line 1.\n Line 2.\n Line a.\n Line b."
flags = ["[0-9]", "a"]
flags_regex = True

new_field = FieldParser(text, flags, flags_regex)
new_field.return_flagged_lines()
>> [('Line 1.', 0), ('Line 2.', 1), ('Line a.', 2)]
```

### Public attributes:
* [switchers](#switchers)
* [breakers](#breakers)
* [droppers](#droppers)
* [shifters](#shifters)

#### <a name="switchers"></a>switchers
List of tuples with switching elements that can be compared against
flagged lines for editing purposes. The first element of the tuple is
the expression to be changed. The second element of the tuple is the
result expression.

##### Example:
```
from MassTextExtractor import FieldParser

text = "Line 1.\n Line 2."
flags = ["1"]

new_field = FieldParser(text, flags)
new_field.switchers = [("Line", "Edited line")]
new_field.switch_field_lines()

new_field.return_flagged_lines()
>> [('Edited line 1.', 0)]
```

#### <a name="breakers"></a>breakers
List of tuples with breaking elements that can be compared against
flagged lines for splitting purposes. The first element of the tuple is
the element for the breaking point(s). The second element of the tuple
is the index of the chunk to be chosen.

##### Example:
```
from MassTextExtractor import FieldParser

text = "Chunk1breakingpointChunk2.\n Line 2.\n Line 3"
flags = ["2"]

new_field = FieldParser(text, flags)
new_field.breakers = [("breakingpoint", 1)]
new_field.break_field_lines()

new_field.return_flagged_lines()
>> [('Chunk2.', 0), ('Line 2.', 1)]
```

#### <a name="droppers"></a>droppers
List of expressions that when found drop that flagged line.

##### Example:
```
from MassTextExtractor import FieldParser

text = "Line 1.\n Bad Line."
flags = ["Line"]

new_field = FieldParser(text, flags)
new_field.droppers = ["Bad"]
new_field.drop_field_lines()

new_field.return_flagged_lines()
>> [('Line 1.', 0)]
```

#### <a name="shifters"></a>shifters
List of tuples with shifting elements that can be compared against
flagged lines for shifting the selected flagged line. The first element
of the tuple is the element to be compared. The second element of the
tuple is the number of lines that flagged line is going to be shifted
(ex: 1 shifts up one line, -1 shifts down one line).

##### Example:
```
from MassTextExtractor import FieldParser

text = "Line 1.\n Line 2.\n Line 3."
flags = ["1"]

new_field = FieldParser(text, flags)
new_field.shifters = [("1", 2)]
new_field.shift_field_lines()

new_field.return_flagged_lines()
>> [('Line 3.', 2)]
```

### Private attributes:

#### <a name="text"></a>text
String where the original text is stored.

#### <a name="flags"></a>flags
List of flagging elements that can be compared against text lines for
filtering purposes.

#### <a name="lines"></a>lines
List of tuples with all the lines from the original text and respective
line positions. The first element of the tuple is the text line. The
second element of the tuple is the line's position from the text.

#### <a name="flagged_lines"></a>flagged_lines
List of tuples of lines, from the text, that where flagged by the
object's flagging methods and respective positions in the text. The
first element of the tuple is the flagged line. The second element of
the tuple is the flagged line's position from the text.

### Public methods:
* [switch_field_lines](#switch_field_lines)
* [break_field_lines](#break_field_lines)
* [drop_field_lines](#drop_field_lines)
* [shift_field_lines](#shift_field_lines)
* [get_sample_lines](#get_sample_lines)
* [get_unflagged_lines](#get_unflagged_lines)
* [match_flagged_lines](#match_flagged_lines)
* [return_flagged_lines](#return_flagged_lines)

#### switch_field_lines
Method for switching the flagged lines by comparing the list of tuples
'switchers' against the list of flagged lines 'flagged_lines' and edit
them. I has an optional argument to indicate if the switchers are regex
expressions.

##### Example:
```
from MassTextExtractor import FieldParser

text = "Line 1.\n Line 2."
flags = ["1"]

new_field = FieldParser(text, flags)
new_field.switchers = [("Line", "Edited line")]
new_field.switch_field_lines()

new_field.return_flagged_lines()
>> [('Edited line 1.', 0)]
```

#### break_field_lines
Method for breaking the flagged lines by comparing the list of tuples
'breakers' against the list of flagged lines 'flagged_lines' and edit
them. I has an optional argument to indicate if the switchers are regex
expressions.

##### Example:
```
from MassTextExtractor import FieldParser

text = "Chunk1breakingpointChunk2.\n Line 2.\n Line 3"
flags = ["2"]

new_field = FieldParser(text, flags)
new_field.breakers = [("breakingpoint", 1)]
new_field.break_field_lines()

new_field.return_flagged_lines()
>> [('Chunk2.', 0), ('Line 2.', 1)]
```

#### drop_field_lines
Method for dropping the flagged lines by comparing the list of tuples
'droppers' against the list of flagged lines 'flagged_lines' and edit
them. I has an optional argument to indicate if the switchers are regex
expressions.

##### Example:
```
from MassTextExtractor import FieldParser

text = "Line 1.\n Bad Line."
flags = ["Line"]

new_field = FieldParser(text, flags)
new_field.droppers = ["Bad"]
new_field.drop_field_lines()

new_field.return_flagged_lines()
>> [('Line 1.', 0)]
```

#### shift_field_lines
Method for shifting the flagged lines by comparing the list of tuples
'shifters' against the list of flagged lines 'flagged_lines' and edit
them. I has an optional argument to indicate if the switchers are regex
expressions.

##### Example:
```
from MassTextExtractor import FieldParser

text = "Line 1.\n Line 2.\n Line 3."
flags = ["1"]

new_field = FieldParser(text, flags)
new_field.shifters = [("1", 2)]
new_field.shift_field_lines()

new_field.return_flagged_lines()
>> [('Line 3.', 2)]
```

#### get_sample_lines
Returns a sample of the original text. It takes 2 optional arguments:
the 'start' element referring to the starting line of the sample and
the 'end' referring to the ending line of the sample (excluding). The
default values for the 'start' and 'end' arguments are 0 and -1 (the
entirety of the original text).

##### Example:
```
from MassTextExtractor import FieldParser

text = "Line 1.\n Line 2.\n Line 3.\n Line 4."
flags = ["1"]

new_field = FieldParser(text, flags)

start = 1
end = 3
new_field.get_sample_lines(start, end)
>> [' Line 2.', ' Line 3.']
```

#### get_unflagged_lines
Returns original text without flagged lines.

##### Example:
```
from MassTextExtractor import FieldParser

text = "Line 1.\n Line 2.\n Line 3.\n Line 4."
flags = ["1"]

new_field = FieldParser(text, flags)

new_field.get_unflagged_lines()
>> [(' Line 2.', 1), (' Line 3.', 2), (' Line 4.', 3)]
```

#### match_flagged_lines
Matches flagged lines against a string element and returns a list of 2
element tuples composed by the field line and corresponding index of
matched/unmatched flagged lines. It takes one argument ('matcher'), and
2 optional arguments ('match' and 'regex'). The 'matcher' argument is
the string that is going to be matched with the flagged lines. The
'match' argument (default: True) is a boolean that when 'True' returns
the flagged lines that match 'matcher' string and when 'False' returns
the flagged lines that don't match 'matcher' string. The 'regex'
(default: False) argument is a boolean that when 'True' assumes the
'matcher' string as a regex expression and when 'False' assumes
'matcher' has a normal expression to be equal or different from flagged
lines.

##### Example:
```
from MassTextExtractor import FieldParser

text = "Line 1.\n Line 2.\n Line a.\n Line b.\n Word."
flags = ["Line"]

new_field = FieldParser(text, flags)

matcher = "[0-9]"
match = False
regex = True
new_field.match_flagged_lines(matcher, match, regex)
>> [('Line a.', 2), ('Line b.', 3)]
```

#### return_flagged_lines
Returns the resulting extracted flagged lines at that point.

#### Example:
```
from MassTextExtractor import FieldParser

text = "Line 1.\n Line 2.\n Line a.\n Line b."
flags = ["[0-9]", "a"]
flags_regex = True

new_field = FieldParser(text, flags, flags_regex)
new_field.return_flagged_lines()
>> [('Line 1.', 0), ('Line 2.', 1), ('Line a.', 2)]
```

### Private methods:

#### get_lines
It parses the original text and returns a list of lines from the text.

#### flag_field_lines
It compares the list of lines against the flags and finds the flagged
field lines. Returns 'False' if nothing is found.

## TextsParser
Subclass of FieldParser for extracting parts from each text from a
group of texts.

### Required fields:
* [file_dirs](#file_dirs)
* [flags](#TextsParserflags)
* [TextsParserflags_regex](#flags_regex)

#### <a name="file_dirs"></a>file_dirs
List of file directories to be parsed by the class.

#### <a name="TextsParserflags"></a>flags
List flagging elements that are compared against each text line for
filtering purposes. It's a list of strings.

#### <a name="TextsParserflags_regex"></a>flags_regex
Boolean that indicates if the flagging elements, to be compared, are
regex expressions or normal strings. Default is 'False'.

#### Example:
```
from MassTextExtractor import TextsParser

file_dirs = ["directory/file01.html", "directory/file02.txt"]
flags = ["[0-9]"]
flags_regex = True
new_field = TextsParser(file_dirs, flags, flags_regex)

new_field.return_texts_field_lines()
>> {'directory/file01.html': [(Line 1, 0), (Line 3, 2)],
    'directory/file02.txt': False}
```

### Private attributes

#### file_dirs
List of file directories to be parsed by the class.

#### texts_field_lines
Dictionary composed by lists of tuples with all the lines from the
original texts and respective line positions. The first element of the
tuple is the text line. The second element of the tuple is the line's
position from the text. The dictionary keys are the file directory for
each parsed text.

### Public methods
* [switch_texts_field_lines](#switch_texts_field_lines)
* [break_texts_field_lines](#break_texts_field_lines)
* [drop_texts_field_lines](#drop_texts_field_lines)
* [shift_texts_field_lines](#shift_texts_field_lines)
* [get_flagged_texts](#get_flagged_texts)
* [save_flagged_texts](#save_flagged_texts)
* [get_unflagged_texts](#get_unflagged_texts)
* [save_unflagged_texts](#save_unflagged_texts)
* [get_texts_unflagged_lines](#get_texts_unflagged_lines)
* [get_unflagged_texts_total](#get_unflagged_texts_total)
* [get_flagged_texts_total](#get_flagged_texts_total)
* [match_texts_flagged_line](#match_texts_flagged_line)
* [match_texts_flagged_lines](#match_texts_flagged_lines)
* [return_texts_field_lines](#return_texts_field_lines)

#### <a name="switch_texts_field_lines"></a>switch_texts_field_lines
Has in 'switch_field_lines' but for each parsed text, and not just one.

#### Example:
```
from MassTextExtractor import TextsParser

file_dirs = ["directory/file01.html", "directory/file02.txt"]
flags = ["[0-9]"]
flags_regex = True
new_field = TextsParser(file_dirs, flags, flags_regex)

new_field.switchers = [("Line", "Edited line")]
new_field.switch_texts_field_lines()

new_field.return_texts_field_lines()
>> {'directory/file01.html': [('Edited line 1.', 0)],
    'directory/file02.txt': False}
```

#### <a name="break_texts_field_lines"></a>break_texts_field_lines
Same has in 'break_field_lines' but for each parsed text, and not just
one.

#### Example:
```
from MassTextExtractor import TextsParser

file_dirs = ["directory/file01.html", "directory/file02.txt"]
flags = ["[0-9]"]
flags_regex = True
new_field = TextsParser(file_dirs, flags, flags_regex)

new_field.breakers = [("breakingpoint", 1)]
new_field.break_texts_field_lines()

new_field.return_texts_field_lines()
>> {'directory/file01.html': [('Chunk2.', 0), ('Line 2.', 1)],
    'directory/file02.txt': False}
```

#### <a name="drop_texts_field_lines"></a>drop_texts_field_lines
Same has in 'drop_field_lines' but for each parsed text, and not just
one.

#### Example:
```
from MassTextExtractor import TextsParser

file_dirs = ["directory/file01.html", "directory/file02.txt"]
flags = ["[0-9]"]
flags_regex = True
new_field = TextsParser(file_dirs, flags, flags_regex)

new_field.droppers = ["Bad"]
new_field.drop_texts_field_lines()

new_field.return_texts_field_lines()
>> {'directory/file01.html': [('Line 1.', 0)],
    'directory/file02.txt': False}
```

#### <a name="shift_texts_field_lines"></a>shift_texts_field_lines
Same has in 'shift_field_lines' but for each parsed text, and not just
one.

#### Example:
```
from MassTextExtractor import TextsParser

file_dirs = ["directory/file01.html", "directory/file02.txt"]
flags = ["[0-9]"]
flags_regex = True
new_field = TextsParser(file_dirs, flags, flags_regex)

new_field.shifters = [("1", 2)]
new_field.shift_texts_field_lines()

new_field.return_texts_field_lines()
>> {'directory/file01.html': [('Line 3.', 2)],
    'directory/file02.txt': False}
```

#### <a name="get_flagged_texts"></a>get_flagged_texts
Returns selected content from flagged texts. It has 2 optional
arguments: 'start' that indicates the beginning of the lines sample
from the flagged texts and 'end' that indicates the ending.

#### Example:
```
from MassTextExtractor import TextsParser

file_dirs = ["directory/file01.html", "directory/file02.txt"]
flags = ["[0-9]"]
flags_regex = True
new_field = TextsParser(file_dirs, flags, flags_regex)

start = 1
end = 3
new_field.get_flagged_texts(start, end)
>> {'directory/flagged_file01.html': [' Line 2.', ' Line 3.'],
    'directory/flagged_file02.txt': [' Line b.', ' Line c.']}
```

#### <a name="save_flagged_texts"></a>save_flagged_texts
Saves into files selected content from each flagged text. It has 3
optional arguments: 'path' (default: './') that indicates the output
directory of the files that are going to be saved; 'line' (default:
'(0, -1)') that refers to the lines interval of the flagged texts that
are going to be saved; and 'txt' that refers to the flagged texts
interval that are going to be saved.

#### Example:
```
from MassTextExtractor import TextsParser

file_dirs = ["directory/file01.html", "directory/file02.txt"]
flags = ["[0-9]"]
flags_regex = True
new_field = TextsParser(file_dirs, flags, flags_regex)

path = 'output_directory/'
line = (3, 5) # (start_line, end_line)
txt = (0, 1) # (start_text, end_text)

new_field.save_flagged_texts(path, line, txt)
```

#### <a name="get_unflagged_texts"></a>get_unflagged_texts
Gets selected content from unflagged texts. It has 2 optional
arguments: 'start' that indicates the beginning of the lines sample
from the unflagged texts and 'end' that indicates the ending.

#### Example:
```
from MassTextExtractor import TextsParser

file_dirs = ["directory/file01.html", "directory/file02.txt"]
flags = ["[0-9]"]
flags_regex = True
new_field = TextsParser(file_dirs, flags, flags_regex)

start = 1
end = 3
new_field.get_unflagged_texts(start, end)
>> {'directory/unflagged_file01.html': [' Line 1.', ' Line 2.'],
    'directory/unflagged_file02.txt': [' Line b.', ' Line c.']}
```

#### <a name="save_unflagged_texts"></a>save_unflagged_texts
Saves into files selected content from each unflagged text. It has 3
optional arguments: 'path' (default: './') that indicates the output
directory of the files that are going to be saved; 'line' (default:
'(0, -1)') that refers to the lines interval of the unflagged texts
that are going to be saved; and 'txt' that refers to the unflagged
texts interval that are going to be saved.

#### Example:
```
from MassTextExtractor import TextsParser

file_dirs = ["directory/file01.html", "directory/file02.txt"]
flags = ["[0-9]"]
flags_regex = True
new_field = TextsParser(file_dirs, flags, flags_regex)

path = 'output_directory/'
line = (3, 5) # (start_line, end_line)
txt = (0, 1) # (start_text, end_text)

new_field.save_unflagged_texts(path, line, txt)
```

#### <a name="get_texts_unflagged_lines"></a>get_texts_unflagged_lines
Same has 'get_unflagged_lines' it returns text without flagged lines,
but from each text.

##### Example:
```
from MassTextExtractor import TextsParser

file_dirs = ["directory/file01.html", "directory/file02.txt"]
flags = ["[0-9]"]
flags_regex = True
new_field = TextsParser(file_dirs, flags, flags_regex)

new_field.get_texts_unflagged_lines()
>> {'directory/file01.html': [(' Line 2.', 1), (' Line 3.', 2)],
    'directory/file02.txt': [(' Line b., 1'), (' Line c.', 2)]}
```

#### <a name="get_unflagged_texts_total"></a>get_unflagged_texts_total
Returns the total number of unflagged texts.

##### Example:
```
from MassTextExtractor import TextsParser

file_dirs = ["directory/file01.html", "directory/file02.txt"]
flags = ["[0-9]"]
flags_regex = True
new_field = TextsParser(file_dirs, flags, flags_regex)

new_field.get_unflagged_texts_total()
>> 1
```

#### <a name="get_flagged_texts_total"></a>get_flagged_texts_total
Returns the total number of flagged texts.

##### Example:
```
from MassTextExtractor import TextsParser

file_dirs = ["directory/file01.html", "directory/file02.txt"]
flags = ["[0-9]"]
flags_regex = True
new_field = TextsParser(file_dirs, flags, flags_regex)

new_field.get_flagged_texts_total()
>> 1
```

#### <a name="match_texts_flagged_line"></a>match_texts_flagged_line
Matches flagged lines against a string element, for each text, and
returns a 2 element tuple composed by the field line and corresponding
index of the first matched/unmatched flagged lines. It takes one
argument ('matcher'), and 2 optional arguments ('match' and 'regex').
The 'matcher' argument is the string that is going to be matched with
the flagged lines. The 'match' argument (default: True) is a boolean
that when 'True' returns the flagged lines that match 'matcher' string
and when 'False' returns the flagged lines that don't match 'matcher'
string. The 'regex' (default: False) argument is a boolean that when
'True' assumes the 'matcher' string as a regex expression and when
'False' assumes 'matcher' has a normal expression to be equal or
different from flagged lines.

##### Example:
```
from MassTextExtractor import TextsParser

file_dirs = ["directory/file01.html", "directory/file02.txt"]
flags = ["Line"]
flags_regex = False
new_field = TextsParser(file_dirs, flags, flags_regex)

matcher = "[0-9]"
match = False
regex = True
new_field.match_texts_flagged_line(matcher, match, regex)
>> {'directory/file01.html': ('Line a.', 2),
    'directory/file02.txt': (' Line b., 1')}
```

#### <a name="match_texts_flagged_lines"></a>match_texts_flagged_lines
Matches flagged lines against a string element, for each text, and
returns a list of 2 element tuples composed by the field line and
corresponding index of matched/unmatched flagged lines. It takes one
argument ('matcher'), and 2 optional arguments ('match' and 'regex').
The 'matcher' argument is the string that is going to be matched with
the flagged lines. The 'match' argument (default: True) is a boolean
that when 'True' returns the flagged lines that match 'matcher' string
and when 'False' returns the flagged lines that don't match 'matcher'
string. The 'regex' (default: False) argument is a boolean that when
'True' assumes the 'matcher' string as a regex expression and when
'False' assumes 'matcher' has a normal expression to be equal or
different from flagged lines.

##### Example:
```
from MassTextExtractor import TextsParser

file_dirs = ["directory/file01.html", "directory/file02.txt"]
flags = ["Line"]
flags_regex = True
new_field = TextsParser(file_dirs, flags, flags_regex)

matcher = "[0-9]"
match = True
regex = True

new_field.match_texts_flagged_lines(matcher, match, regex)
>> {'directory/file01.html': [(' Line 2.', 1), (' Line 3.', 2)],
    'directory/file02.txt': [(' Line 2., 1')]}
```

#### <a name="return_texts_field_lines"></a>return_texts_field_lines
Returns the resulting extracted flagged lines at that point for all the
parsed texts.

#### Example:
```
from MassTextExtractor import TextsParser

file_dirs = ["directory/file01.html", "directory/file02.txt"]
flags = ["[0-9]"]
flags_regex = True
new_field = TextsParser(file_dirs, flags, flags_regex)

new_field.return_texts_field_lines()
>> {'directory/file01.html': [(Line 1, 0), (Line 3, 2)],
    'directory/file02.txt': False}
```

### Private methods

#### get_text
Gets texts from files.

#### flag_texts_field_lines
Gets list of lines from each text.
