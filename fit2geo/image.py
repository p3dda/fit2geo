# -*- coding: utf-8 -*-
import datetime
import fractions
import os
import shutil

import piexif


class ImageError(Exception):
	pass


class Image:
	def __init__(self, filename, newfilename=None):
		self.exif = piexif.load(filename)
		self.filename = filename
		if not newfilename:
			self.newfilename = os.path.splitext(filename)[0] + "_orig" + os.path.splitext(filename)[1]
		else:
			self.newfilename = newfilename

	def has_geotagging(self):
		def to_float(rational):
			numerator, denominator = rational
			return numerator / denominator

		def to_deg_decimal(val):
			assert len(val) == 3
			deg, min, sec = val

			deg_dec = to_float(deg) + to_float(min) / 60 + to_float(sec) / 3600
			return deg_dec

		if "GPS" in self.exif and piexif.GPSIFD.GPSLongitude in self.exif["GPS"]:
			if isinstance(self.exif["GPS"][piexif.GPSIFD.GPSLongitude], tuple):
				if to_deg_decimal(self.exif["GPS"][piexif.GPSIFD.GPSLongitude]) != 0 or to_deg_decimal(self.exif["GPS"][piexif.GPSIFD.GPSLatitude]) != 0:
					return True
		return False

	def get_timestamp(self, timezone):
		timestamp = self.exif["Exif"][piexif.ExifIFD.DateTimeOriginal].decode()
		dt = timezone.localize(datetime.datetime.strptime(timestamp, "%Y:%m:%d %H:%M:%S"))
		return dt

	def set_geotagging(self, lat, lon, alt, force=False, backup=False):
		def to_deg(value, loc):
			if value < 0:
				loc_value = loc[0]
			elif value > 0:
				loc_value = loc[1]
			else:
				loc_value = ""
			abs_value = abs(value)
			deg = int(abs_value)
			t1 = (abs_value - deg) * 60
			min = int(t1)
			sec = round((t1 - min) * 60, 5)
			return (deg, min, sec, loc_value)

		def change_to_rational(number):
			"""
			convert a number to rational

			:param number: number
			:return: tuple like (1, 2), (numerator, denominator)
			"""
			f = fractions.Fraction(str(number))
			return (f.numerator, f.denominator)

		if self.has_geotagging() and not force:
			return False

		lat_deg = to_deg(lat, ["S", "N"])
		lng_deg = to_deg(lon, ["W", "E"])
		exiv_lat = (change_to_rational(lat_deg[0]), change_to_rational(lat_deg[1]), change_to_rational(lat_deg[2]))
		exiv_lng = (change_to_rational(lng_deg[0]), change_to_rational(lng_deg[1]), change_to_rational(lng_deg[2]))

		gps_ifd = {
			piexif.GPSIFD.GPSVersionID: (2, 3, 0, 0),
			piexif.GPSIFD.GPSAltitudeRef: 1,
			piexif.GPSIFD.GPSAltitude: change_to_rational(round(alt)),
			piexif.GPSIFD.GPSLatitudeRef: lat_deg[3],
			piexif.GPSIFD.GPSLatitude: exiv_lat,
			piexif.GPSIFD.GPSLongitudeRef: lng_deg[3],
			piexif.GPSIFD.GPSLongitude: exiv_lng,
		}

		self.exif.update(dict(GPS=gps_ifd))
		exif_bytes = piexif.dump(self.exif)

		if backup:
			# make copy of image
			shutil.copy(self.filename, self.newfilename)

		# Add updated geotagging EXIF data
		piexif.insert(exif_bytes, self.filename)
		return True
