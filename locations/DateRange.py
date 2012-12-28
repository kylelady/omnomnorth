

class DateRange ():

	start_month = 0
	start_day   = 0
	end_month   = 0
	end_day     = 0

	def __init__ (self, start_month, start_day, end_month, end_day):
		self.start_month = start_month
		self.start_end   = start_day
		self.end_month   = end_month
		self.end_day     = end_day

	def in_range (self, month, day):
		if month < end_month and month > start_month:
			return True
		elif month == start_month and day >= start_day:
			return True
		elif month == end_month and day <= end_day:
			return True
		return False

