
import codecs
import DateRange

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)


details = enum('NAME', 'URL', 'DESC', 'HOURS', 'ADDRESS', 'HAPPYHOUR')
# days of week
dow = enum('MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY')

all_days = [dow.MONDAY, dow.TUESDAY, dow.WEDNESDAY, dow.THURSDAY, dow.FRIDAY, dow.SATURDAY, dow.SUNDAY]

detail_categorize = {
	details.NAME:      ['name'],
	details.URL:       ['url', 'website'],
	details.DESC:      ['desc', 'description'],
	details.HOURS:     ['hours', 'hour'],
	details.ADDRESS:   ['location', 'loc', 'address', 'addr'],
	details.HAPPYHOUR: ['happyhour', 'happyhours', 'happy'],
}

class LocationParseError(Exception):
	def __init__ (self, err_str):
		self.err_str = err_str
	def __str__ (self):
		return self.err_str	


class LocationParser ():
	current_category   = None
	loc_manager        = None
	current_date_range = None

	def __init__ (self):
		pass

	def parse (self, filename, loc_info):
		try:
		#	f = open(filename, 'r')
			f = codecs.open(filename, encoding='utf-8')
		except IOError:
			raise LocationParseError('Could not open "{0}".'.format(filename))

		# save location manager
		self.loc_manager = loc_info
		# set default date range
		self.current_date_range = DateRange.DateRange(1, 1, 12, 31)

		lines = f.readlines()

		for l in lines:
			l = l.strip('\n')

			# remove any comment
			l = l.split(' #', 1)[0]
			l = l.split('\t#', 1)[0]

			if len(l) == 0 or l[0] == '#':
				# empty or comment
				continue

			elif self.is_tab(l[0:4]):
				# same category
				self.process_remainder(l)

			else:
				# check for a new category and possibly process whats on the line
				lsplit = l.split(':', 1)
				if len(lsplit) != 2:
					raise LocationParseError('Could not understand line "{0}".'.format(l))

				self.current_category = self.get_detail_category(lsplit[0])

				# now that we have a category, process whats left on this line in that
				# context.
				self.process_remainder(lsplit[1])

		f.close()


	def is_tab (self, s):
		if s.count('\t') > 0:
			return True
		if s.count(' ') > 3:
			return True
		return False


	# Given a category text string, try to match it to a category and return
	#  the category enum.
	def get_detail_category (self, s):
		s = ''.join(s.split()).lower()
		for det,words in detail_categorize.iteritems():
			if s in words:
				return det

		raise LocationParseError('Did not understand "{0}" as a detail type.'.format(s))


	def process_remainder (self, s):
	#	global name, url, description, hours, current_category
		s = s.strip()

		if len(s) == 0:
			return

		if self.current_category == details.NAME:
			self.loc_manager.setName(s)
		elif self.current_category == details.URL:
			self.loc_manager.setUrl(s)
		elif self.current_category == details.DESC:
			self.loc_manager.setDescription(s)
		elif self.current_category == details.ADDRESS:
			self.loc_manager.setAddress(s)
		elif self.current_category == details.HOURS:
			self.process_hours_remainder(s)
		elif self.current_category == details.HAPPYHOUR:
			self.process_hours_remainder(s)


	def process_hours_remainder (self, s):
		if '/' in s:
			# date range
			self.current_date_range = self.process_date_range(s)
		else:
			# should be a day of the week then colon then hour info
			hsplit = s.split(':', 1)
			# check if there is a : that it follows a day
			# this could be a problem if a place opens at 7:30 everday
			if len(hsplit) == 2:
				try:
					day_temp = self.process_day(hsplit[0])
				except LocationParseError:
					hsplit = []
			if len(hsplit) < 2:
				# no day listed, assume whatever is on this list applies
				#  to all days.
				day = all_days
				times = s.split('and')
			else:
				day   = self.process_day(hsplit[0])
				times = hsplit[1].split('and')
			range_pairs = []
			for t in times:
				tsplit = t.split('-')
				range_pairs.append((tsplit[0], tsplit[1]))
			ranges = self.get_ranges(day, range_pairs)
			for r in ranges:
				if self.current_category == details.HOURS:
					self.loc_manager.insertHours(r[0],
					                             r[1],
					                             self.current_date_range)
				elif self.current_category == details.HAPPYHOUR:
					self.loc_manager.insertHappyHours(r[0],
					                                  r[1],
					                                  self.current_date_range)


	def process_date_range (self, s):
		dates = s.split('-')
		if len(dates) != 2:
			raise LocationParseError('Not a date range: {0}.'.format(s))

		sdate_split = dates[0].split('/')
		edate_split = dates[1].split('/')
		try:
			smonth = int(sdate_split[0].strip())
			sday   = int(sdate_split[1].strip())
			emonth = int(edate_split[0].strip())
			eday   = int(edate_split[1].strip())
		except:
			raise LocationParseError('Not a valid date range {0}.'.format(s))

		return DateRange.DateRange(smonth, sday, emonth, eday)


	# Returns a list of days from a range
	def process_day_range (self, s):
		days_in_range = []

		drange = s.split('-')
		start = self.process_day_single(drange[0])
		end   = self.process_day_single(drange[1])

		# loop through the number version of the enum because its easier
		while True:
			days_in_range.append(start)
			if start == end:
				break
			start += 1
			if start > 6:
				start = 0

		return days_in_range


	def process_day_list (self, s):
		days_in_list = []

		dlist = s.split(',')

		for d in dlist:
			try:
				day = self.process_day_single(d)
				days_in_list.append(day)
			except LocationParseError:
				# if bad day, just skip it
				pass

		return days_in_list


	# returns base minute offset
	def process_day (self, day):
		if '-' in day:
			# day was specified as range
			return self.process_day_range(day)
		elif ',' in day:
			# day was specified as a comma separted list
			return self.process_day_list(day)
		
		return self.process_day_single(day)

	def process_day_single (self, day):
		day = day.strip().lower()
		if day == 'm' or day == 'mo' or day == 'mon' or day == 'monday':
			return dow.MONDAY
		elif day == 'tu' or day == 'tue' or day == 'tuesday':
			return dow.TUESDAY
		elif day == 'w' or day == 'we' or day == 'wed' or day == 'wednesday':
			return dow.WEDNESDAY
		elif day == 'th' or day == 'thu' or day == 'thursday':
			return dow.THURSDAY
		elif day == 'f' or day == 'fri' or day == 'friday':
			return dow.FRIDAY
		elif day == 'sa' or day == 'fr' or day == 'sat' or day == 'saturday':
			return dow.SATURDAY
		elif day == 'su' or day == 'sun' or day == 'sunday':
			return dow.SUNDAY
		
		raise LocationParseError('Unable to parse "{0}" as day.'.format(day))


	# returns base minute offset
	def get_day_offset (self, day):
		try:
			return (day)*24*60
		except:
			raise LocationParseError('Bad enum to get_day_offset')


	#returns hours,minutes from ex. 10:30
	def process_hours_minutes (self, s):
		hour   = 0
		minute = 0

		tsplit = s.split(':')
		try:
			hour = int(tsplit[0])
			if len(tsplit) == 2:
				minute = int(tsplit[1])
		except ValueError:
			raise LocationParseError('Unable to parse "{0}" as time.'.format(s))

		return hour,minute


	"""
	Accepts a day string (or list) and a list of (start, end) string tuples.
	Returns a list of (start, end) integer tuples that correspond to minutes from
	the beginning of the week.
	"""
	def get_ranges (self, day, range_pairs):

		out_ranges = []

		for r in range_pairs:
			start = r[0].strip().lower()
			end   = r[1].strip().lower()

			# Process the start time.
			s_hour_offset = 0
			s_hour        = 0
			s_minute      = 0
			if start == 'noon':
				s_hour = 12
			elif start == 'midnight':
				s_hour = 0
			else:
				if 'am' in start:
					start = start.replace('am', '').strip()
				elif 'pm' in start:
					s_hour_offset += 12
					start = start.replace('pm', '').strip()
				s_hour, s_minute = self.process_hours_minutes(start)
				if s_hour != 12:
					# Only apply the pm offset to non twelve hours
					s_hour += s_hour_offset
				else:
					# Determine if it is 12:xx PM or AM.
					if s_hour_offset == 0:
						s_hour = 0

			# Process the end time.
			e_hour_offset = 0
			e_hour        = 0
			e_minute      = 0
			if end == 'noon':
				e_hour = 12
			elif end == 'midnight':
				e_hour = 0
			else:
				if 'am' in end:
					end = end.replace('am', '').strip()
					e_hour, e_minute = self.process_hours_minutes(end)
					if e_hour == 12:
						# 12 am was entered this most likely means past midnight
						# of the next day.
						if s_hour > 0:
							e_hour += 12
						elif s_hour == 0 and s_min < e_min:
							# This is a very strange case where the open times
							# are something like 12:15am-12:35am.
							e_hour = 0
				elif 'pm' in end:
					end = end.replace('pm', '').strip()
					e_hour, e_minute = self.process_hours_minutes(end)
					e_hour += 12
				else:
					# don't know am or pm, try to figure it out
					e_hour, e_minute = self.process_hours_minutes(end)
					# Assume if not labeled the end time is pm
					e_hour += 12

			# Extra logic to handle chains of open times. That is, if a place is
			#  open from 11am-2pm and 5-9, then obviously the 5-9 corresponds to 
			#  5pm-9pm and not 5am-9pm. This fixes that.
			if len(out_ranges) > 0:
				# this is a multirange time for this day
				# we need to make sure that the start time for this range
				#  is greater than the end time of the previous range
				prev_end_time = out_ranges[-1][1]
				if s_hour*60 + s_minute < prev_end_time:
					s_hour += 12
					if e_hour < 12:
						# didn't specify pm for the end time, need to increment
						#  that too
						e_hour += 12

			# Check if the place is open after midnight
			if e_hour <= s_hour:
				# add 12 hours until we get to the next day
				while e_hour < 24:
					e_hour += 12

			# Calculate the minute offset
			stotal = s_hour*60 + s_minute
			etotal = e_hour*60 + e_minute

			out_ranges.append((stotal, etotal))

		out_shifted = []
		# Add in the offset for the day of the week
		if type(day) is not list:
			day = [day]

		for d in day:
			day_offset_minutes = self.get_day_offset(d)

			for r in out_ranges:
				out_shifted.append((r[0]+day_offset_minutes, r[1]+day_offset_minutes))

		return out_shifted





