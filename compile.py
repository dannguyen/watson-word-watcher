from foo.project_settings import *
from foo.transcribe import *
import sys
import json

def compile_project(slug):
    tsdata =  compile_timestamped_transcript_files(transcripts_filenames(slug))
    # save to disk
    with open(full_transcript_path(slug), 'w') as f:
        f.write(json.dumps(tsdata, indent=4))
        print("Wrote:\n\t", full_transcript_path(slug))

    with open(lines_transcript_path(slug), 'w') as f:
        lines_data = extract_line_level_data(tsdata)
        f.write(json.dumps(lines_data, indent = 4))
        print("Wrote", len(lines_data), "lines to:\n\t", lines_transcript_path(slug))

    with open(words_transcript_path(slug), 'w') as f:
        wordsdata = extract_word_level_data(tsdata)
        f.write(json.dumps(wordsdata, indent = 4))
        print("Wrote", len(wordsdata), "words to: \n\t", words_transcript_path(slug))


if __name__ == '__main__':
    pslug = sys.argv[1].strip()
    if not does_project_exist(pslug):
        raise NameError(project_dir(pslug) + " does not exist")

    print("Compiling project at:\n\t", project_dir(pslug))
    compile_project(pslug)
