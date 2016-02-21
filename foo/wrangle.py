import json
from os.path import basename, splitext
from collections import OrderedDict
WORDS_HEADERS = ['text', 'start', 'end', 'confidence',
                 'line_number', 'line_position',
                 'audible_duration', 'pregap',]

LINES_HEADERS = ['line_number', 'start', 'end', 'confidence',
                 'word_count', 'audible_duration', 'text',]

"""
Scripts for wrangling the transcript files
"""


def compile_timestamped_transcript_files(json_filenames):
    """
    `json_filenames` is a list of filepaths with this filename format:
      00900-01000.json
      where the left-number represents the starting time offset and
        the right-number represents the ending time, in seconds

    Each file in this list follows the Watson API standard JSON response

    Returns: a dictionary that is the result of concatenating all the json files
    into one, with "results" pointing to a list of all returned responses.

    To maintain compatibility with Watson's API response, "result_index" key
      is included and is set to 0, i.e. it'd be as if the resulting dictionary
      is the response returned when sending an entire unbroken soundstream to Watson
    """
    compiled_results = []
    compiled_dict = {'results': compiled_results, "result_index": 0}
    filenames = sorted(json_filenames, key=lambda x: int(basename(x).split('-')[0]))
    for fn in filenames:
        start_offset_sec = int(basename(fn).split('-')[0])
        with open(fn) as f:
            data = json.load(f)
            for result in data['results']:
                for x in result.get('word_alternatives'):
                    x['start_time'] += start_offset_sec
                    x['end_time'] += start_offset_sec
                for alt in result.get('alternatives'):
                    for ts in alt['timestamps']:
                        # each timestamp object is a list:
                        # ["hi", 9.93, 10.11]
                        ts[1] += start_offset_sec
                        ts[2] += start_offset_sec
                compiled_results.append(result)
    return compiled_dict




# Much better...

def parse_transcript(data):
    """
    data (dict): as derived from standard Watson API JSON

    returns: two dicts of lists of dicts:
    {
        words: [],
        lines: []
    }


    This is something that can be converted to CSV easily
    {
        'start': 1.00
        'end': 3.00
        'confidence': 0.77
        'words': "Hello world"
        'pregap': 0.5,
        'postgap': 1.2
    }
    """
    lines = []
    words = []
    prev_line_end = 0
    line_results = data['results']
    for linenum, result in enumerate(line_results): # each result is a  line
        if result.get('alternatives'): # each result may have many alternatives
            # just pick best alternative
            lineobj = result.get('alternatives')[0]
            # each line has timestamps per word
            # filter out the HESITATIONs
            word_timestamps = [o for o in lineobj['timestamps'] if o[0] != '%HESITATION']
            if word_timestamps: # for some reason, timestamps can be empty in some cases
                linewords = []
                # confidence value per word is stored in its own list
                word_confidences = [o for o in lineobj['word_confidence'] if o[0] != '%HESITATION']
                prev_word_end = 0
                for wordpos, txtobj in enumerate(word_timestamps):
                    # we track the word's position in the line so that we can extract the
                    # corresponding word confidence for the current word
                    word = {}
                    word["line_position"] = wordpos
                    word["line_number"] = linenum
                    word['confidence'] =  round(word_confidences[wordpos][1], 3)
                    word["text"] = txtobj[0]
                    word["start"] = txtobj[1]
                    word["end"] = txtobj[2]
                    word["audible_duration"] = round(word["end"] - word["start"], 2)
                    # calculate delay until previous word
                    word["pregap"] = round(word["start"] - prev_word_end, 2)
                    # if word is not last in sentence
                    # if wordpos < len(word_timestamps):
                    #     nextword =  word_timestamps[wordpos]
                    #     word["postgap"] = nextword[0] - word["end"]
                    #     word["total_duration"] = (word["audible_duration"]
                    #                                  + nextword["start"]
                    # set the prev_word_end val to this end
                    prev_word_end = word["end"]
                    linewords.append(word)


                line = {}
                line['line_number'] = linenum
                line['start'] = linewords[0]['start']
                line['end'] = linewords[-1]['end']
                line['text'] = " ".join([w['text'] for w in linewords])
                line['audible_duration'] = round(line['end'] - line['start'], 2)
                line['confidence'] = round(lineobj['confidence'], 3)
                line['word_count'] = len(words)
                # line["pregap"] = line["start"] - prev_line_end
                # # if word is not last in sentence
                # if line['line_number'] == 0:
                #     line["pregap"] = line["start"]
                # elif line['line_number'] < len(line_results):
                #     prevline =  lines[line['line_number'] - 1]
                #     line["pregap"] = line['start'] - prevline['end']
                #     # set the previous line's duration
                #     prevline['postgap'] = line['start'] - prevline['end']
                #     prevline['total_duration'] = prevline['audible_duration'] + prevline['postgap'] + prevline['pregap']


                lines.append(line)
                words.extend(linewords)

    return {'lines': lines, 'words': words}
















def extract_line_level_data(data):
    """
    data (dict): as derived from standard Watson API JSON

    returns: a list of dictionary, each sub-list representing a line:
    {
       "start": 1.42,
       "end": 3.8,
       "confidence": 0.999,
       "words": [
            {
                "text": "Hello",
                "start": 1.42,
                "end": 2.4,
                "confidence": 0.93
            }
       ]
    }
    """
    lines = []
    for result in data['results']:
        if result.get('alternatives'):
            # just pick best alternative
            alt = result.get('alternatives')[0]
            timestamps = alt['timestamps']
            if timestamps: # for some reason, timestamps can be empty in some cases
                words = []
                word_confidences = alt['word_confidence']
                for idx, tobject in enumerate(alt['timestamps']):
                    txt, tstart, tend = tobject
                    word = OrderedDict()
                    word["start"] = tstart
                    word["end"] = tend
                    word['confidence'] = word_confidences[idx][1]
                    word["text"] = txt
                    words.append(word)
                line = OrderedDict()
                line['start'] = words[0]['start']
                line['end'] = words[-1]['end']
                line['confidence'] = alt['confidence']
                line['word_count'] = len(words)
                line['words'] = words
                lines.append(line)

    return lines


## TOO LAZY TO REFACTOR THIS

def extract_word_level_data(data):
    """
    data (dict): as derived from standard Watson API JSON

    returns: a flat list of dictionaries for each word
    [
        {
            "text": "Hello",
            "start": 1.42,
            "end": 2.4,
            "confidence": 0.93
        },
        {
            "text": "World",
            "start": 2.5,
            "end": 3.2,
            "confidence": 0.90
        }

    ]
    """
    words = []
    for result in data['results']:
        if result.get('alternatives'):
            # just pick best alternative
            alt = result.get('alternatives')[0]
            timestamps = alt['timestamps']
            if timestamps: # for some reason, timestamps can be empty in some cases
                word_confidences = alt['word_confidence']
                for idx, tobject in enumerate(alt['timestamps']):
                    txt, tstart, tend = tobject
                    word = OrderedDict()
                    word["start"] = tstart
                    word["end"] = tend
                    word['confidence'] = word_confidences[idx][1]
                    word["text"] = txt
                    words.append(word)
    return words



