from foo.project_settings import *
from foo.audio_video import excerpt_and_compile_video_file
import sys
# import json # DEPRECATED
import csv
import re

MIN_CONFIDENCE = 0.0

"""
TODO
refactor into separate CLI-subcommands
CSV makes for bad numerical data...
"""



if __name__ == '__main__':
    """
    usage:
        python supercut.py republican-debate-sc-2016-02-13 'Obama|Bush'

    Expects: The following routines have already been run:

        python go.py ~/Downloads/republican-debate-sc-2016-02-13.mp4

        python compile.py republican-debate-sc-2016-02-13

    Produces: a movie file in the project's supercuts directory, e.g.

        projects/republican-debate-sc-2016-02-13/supercuts/obama-bush.mp4

    """
    pslug, word_pattern = sys.argv[1:3]
    is_dryrun = True if not sys.argv[-1] == '--produce' else False
    if not does_project_exist(pslug):
        raise NameError(project_dir(pslug) + " does not exist")
    print("Extracting case-insensitive pattern:", word_pattern)
    print("  from project:", pslug)
    print("  with a minimum confidence of:", MIN_CONFIDENCE)
    # create a filename based on the word_pattern
    supercut_slug = re.sub('[^A-z0-9_\.-]+', '-', word_pattern.replace('\\', '')).strip('-').lower()
    supercut_fname = join(supercuts_dir(pslug), supercut_slug + '.mp4')
    re_pattern = re.compile(word_pattern, re.IGNORECASE)
    word_matches = []
    with open(words_transcript_path(pslug)) as f:
        transcribed_words = list(csv.DictReader(f))
        for t_word in transcribed_words:
            if re_pattern.search(t_word['text']) and float(t_word['confidence']) >= MIN_CONFIDENCE:
                word_matches.append(t_word)

    timestamps = []
    for n, word in enumerate(word_matches):
        print("\t", str(n) + ':',  word['text'], word['confidence'], word['start'], word['end'])
        timestamps.append((float(word['start']), float(word['end'])))

    if is_dryrun:
        print("...just a dry run...Use: --produce to create the video file")
    else:
        excerpt_and_compile_video_file(
            src_path=full_video_path(pslug),
            dest_path=supercut_fname,
            timestamps=timestamps
        )

    print("Wrote", len(timestamps), "cuts to:\n\t", supercut_fname)
