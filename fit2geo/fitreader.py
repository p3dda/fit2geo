import datetime
import fitdecode


class TimeStampOutOfRange(Exception):
	pass


class FitFileReader:
	def __init__(self, fitfile):
		self.fitfile = fitfile
		self.positions = dict()
		self.parsed = False

	# degrees = semicircles * ( 180 / 2^31 )
	# semicircles = degrees * ( 2^31 / 180 )
	@staticmethod
	def deg(s):
		return s * (180. / (2 ** 31))

	def parse(self):
		with fitdecode.FitReader(self.fitfile) as fit:
			for frame in fit:
				if isinstance(frame, fitdecode.FitDataMessage):
					try:
						timestamp = frame.get_value("timestamp", fit_type="date_time")
						if frame.get_value("position_lat") and frame.get_value("position_long"):
							lat = self.deg(frame.get_value("position_lat"))
							lon = self.deg(frame.get_value("position_long"))
							ts = timestamp.timestamp()
							alt = frame.get_value("altitude", fallback=0)

							self.positions[ts] = (lat, lon, alt)
					except KeyError:
						pass
		self.parsed = True

	def get_position(self, timestamp):
		assert self.parsed
		assert isinstance(timestamp, datetime.datetime)
		ts_list = list(self.positions.keys())
		ts_list.sort()
		timestamp = timestamp.timestamp()
		if timestamp < ts_list[0] or timestamp > ts_list[-1]:
			raise TimeStampOutOfRange
		if timestamp in self.positions:
			return self.positions[timestamp]

		prev_ts = ts = None
		for ts in ts_list:
			if ts < timestamp:
				prev_ts = ts
			else:
				break

		lat = (self.positions[prev_ts][0] + self.positions[ts][0]) / 2
		lon = (self.positions[prev_ts][1] + self.positions[ts][1]) / 2
		alt = (self.positions[prev_ts][2] + self.positions[ts][2]) / 2
		return (lat, lon, alt)
