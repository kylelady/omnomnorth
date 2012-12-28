
import parse
import RangeBinaryTree
import DateRange



class LocationInfo ():
	name  = ''
	url   = ''
	desc  = ''
	group = ''
	# map of date ranges to RangeBinaryTrees that contain open hour ranges
	hours = {}
	current_date_range = None

	def __init__ (self):
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

	def __str__ (self):
		for i in self.hours.iteritems():
			i[1].printTree()
		return ''

t = LocationInfo()
p = parse.LocationParser()

p.parse('gpeak.loc', t)

print t


