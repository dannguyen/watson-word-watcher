import sys
from foo import high as high_foo
from foo.project_settings import get_watson_creds, does_project_exist, project_dir

"""
TODO
refactor into separate CLI-subcommands
"""


if __name__ == '__main__':
    pslug = sys.argv[1].strip()
    if not does_project_exist(pslug):
        raise NameError(project_dir(pslug) + " does not exist")
    # transcribes audio
    print("""
    TRANSCRIBING AUDIO
    ====================
    """)
    high_foo.transcribe_audio(pslug, creds=get_watson_creds())
