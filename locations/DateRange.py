

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
		if month < self.end_month and month > self.start_month:
			return True
		elif month == self.start_month and day >= self.start_day:
			return True
		elif month == self.end_month and day <= self.end_day:
			return True
		return False

