#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import os
import re
import pytz
import sys

from fit2geo import image, fitreader

def main():
	parser = argparse.ArgumentParser(description='Geotag photos from fit file')
	parser.add_argument("--fitfile", "-f", type=str, help="FIT file")
	parser.add_argument("--photo", "-p", type=str, help="Photo file or directory")
	parser.add_argument("--timezone", type=str, help="Photo timezone", default="Europe/Berlin")
	parser.add_argument("--backup", "-b", action="store_true", default=False, help="Backup original file")

	args = parser.parse_args()

	if not os.path.isfile(args.fitfile):
		print("No such file: %s" % args.fitfile)
		sys.exit(1)

	fit = fitreader.FitFileReader(args.fitfile)
	fit.parse()

	if os.path.isfile(args.photo):
		images = [args.photo, ]
	elif os.path.isdir(args.photo):
		images = [os.path.join(args.photo, filename) for filename in os.listdir(args.photo) if re.search(r'\.jpg$', filename, re.IGNORECASE)]
	else:
		print("No such file or directory: %s" % args.image)
		sys.exit(1)
	tz = pytz.timezone(args.timezone)

	for i in images:
		print("%s... \t\t" % i, end='')
		img = image.Image(i)
		if img.has_geotagging():
			print("Has location data")
			continue
		else:
			try:
				ts = img.get_timestamp(tz)
				(lat, lon, alt) = fit.get_position(ts)
				if img.set_geotagging(lat, lon, int(alt), ts, backup=args.backup):
					print("OK")
				else:
					print("Fail")
			except fitreader.TimeStampOutOfRange:
				print("Timestamp not in .fit file")


if __name__ == '__main__':
	main()
