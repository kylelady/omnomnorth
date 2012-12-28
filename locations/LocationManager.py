
# Handles all of the locations

import datetime
import os

import LocationInfo
import parse

class LocationManager ():

	location_parser = parse.LocationParser()
	# Map of location groups to a list of locations in that group
	locations = {}

	# Parse all location files and keep track of all locations
	def __init__ (self, directory='.'):

		files = os.listdir(directory)
		for f in files:
			ext = os.path.splitext(f)[1]
			if ext == '.loc':
				li = LocationInfo.LocationInfo()
				self.location_parser.parse(directory + '/' + f, li)

				# Check if we've seen this group, if not add it. Then add the
				#  location to the list.
				group = li.getGroup()
				if group not in self.locations:
					self.locations[group] = []
				self.locations[group].append(li)

	def getStatuses (self):
		out = {}
		now = datetime.datetime.now()
		for group,locs in self.locations.iteritems():
			if group not in out:
				out[group] = []
			for li in locs:
				out[group].append({'name':li.getName(),
					               'status':li.getStatus(now)})
		return out

	def __str__ (self):
		out = ''
		for group,locs in self.locations.iteritems():
			out += group + '\n'
			for li in locs:
				status = li.prettyStatus(li.getStatus(datetime.datetime.now()))
				name   = li.getName()
				out += '  {0}: {1}\n'.format(name, status)

		return out


if __name__ == '__main__':
	lm = LocationManager()
	print lm.getStatuses()

