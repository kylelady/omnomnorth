
import RangeBinaryTree
import DateRange
import datetime
import HappyHour

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

State = enum('OPEN', 'OPENING_SOON', 'CLOSED', 'CLOSING_SOON')
StateNames = ['OPEN', 'OPENING_SOON', 'CLOSED', 'CLOSING_SOON']

class LocationInfo ():
	name       = ''
	url        = ''
	desc       = ''
	address    = ''
	# map of date ranges to RangeBinaryTrees that contain open hour ranges
	hours      = {}
	happyhours = {}

	def __init__ (self):
		self.hours      = {}
		self.happyhours = {}

	def setName (self, name):
		self.name = name

	def setUrl (self, url):
		self.url = url

	def setDescription (self, desc):
		self.desc = desc

	def setAddress (self, addr):
		self.address = addr

	def insertHours (self, start, end, date_range):
		if date_range not in self.hours:
			self.hours[date_range] = RangeBinaryTree.RangeBinaryTree()

		self.hours[date_range].insert(start, end)

	def insertHappyHours (self, start, end, date_range):
		if date_range not in self.happyhours:
			self.happyhours[date_range] = HappyHour.HappyHour()

		self.happyhours[date_range].insert(start, end)

	def getInfo (self, dt):
		out = {}
		out['name']   = self.name
		if self.url != '':
			out['url']    = self.url
		if self.desc != '':
			out['desc']   = self.desc
		if self.address != '':
			out['address'] = self.address
		out['status'] = self.getStatus(dt)
		out['happy_hours'] = self.getHappyHour(dt)
		if len(out['happy_hours']) == 0:
			del out['happy_hours']

		return out

	def getHappyHour (self, dt):
		hhours = []
		for date_range,hours in self.happyhours.iteritems():
			if date_range.in_range(dt.month, dt.day):
				hhours = hours.get(dt)
				break
		return hhours

	"""
	dt: datetime.now()
	returns: State enum
	"""
	def getStatus (self, dt):

		min_offset = (dt.weekday()*24*60) + (dt.hour*60) + dt.minute
		min_offset_hour_future = min_offset + 60
		if min_offset_hour_future > 7*24*60:
			min_offset_hour_future -= 7*24*60

		open_now  = False
		open_soon = False

		# Find the correct date range
		for date_range,hours in self.hours.iteritems():
			if date_range.in_range(dt.month, dt.day):
				open_now = hours.in_range(min_offset)
				open_soon = hours.in_range(min_offset_hour_future)
				break

		# Actual logic to determine which state the location is in
		if open_now:
			if not open_soon:
				return State.CLOSING_SOON
			else:
				return State.OPEN
		elif open_soon:
			return State.OPENING_SOON
		
		return State.CLOSED


	def prettyStatus (self, status):
		return StateNames[status]

	def getName (self):
		return self.name

	def __str__ (self):
		out = 'Name: {0}\n'.format(self.name)
		for date_range,hours in self.hours.iteritems():
			out += '  {0}\n'.format(date_range)
			out += str(hours)
		return out



if __name__ == '__main__':

	import LocationParser

	t = LocationInfo()
	p = LocationParser.LocationParser()

	p.parse('../places/central/state/redhawk.loc', t)

	print t

	print StateNames[t.getStatus(datetime.datetime.now())]

