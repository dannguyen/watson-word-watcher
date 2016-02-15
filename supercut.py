from foo.project_settings import *
from foo.audio_video import excerpt_and_compile_video_file
import sys
import json
import re

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
    is_dryrun = True if sys.argv[-1] == '--dry-run' else False
    if not does_project_exist(pslug):
        raise NameError(project_dir(pslug) + " does not exist")
    print("Extracting case-insensitive pattern:", word_pattern)
    print("  from project:", pslug)
    # create a filename based on the word_pattern
    supercut_slug = re.sub('[^A-z0-9_\.-]+', '-', word_pattern.replace('\\', '')).strip('-').lower()
    supercut_fname = join(supercuts_dir(pslug), supercut_slug + '.mp4')
    re_pattern = re.compile(word_pattern, re.IGNORECASE)
    word_matches = []
    with open(words_transcript_path(pslug)) as f:
        transcribed_words = json.load(f)
        for t_word in transcribed_words:
            if re_pattern.search(t_word['text']):
                word_matches.append(t_word)

    timestamps = []
    for n, word in enumerate(word_matches):
        print("\t", str(n) + ':',  word['text'], word['start'], word['end'])
        timestamps.append((word['start'], word['end']))

    if is_dryrun:
        print("...just a dry run...")
    else:
        excerpt_and_compile_video_file(
            src_path=full_video_path(pslug),
            dest_path=supercut_fname,
            timestamps=timestamps
        )

    print("Wrote", len(timestamps), "cuts to:\n\t", supercut_fname)
