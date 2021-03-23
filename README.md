# fit2geo
Python Script to geotag a collection of pictures with coordinates coming from a [FIT Activity File](https://developer.garmin.com/fit/file-types/activity/).

This tool uses [pexif](https://github.com/bennoleslie/pexif) to extract and modify EXIF data in JPEG files, and [fitdecode](https://github.com/polyvertex/fitdecode) for parsing FIT activity files and extracting locations.

## Usage example:

```
python3 main.py -h                                                                       1 ↵  3.9.2 (fit2geo)    1.70    
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

