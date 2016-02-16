from collections import Counter
from foo.project_settings import *
from operator import itemgetter
import sys
import json

if __name__ == '__main__':

    pslug = sys.argv[1]
    if not does_project_exist(pslug):
        raise NameError(project_dir(pslug) + " does not exist")
    with open(words_transcript_path(pslug)) as f:
        words = [w for w in json.load(f)]

    unique_words = Counter(w['text'].lower() for w in words)
    total_duration = words[-1]['end']
    word_count = len(words)
    print()
    print("Total duration:", total_duration)
    print("Total word count:", word_count)
    print("Words/second:", round(word_count/ total_duration, 2))
    print("Total unique words used:", len(unique_words))
    print("Median word confidence:", sorted(words, key=itemgetter('confidence'))[word_count//2]['confidence'])

    longest_words_by_char = sorted(words, key=lambda w: len(w['text']), reverse=True)
    print()
    print("Top 10 longest words by spelling:")
    print("---------------------------------")
    for w in longest_words_by_char[0:10]:
        print(w['text'])

    # longest_words_by_duration = sorted(words, key=lambda w: w['end'] - w['start'], reverse=True)
    # print()
    # print("Top 10 longest words by spoken duration:")
    # print("----------------------------------------")
    # for w in longest_words_by_duration[0:10]:
    #     print(w['text'])

    print()
    print("All words, listed in order of frequency:")
    print("----------------------------------------")
    for i, (w, x) in enumerate(sorted(unique_words.most_common(), key=lambda z: (-z[1], z[0]))):
        print((str(i) + '. ').ljust(4) + w.ljust(30), str(x).rjust(6))
