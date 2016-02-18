import json
import sys
from foo.project_settings import *



if __name__ == '__main__':
    pslug = sys.argv[1].strip()
    if not does_project_exist(pslug):
        raise NameError(project_dir(pslug) + " does not exist")

    filename = lines_transcript_path(pslug)
    with open(filename, 'r') as t:
        for line in json.loads(t.read()):
            txtline = " ".join([w['text'] for w in line['words']])
            print(txtline)
            print("")

