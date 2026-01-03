#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import sys
import traceback
from argparse import ArgumentParser, RawTextHelpFormatter, SUPPRESS
import urllib.parse
import urllib.request
import m3u8
from collections import OrderedDict
import subprocess


__RET_CODE_SUCCESS = 0
__RET_CODE_UNEXPECTED_FAILURE = 1


class StdoutFilter(logging.Filter):
    """
    Filter LogRecords that should not be logged to stdout.
    """

    def __init__(self, level):
        """
        :param level: the filter threshold. Records with level higher or equal to threshold are filtered.
        :type level: logging level
        """
        super(StdoutFilter, self).__init__()
        self.__level = level

    def filter(self, record):
        """
        Determine if the specified record has to be logged.
        Returns True if the record should be logged, False otherwise.
        :param record: a logging record.
        :type record: logging.LogRecord
        """
        return record.levelno < self.__level


__logger = logging.getLogger('redbull_dl')

__formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

__err_handler = logging.StreamHandler(sys.stderr)
__err_handler.setLevel(logging.ERROR)
__err_handler.setFormatter(__formatter)
__logger.addHandler(__err_handler)

__def_handler = logging.StreamHandler(sys.stdout)
__def_handler.setLevel(logging.DEBUG)
__def_handler.addFilter(StdoutFilter(logging.ERROR))
__def_handler.setFormatter(__formatter)
__logger.addHandler(__def_handler)

__logger.setLevel(logging.INFO)


def main():
    parser = ArgumentParser(description='A tool to download movies from the Red Bull TV.',
                            formatter_class=RawTextHelpFormatter,
                            add_help=False)
    parser.add_argument('-h', '--help', action='help', help='Show this help message.')
    parser.add_argument('--debug', help='Turn debug on.', action='store_true')
    parser.add_argument('--dry-run', help='Show what should be done but don\'t do anything.',
                        action='store_true')
    parser.add_argument('--list-formats', help='Display available formats.', action='store_true')
    parser.add_argument('--video', help='Format of the video stream.', metavar='RESOLUTION')
    parser.add_argument('--audio', help='Format of the audio stream.', metavar='LANGUAGE')
    parser.add_argument('--subtitles', help='Format of the subtitles.', metavar='LANGUAGE')
    parser.add_argument('--output', help='Path where movie will be saved.', metavar='PATH')
    parser.add_argument('--ffmpeg', help='Path of the ffmpeg executable.', metavar='PATH')
    parser.add_argument('ID', help='ID of the movie to download.')

    args = parser.parse_args()
    if args.debug:
        __logger.setLevel('DEBUG')

    base_url = 'https://play.redbull.com/main/v1/rbcom/en/en/personal_computer/http/'
    url = urllib.parse.urljoin(base_url, '{}{}'.format(args.ID, '.m3u8'))
    __logger.debug('m3u8: {}'.format(url))

    playlist = m3u8.load(url)

    medias = {parsed['media'][0]['language']: parsed for parsed in (m3u8.parse('{}'.format(a_media))
                                                                    for a_media in playlist.media)}
    __logger.debug('medias: {}'.format(medias))

    playlists = {parsed['playlists'][0]['stream_info']['resolution']: parsed
                 for parsed in (m3u8.parse('{}'.format(a_pl)) for a_pl in playlist.playlists)}
    __logger.debug('playlists: {}'.format(playlists))

    if args.list_formats:
        print('VIDEO:')
        print('- {}'.format('\n- '.join('{} ({}p)'.format(value, key) for key, value in
                                        OrderedDict(sorted({int(height): '{}x{}'.format(width, height)
                                                            for width, height in (res.split('x')
                                                                                  for res in playlists.keys())}.items(),
                                                           key=lambda x: x[0])).items())))
        print('AUDIO:')
        print('- {}'.format('\n- '.join('{} ({})'.format(value, key) for key, value in
                                        {medias[key]['media'][0]['name']: medias[key]['media'][0]['language']
                                         for key in medias
                                         if 'audio' == medias[key]['media'][0]['type'].lower()}.items())))
        print('SUBTITLES:')
        print('- {}'.format('\n- '.join('{} ({})'.format(value, key) for key, value in
                                        {medias[key]['media'][0]['name']: medias[key]['media'][0]['language']
                                         for key in medias
                                         if 'subtitles' == medias[key]['media'][0]['type'].lower()}.items())))
    else:
        if (None is args.audio) and (None is args.video):
            raise parser.error('Video or audio format is required.')
        if None is args.output:
            raise parser.error('Output path is required.')
        urls = set()
        if None is not args.video:
            v_url = playlists[args.video]['playlists'][0]['uri']
            __logger.debug('video URL : {}'.format(v_url))
            urls.add(v_url)
        if None is not args.audio:
            a_url = medias[args.audio]['media'][0]['uri']
            __logger.debug('audio URL : {}'.format(a_url))
            urls.add(a_url)
        if None is not args.subtitles:
            s_url = medias[args.subtitles]['media'][0]['uri']
            __logger.debug('subtitles URL : {}'.format(s_url))
            urls.add(s_url)
        ffmpeg_exe = args.ffmpeg
        if None is ffmpeg_exe:
            # get ffmpeg from PATH
            ffmpeg_exe = 'ffmpeg'
        command = '{} -i {} -c:v copy -c:a copy -c:s mov_text {}'.format(ffmpeg_exe, ' -i '.join(urls), args.output)
        __logger.debug('ffmpeg command : {}'.format(command))
        __logger.info('Download {} to {}'.format(args.ID, args.output))
        if not args.dry_run:
            subprocess.run(command, shell=True, check=True)


if __name__ == '__main__':
    ret_code = __RET_CODE_SUCCESS
    try:
        main()
    except Exception:  # noqa
        __logger.error(traceback.format_exc())
        ret_code = __RET_CODE_UNEXPECTED_FAILURE
    exit(ret_code)
