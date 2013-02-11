import datetime

class HappyHour ():
	# List of lists of minute ranges
	hours = None
	# human readable strings of when the happy hours are each day
	pretty = None

	def __init__ (self):
		# create a list of 7 lists (one per day)
		self.hours = [[] for i in range(7)]

	def insert (self, start, end):
		# Convert start to which day
		# Shift by 300 to handle if a happy hour was 1am-2am or something
		# Assumes that no one has a happy hour starting before 5am that shoud
		#  show up on that day.
		day = (start - 300) / 24 / 60

		if day < 0 or day > 6:
			return

		offset = day * 24*60

		self.hours[day].append((start-offset, end-offset))

		# make sure to invalidate the human version
		self.pretty = None

	def get (self, dt):
		# get current day index
		day = dt.weekday()
		if dt.hour < 5:
			day -= 1
			if day == -1:
				day = 6

		if self.pretty is None:
			# Create the nice strings
			self.pretty = []
			for i, day_list in zip(range(7), self.hours):
				self.pretty.append([])
				for h in day_list:
					shour = h[0] / 60
					smin  = h[0] - (shour * 60)
					if shour < 12 or shour >= 24:
						stail = 'am'
					else:
						stail = 'pm'
					while shour > 12:
						shour -= 12

					ehour = h[1] / 60
					emin  = h[1] - (ehour * 60)
					if ehour < 12 or ehour >= 24:
						etail = 'am'
					else:
						etail = 'pm'
					while ehour > 12:
						ehour -= 12

					# format output string
					if shour == 12 and smin == 0:
						start = 'Midnight' if stail == 'am' else 'Noon'
					else:
						start = str(shour) + (':{0:02d}'.format(smin) if smin else '') + stail
					if ehour == 12 and emin == 0:
						end = 'Midnight' if etail == 'am' else 'Noon'
					else:
						end   = str(ehour) + (':{0:02d}'.format(emin) if emin else '') + etail
					hh_s  = '{0} - {1}'.format(start, end)

					self.pretty[i].append(hh_s)

		return self.pretty[day]



if __name__ == '__main__':
	h = HappyHour()
	h.insert(420, 480)
#	h.insert(4860, 4920)
#	h.insert(3780, 3840)
	print h.get(datetime.datetime.now())
#	h.insert(4321, 4439)
	h.insert(3599, 3854)
	print h.get(datetime.datetime.now())
	print h.get(datetime.datetime.now())


