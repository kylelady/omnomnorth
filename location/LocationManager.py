
# Handles all of the locations

import datetime
import os

import LocationInfo
import LocationParser

class LocationManager ():

	location_parser = LocationParser.LocationParser()
	# Map of location regions to a map of locations groups to a list of
	#  locations in that group.
	locations = {}
	group_order = []

	# Parse all location files and keep track of all locations.
	# This could be prettier somehow.
	def __init__ (self, directory='.'):
		self.locations = {}

		root_files = os.listdir(directory)
		for rf in root_files:
			if os.path.isdir(directory + '/' + rf):
				# found a region folder
				self.locations[rf.lower()] = {}

				region_files = os.listdir(directory + '/' + rf)
				for ref in region_files:
					if os.path.isdir(directory + '/' + rf + '/' + ref):
						# found a group folder
						self.locations[rf.lower()][ref.lower()] = []

						group_files = os.listdir(directory + '/' + rf + '/' + ref)
						for gf in group_files:
							ext = os.path.splitext(gf)[1]
							if ext == '.loc':
								li = LocationInfo.LocationInfo()
								self.location_parser.parse(directory + '/' + rf + '/' + ref + '/' + gf, li)
								self.locations[rf.lower()][ref.lower()].append(li)

		# Load in group order
	#	with open(directory + '/group_order.txt') as f:
	#		for l in f:
	#			l = l.strip()
	#			if len(l) > 0:
	#				self.group_order.append(l)


	def getRegions (self):
		return self.locations.keys()

	def getStatuses (self, region):
		region = region.strip().lower()
		if region not in self.locations:
			return None

		out = {}
		now = datetime.datetime.now()

		for group,locs in self.locations[region].iteritems():
			out[group] = []
			for li in locs:
				out[group].append(li.getInfo(now))

		return out

#	def getGroupOrder (self):
#		return self.group_order

	def __str__ (self):
		out = ''
		for region in self.locations.keys():
			out += '{0}\n'.format(region)
			for group,locs in self.locations[region].iteritems():
				out += '  {0}\n'.format(group)
				for li in locs:
					status = li.prettyStatus(li.getStatus(datetime.datetime.now()))
					name   = li.getName()
					out += '    {0}: {1}\n'.format(name, status)

		return out


if __name__ == '__main__':
	lm = LocationManager('../places')
	print lm.getStatuses('central')
	print lm
	print lm.getRegions()

