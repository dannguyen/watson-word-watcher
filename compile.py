from foo.project_settings import *
from foo.transcribe import *
import sys
import json

def compile_project(slug):
    tsdata =  compile_timestamped_transcript_files(transcripts_filenames(slug))
    # save to disk
    with open(full_transcript_path(slug), 'w') as f:
        f.write(json.dumps(tsdata, indent=4))
    with open(lines_transcript_path(slug), 'w') as f:
        lines_data = extract_line_level_data(tsdata)
        f.write(json.dumps(lines_data, indent = 4))


if __name__ == '__main__':
    slug = sys.argv[1].strip()
    print("Compiling project at:\n\t", project_dir(slug))
    data = compile_project(slug)
