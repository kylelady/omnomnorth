
# Represents a range of days in a single year specified by a month and a day.
# These limitations make it easy to determine if a date is in the range.
class DateRange ():

	start_month = 0
	start_day   = 0
	end_month   = 0
	end_day     = 0

	def __init__ (self, start_month, start_day, end_month, end_day):
		self.start_month = start_month
		self.start_day   = start_day
		self.end_month   = end_month
		self.end_day     = end_day

	def in_range (self, month, day):
		if month < self.end_month and month > self.start_month:
			return True
		elif month == self.start_month and day >= self.start_day:
			return True
		elif month == self.end_month and day <= self.end_day:
			return True
		elif self.start_month > self.end_month:
			# wrap around end
			if month > self.start_month or month < self.end_month:
				return True
		return False

	def __str__ (self):
		return '{0}/{1} - {2}/{3}'.format(self.start_month, self.start_day, self.end_month, self.end_day)

if __name__ == '__main__':
	d = DateRange(9, 1, 5, 1)
	print d.in_range(10, 5)
	print d.in_range(12, 29)

