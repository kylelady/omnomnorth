
# Handles all of the locations

import datetime
import os
import time

import LocationInfo
import LocationParser

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from utils import timezones

class PlaceWatcher (FileSystemEventHandler):
	lm = None

	def __init__(self, lm):
		self.lm = lm

	def on_created (self, event):
		if not event.is_directory:
			name,ext = os.path.splitext(event.src_path)
			if ext == '.loc':
				self.lm.parseLocation(event.src_path)
			elif name[-5:] == 'order' and ext == '.txt':
				# created a new order file, probably also created a new region
				# just reparse
				self.lm.reparse()

	def on_modified (self, event):
		if not event.is_directory:
			name,ext = os.path.splitext(event.src_path)
			if ext == '.loc':
				self.lm.parseLocation(event.src_path)
			elif name[-5:] == 'order' and ext == '.txt':
				self.lm.parseOrder(event.src_path)

	def on_deleted (self, event):
		if event.is_directory:
			self.lm.reparse()
		elif os.path.splitext(event.src_path)[1] == '.loc':
			self.lm.parseLocation(event.src_path)

	def on_moved (self, event):
		if event.is_directory:
			self.lm.reparse()
		else:
			self.lm.parseLocation(event.src_path)
			self.lm.parseLocation(event.dest_path)


class LocationManager ():

	location_parser = LocationParser.LocationParser()
	# Map of location regions to a map of locations groups to a list of
	#  locations in that group.
	locations = {}
	group_order = {}

	directory = None

	# Parse all location files and keep track of all locations.
	# This could be prettier somehow.
	def __init__ (self, directory):
		self.directory = os.path.abspath(directory)

		self.reparse()


	def startPlaceWatch (self):
		self.observer = Observer()
		self.observer.schedule(PlaceWatcher(self), self.directory, recursive=True)
		self.observer.start()


	def reparse (self):

		self.locations = {}
		self.group_order = {}

		root_files = os.listdir(self.directory)
		for rf in root_files:
			if os.path.isdir(self.directory + '/' + rf):
				# found a region folder
				self.locations[rf.lower()] = {}

				region_files = os.listdir(self.directory + '/' + rf)
				for ref in region_files:
					if os.path.isdir(self.directory + '/' + rf + '/' + ref):
						# found a group folder
						self.locations[rf.lower()][ref.lower()] = []

						self.parseGroup(rf.lower(), ref.lower())

				# Load in group order
				self.parseOrder(self.directory + '/' + rf + '/order.txt')


	"""
	Parse a location by removing all locations in the group and rescanning
	the group.

	path: must be a full path to a .loc file
	"""
	def parseLocation (self, path):
		# remove the base so we can accurately get region and group
		path = path.replace(self.directory, '')
		folders = path.split('/')
		if len(folders) < 3:
			return

		region = folders[-3].strip().lower()
		group  = folders[-2].strip().lower()

		if region not in self.locations:
			self.locations[region] = {}

		# if the group never existed, create it
		# if it did, delete the old list and reparse
		self.locations[region][group] = []

		self.parseGroup(region, group)


	def parseGroup (self, region, group):

		group_path  = self.directory + '/' + region + '/' + group
		group_files = os.listdir(group_path)
		for gf in group_files:
			if os.path.splitext(gf)[1] == '.loc':
				try:
					li = LocationInfo.LocationInfo()
					self.location_parser.parse(group_path + '/' + gf, li)
					self.locations[region][group].append(li)
				except LocationParser.LocationParseError as e:
					# Some error in this config file
					print e

	def parseOrder (self, order_path):
		path = order_path.replace(self.directory, '')
		folders = path.split('/')
		if len(folders) != 3:
			return

		region = folders[-2].lower()

		self.group_order[region] = []
		try:
			with open(order_path) as f:
				for l in f:
					l = l.strip().lower()
					if len(l) > 0:
						self.group_order[region].append(l)
		except IOError:
			self.group_order[region] = self.locations[region].keys()

	def getRegions (self):
		return self.locations.keys()

	def getStatuses (self, region):
		region = region.strip().lower()
		if region not in self.locations:
			return None

		out = {}
		now = datetime.datetime.now(timezones.Eastern)

		for group,locs in sorted(self.locations[region].iteritems()):
			out[group] = []
			for li in locs:
				out[group].append(li.getInfo(now))

		return out

	def getGroupOrder (self, region):
		region = region.strip().lower()
		return self.group_order[region]

	def __str__ (self):
		out = ''
		for region in self.locations.keys():
			out += '{0}\n'.format(region)
			for group in self.group_order[region]:
				locs = self.locations[region][group]
				out += '  {0}\n'.format(group)
				for li in locs:
					status = li.prettyStatus(li.getStatus(datetime.datetime.now()))
					name   = li.getName()
					out += '    {0}: {1}\n'.format(name.encode('utf-8'), status)

		return out


if __name__ == '__main__':
	lm = LocationManager('../places')
	print lm
	print lm.getRegions()
	lm.startPlaceWatch()
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		quit()

