![Build](https://github.com/p3dda/fit2geo/actions/workflows/build_images.yml/badge.svg)
[![Docker Pulls](https://img.shields.io/docker/pulls/p3dda/fit2geo.svg)](https://hub.docker.com/r/p3dda/fit2geo/)

# fit2geo
Python Script to geotag a collection of pictures with coordinates coming from a [FIT Activity File](https://developer.garmin.com/fit/file-types/activity/).

This tool uses [pexif](https://github.com/bennoleslie/pexif) to extract and modify EXIF data in JPEG files, and [fitdecode](https://github.com/polyvertex/fitdecode) for parsing FIT activity files and extracting locations.

## Usage example:

```
python3 main.py --fitfile ./my_garmin_recording.fit --photo ./100MEDIA
```

### Complete usage 
```
python3 main.py -h
usage: main.py [-h] [--fitfile FITFILE] [--photo PHOTO] [--timezone TIMEZONE] [--backup]

Geotag photos from fit file

optional arguments:
  -h, --help            show this help message and exit
  --fitfile FITFILE, -f FITFILE
                        FIT file
  --photo PHOTO, -p PHOTO
                        Photo file or directory
  --timezone TIMEZONE   Photo timezone
  --backup, -b          Backup original file
```

## Docker usage
```
docker run --rm -v ./my_garmin_recording.fit:/activity.fit -v ./100MEDIA:/photos p3dda/fit2geo 
