# redbull_dl
redbull_dl is a tool to download movies from the Red Bull TV.

# Requirements
## System packages
* python3
* ffmpeg
## Python packages
* m3u8

# Usage
```
usage: redbull_dl.py [-h] [--debug] [--dry-run] [--list-formats] [--video RESOLUTION] [--audio LANGUAGE] [--subtitles LANGUAGE] [--output PATH] [--ffmpeg PATH] ID

A tool to download movies from the Red Bull TV.

positional arguments:
  ID                    ID of the movie to download.

options:
  -h, --help            Show this help message and exit.
  --debug               Turn debug on.
  --dry-run             Show what should be done but don't do anything.
  --list-formats        Display available formats.
  --video RESOLUTION    Format of the video stream.
  --audio LANGUAGE      Format of the audio stream.
  --subtitles LANGUAGE  Format of the subtitles.
  --output PATH         Path where movie will be saved.
  --ffmpeg PATH         Path of the ffmpeg executable.
```

# How to retrieve the ID of a movie
* Navigate to the movie web page with your browser and open web developer tools.
* In developer tools, click on Network tab.
* On the web page, click on the "Watch Film" button.
* In the Network tab of the developer tools, search for a m3u8 resource which url starts with 'https://play.redbull.com/main/v1'
* The filename of the resource is the ID of the movie.

## Example
Movie url : https://www.redbull.com/us-en/films/valley-uprising \
Resource url : https://play.redbull.com/main/v1/rbcom/en/us/personal_computer/http/AA-2647XX3851W11.m3u8 \
Movie ID : AA-2647XX3851W11

# Licence
Copyright (C) 2026  Thibault Vataire

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
