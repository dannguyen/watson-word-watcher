import sys
from foo import high as high_foo
from foo.project_settings import get_watson_creds

"""
TODO
refactor into separate CLI-subcommands, so that splitting audio
 is done totally separate from transcribing audio, and so forth...
"""


if __name__ == '__main__':
    filepath = sys.argv[1].strip()

    print("""
    INITIALIZING PROJECT
    ====================
    """)
    # initialize project
    project_slug = high_foo.init_project(filepath)

    # extracts and splits audio
    print("""
    SPLITTING AUDIO
    ====================
    """)
    for seg_fn in high_foo.split_audio(project_slug):
        print(seg_fn)

    # transcribes audio
    print("""
    TRANSCRIBING AUDIO
    ====================
    """)
    high_foo.transcribe_audio(project_slug, creds=get_watson_creds())


