import json
from os.path import basename, splitext
from collections import OrderedDict

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


# def fetch_transcript_parts(data):
#     """
#     `data` (dictonary):

#     returns:
#     """
