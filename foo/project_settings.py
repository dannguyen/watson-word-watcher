from os import makedirs
from os.path import join, basename, splitext, expanduser, abspath
from glob import glob
from foo.audio_video import convert_to_mp4_file
from shutil import copyfile
import json


PROJECTS_MAIN_DIR = join(".", "projects")
FULL_AUDIO_BASENAME = 'full-audio.wav'
FULL_VIDEO_BASENAME = 'full-video.mp4'
FULL_TRANSCRIPT_BASENAME = 'full-transcript.json'
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


def init_project_from_video_file(src_path):
    """
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
    b, ext = splitext(src_path)

    if 'mp4' in ext.lower():  # don't bother converting, just copy
        copyfile(full_src_path, full_video_path(slug))
    else:
        convert_to_mp4_file(full_src_path, full_video_path(slug))

    return slug


def project_dir(slug):
    """
    Creates a subdirectory within the main projects directory
      and returns the path.

    slug: a string representing the name of the project
        e.g. "myvideo"
    returns: the absolute path to the project directory
        e.g. "/Users/yourname/whatever/projects/myvideo"
    """
    d = join(PROJECTS_MAIN_DIR, slug)
    d = abspath(expanduser(d))
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
    glob(join(audio_segments_dir(slug), '*.wav'))

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
    glob(join(transcripts_dir(slug), '*.json'))



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

