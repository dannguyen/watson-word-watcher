from os import makedirs
from os.path import join, basename, splitext, expanduser, abspath, isdir
from glob import glob
from shutil import copyfile
import json


PROJECTS_MAIN_DIR = join(".", "projects")
FULL_AUDIO_BASENAME = 'full-audio.wav'
FULL_VIDEO_BASENAME = 'full-video.mp4'
FULL_TRANSCRIPT_BASENAME = 'full-transcript.json'
LINES_TRANSCRIPT_BASENAME = 'lines-transcript.csv'
WORDS_TRANSCRIPT_BASENAME = 'words-transcript.csv'
WATSON_CREDS_FILENAME = "credsfile_watson.json"

def get_watson_creds(fname=WATSON_CREDS_FILENAME):
    """
    returns a dictionary with username and password as keys
    """
    fullname = abspath(expanduser(fname))
    with open(fullname, 'r') as f:
        data = json.load(f)
        return data['credentials']



def make_slug_from_path(full_path):
    """
    Given a filename, such as "/tmp/heywhat/myvideo.mp4"
    Returns the base filename stripped of its extension,
        e.g. "myvideo"
    """
    return splitext(basename(full_path))[0]


def does_project_exist(slug):
    """
    Yeah....this is probably a good example of why a Project class should be made...
    but hate making oop so much...

    slug refers to a subdirectory in projects/
    Returns True if that subdirectory exists
    """
    return isdir(project_dir(slug))

def init_project_from_video_file(src_path):
    """
    TODO: this should be moved into foo.high

    Given `src_path`, a video filename on the local disk:
        ~/Downloads/myvideo.mp4

    Derive its full path, i.e.
        /Users/Dan/Downloads/myvideo.mp4

    Then create a new projects directory:

        ./projects/myvideo

    And copy the src video to:

        ./projects/myvideo/full-video.mp4

    Note that the projects paths are all relative because I'm too
    lazy to make this object-oriented...

    Returns: project slug, e.g. "myvideo"
    """

    full_src_path = abspath(expanduser(src_path))
    slug = make_slug_from_path(src_path)
    project_dir(slug, make_dir = True)
    b, ext = splitext(src_path)

    if 'mp4' in ext.lower():  # don't bother converting, just copy
        copyfile(full_src_path, full_video_path(slug))
    else:
        from foo.audio_video import convert_to_mp4_file
        convert_to_mp4_file(full_src_path, full_video_path(slug))

    return slug


def project_dir(slug, make_dir = False):
    """
    Creates a subdirectory within the main projects directory
      and returns the path.

    slug: a string representing the name of the project
        e.g. "myvideo"
    returns: the absolute path to the project directory
        e.g. "/Users/yourname/whatever/projects/myvideo"


    Note: sometimes the "slug" will contain projects/ prefix
        e.g. projects/myvideo as opposed to just myvideo

    This function takes the basename of slug, effectively removing
      any prefixed directory name
    """
    xslug = slug.replace("projects/", "").rstrip('/')
    d = join(PROJECTS_MAIN_DIR, xslug)
    d = abspath(expanduser(d))
    # no need to always makedirs here, as all subdirectory calls
    # do their own makedirs call
    if make_dir:
        makedirs(d, exist_ok=True)
    return d

def audio_segments_dir(slug):
    """
    Creates a subdirectory within a given slug subdirectory
      and returns the path.

    slug: a string representing the name of the project
        e.g. "myvideo"
    returns: the absolute path to the project's audio directory
        e.g. "./projects/myvideo/audio-segments
    """
    d = join(project_dir(slug), "audio-segments")
    makedirs(d, exist_ok=True)
    return d

def audio_segments_filenames(slug):
    """
    Assuming that transcripts_dir exists for a given video slug,
    and that it is filled with JSON formatted transcripts,
    this returns a list of globbed JSON files
    """
    return glob(join(audio_segments_dir(slug), '*.wav'))

def supercuts_dir(slug):
    d = join(project_dir(slug), "supercuts")
    makedirs(d, exist_ok=True)
    return d

def transcripts_dir(slug):
    """
    Creates a subdirectory within a given slug subdirectory
      and returns the path.

    slug: a string representing the name of the project
        e.g. "myvideo"
    returns: the absolute path to the project's transcripts dir
        e.g. "./projects/myvideo/transcripts
    """
    d = join(project_dir(slug), "transcripts")
    makedirs(d, exist_ok=True)
    return d

def transcripts_filenames(slug):
    """
    Assuming that transcripts_dir exists for a given video slug,
    and that it is filled with JSON formatted transcripts,
    this returns a list of globbed JSON files
    """
    return glob(join(transcripts_dir(slug), '*.json'))



def full_audio_path(slug):
    """
    Returns the path to the video WAV file that is stored
    in the specific projects directory

    e.g. "./projects/myvideo/full-audio.wav"
    """
    p = join(project_dir(slug), FULL_AUDIO_BASENAME)
    return p


def full_video_path(slug):
    """
    Returns the path to the video MP4 file that is stored
    in the specific projects directory

    e.g. "./projects/myvideo/full-video.mp4"
    """
    p = join(project_dir(slug), FULL_VIDEO_BASENAME)
    return p

def full_transcript_path(slug):
    """
    Returns the path to the JSON file that is the compiled
    version of everything in transcripts_dir(slug)

    e.g. "./projects/myvideo/full-transcript.json"
    """
    p = join(project_dir(slug), FULL_TRANSCRIPT_BASENAME)
    return p



def lines_transcript_path(slug):
    p = join(project_dir(slug), LINES_TRANSCRIPT_BASENAME)
    return p

def words_transcript_path(slug):
    p = join(project_dir(slug), WORDS_TRANSCRIPT_BASENAME)
    return p
