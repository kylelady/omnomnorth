
import parse
import RangeBinaryTree
import DateRange
import datetime

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

State = enum('OPEN', 'OPENING_SOON', 'CLOSED', 'CLOSING_SOON')
StateNames = ['OPEN', 'OPENING_SOON', 'CLOSED', 'CLOSING_SOON']

class LocationInfo ():
	name  = ''
	url   = ''
	desc  = ''
	group = ''
	# map of date ranges to RangeBinaryTrees that contain open hour ranges
	hours = {}
	current_date_range = None

	def __init__ (self):
		self.hours = {}
		pass

	def setName (self, name):
		self.name = name

	def setUrl (self, url):
		self.url = url

	def setDescription (self, desc):
		self.desc = desc

	def setGroup (self, g):
		self.group = g

	def setDateRange (self, dates):
		self.current_date_range = dates
		self.hours[dates] = RangeBinaryTree.RangeBinaryTree()

	def insertHours (self, start, end):
		if self.current_date_range == None:
			drange = DateRange.DateRange(1, 1, 12, 31)
			self.current_date_range = drange
			self.hours[drange] = RangeBinaryTree.RangeBinaryTree()

		self.hours[self.current_date_range].insert(start, end)


	"""
	dt: datetime.now()
	returns: State enum
	"""
	def getStatus (self, dt):

		min_offset             = (dt.weekday()*24*60) + (dt.hour*60) + dt.minute
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

	def getGroup (self):
		return self.group


	def __str__ (self):
	#	for i in self.hours.iteritems():
	#		i[1].printTree()
		return self.name



if __name__ == '__main__':

	t = LocationInfo()
	p = parse.LocationParser()

	p.parse('gpeak.loc', t)

	print t

	print StateNames[t.getStatus(datetime.datetime.now())]

