
# Handles all of the locations

import datetime
import os

import LocationInfo
import parse

class LocationManager ():

	location_parser = parse.LocationParser()
	# Map of location regions to a map of locations groups to a list of
	#  locations in that group.
	locations = {}
	group_order = []

	# Parse all location files and keep track of all locations
	def __init__ (self, directory='.'):
		self.locations = {}

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

		# Load in group order
		with open(directory + '/group_order.txt') as f:
			for l in f:
				l = l.strip()
				if len(l) > 0:
					self.group_order.append(l)


	def getStatuses (self):
		out = {}
		now = datetime.datetime.now()

		for group,locs in self.locations.iteritems():
			out[group] = []
			for li in locs:
				out[group].append(li.getInfo(now))

		return out

	def getGroupOrder (self):
		return self.group_order

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

