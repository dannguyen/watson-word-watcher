from moviepy.editor import VideoFileClip, AudioFileClip
from math import ceil
from os.path import splitext, join
DEFAULT_VIDEO_CODEC = 'libx264' # i.e. mp4
DEFAULT_VIDEO_AUDIO_CODEC = 'libmp3lame' # 'libfdk_aac' doesn't seem to work right now...
DEFAULT_AUDIOFILE_CODEC = 'pcm_s16le' # i.e. wav, 16-bit
DEFAULT_AUDIOFILE_BITRATE = '16k'
DEFAULT_ZEROES_PADDING = 5
DEFAULT_AUDIO_SEGMENT_DURATION_SEC = 300

def convert_to_mp4_file(src_path, dest_path,
                        video_codec=DEFAULT_VIDEO_CODEC,
                        audio_codec=DEFAULT_VIDEO_AUDIO_CODEC):
    """
    Takes an existing movie file and converts it to mp4

    src_path (str): full path to the video file to be copied/processed

    dest_path (str): full path to where the video file should be copied

    video_codec (str): optional string to specify a codec. Otherwise
        all copied videos will be mp4 regardless of extension

    returns: dest_path
    """
    movie = VideoFileClip(src_path)
    movie.write_videofile(dest_path, audio=True,
                          codec=video_codec, audio_codec=audio_codec)
    return dest_path

def extract_audio_file(src_video_path, dest_audio_path,
                  audio_codec=DEFAULT_AUDIOFILE_CODEC,
                  audio_bitrate=DEFAULT_AUDIOFILE_BITRATE):
    """
    Given a video file, extracts the audio into a separate file
    Returns: the path to the extracted audio file

    src_video_path (str): absolute path to source video file

    src_audio_path (str): absolute destination path for audio file

    audio_codec (str): e.g. 'pcm_s16le', the default is 16bit WAV

    audio_bitrate (str): e.g. '16k'
    """

    movie = VideoFileClip(src_video_path)
    audio = movie.audio
    audio.write_audiofile(dest_audio_path,
                codec=audio_codec,bitrate=audio_bitrate)
    return dest_audio_path


def segment_audio_file(src_path, dest_dir,
                  segment_duration=DEFAULT_AUDIO_SEGMENT_DURATION_SEC,
                  zeroes_padding=DEFAULT_ZEROES_PADDING):
    """
    For a given audio file at `src_path`, the audio is segmented
    into chunks of `segment_duration` seconds. Each segment
    is saved in `dest_dir` with a filename convention using
    the start and end time in seconds.


    src_path (str): absolute path to the audio file

    dest_dir (str): absolute path to the subdirectory

    segment_duration (int): the number of seconds for each segment

    zeroes_padding (int): the number of zeroes to pad each segment's filename


    Yields a generator; for each iteration, the path to a
    newly-created audio segment is returned, e.g.

        "./projects/myvideo/audio-segments/00000-00100.wav"
    """
    src_basename, src_ext = splitext(src_path)
    # e.g. for a file, "myvideo/audio.wav", audio_ext is ".wav"
    audio = AudioFileClip(src_path)
    total_seconds = audio.duration
    x_sec = 0
    while x_sec < total_seconds:
        y_sec = x_sec + segment_duration
        if y_sec > total_seconds:
            # when we've reached the end of the total duration
            # round to the next second
            y_sec = ceil(total_seconds)
            # turns out subclip does not like an endpoint bigger
            # than the clip's duration, so we leave off second argument
            segment = audio.subclip(x_sec)
        else:
            segment = audio.subclip(x_sec, y_sec)
        segment_basename = "%s-%s%s" % (
                str(x_sec).rjust(zeroes_padding, "0"),
                str(y_sec).rjust(zeroes_padding, "0"),
                src_ext)
        segment_full_path = join(dest_dir, segment_basename)
        segment.write_audiofile(segment_full_path)
        yield segment_full_path
        # set x_sec to equal y_sec, so that the next clip start at y_sec
        x_sec = y_sec
