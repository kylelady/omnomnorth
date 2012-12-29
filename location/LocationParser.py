
import DateRange

def enum(**enums):
	return type('Enum', (), enums)


details = enum(NAME=1, URL=2, DESC=3, HOURS=4, GROUP=5, ADDRESS=6)



class LocationParseError(Exception):
	def __init__ (self, err_str):
		self.err_str = err_str
	def __str__ (self):
		return self.err_str	


class LocationParser ():
	current_category = None
	loc_manager      = None

	def __init__ (self):
		pass

	def parse (self, filename, loc_info):
		try:
			f = open(filename, 'r')
		except IOError:
			raise LocationParseError('Could not open "{0}".'.format(filename))

		# save location manager
		self.loc_manager = loc_info

		lines = f.readlines()

		for l in lines:
			l = l.strip('\n')

			if len(l) == 0 or l[0] == '#':
				# empty or comment
				continue

			elif l[0] == '\t' or l[0:3] == '    ':
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


	def get_detail_category (self, s):
		s = s.strip().lower()
		if s == 'name':
			return details.NAME
		elif s == 'url':
			return details.URL
		elif s == 'desc' or s == 'description':
			return details.DESC
		elif s == 'group' or s == 'area':
			return details.GROUP
		elif s == 'hours':
			return details.HOURS
		elif s == 'location' or s == 'address' or s == 'loc':
			return details.ADDRESS
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
		elif self.current_category == details.GROUP:
			self.loc_manager.setGroup(s)
		elif self.current_category == details.ADDRESS:
			self.loc_manager.setAddress(s)
		elif self.current_category == details.HOURS:
			if '/' in s:
				# date range
				self.loc_manager.setDateRange(self.process_date_range(s))
			else:
				# should be a day of the week then colon then hour info
				hsplit = s.split(':', 1)
				if len(hsplit) < 2:
					# no day listed, assume whatever is on this list applies
					#  to all days.
					day = 'all'
					times = s.split('and')
				else:
					day   = hsplit[0].strip()
					times = hsplit[1].split('and')
				range_pairs = []
				for t in times:
					tsplit = t.split('-')
					range_pairs.append((tsplit[0], tsplit[1]))
				ranges = self.get_ranges(day, range_pairs)
				for r in ranges:
					self.loc_manager.insertHours(r[0], r[1])


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


	# returns base minute offset
	def process_day (self, day):
		day_offset_minutes = 0
		if day == 'm' or day == 'mon' or day == 'monday':
			day_offset_minutes = 0
		elif day == 'tu' or day == 'tue' or day == 'tuesday':
			day_offset_minutes = 1*24*60
		elif day == 'w' or day == 'wed' or day == 'wednesday':
			day_offset_minutes = 2*24*60
		elif day == 'th' or day == 'thu' or day == 'thursday':
			day_offset_minutes = 3*24*60
		elif day == 'f' or day == 'fri' or day == 'friday':
			day_offset_minutes = 4*24*60
		elif day == 'sa' or day == 'sat' or day == 'saturday':
			day_offset_minutes = 5*24*60
		elif day == 'su' or day == 'sun' or day == 'sunday':
			day_offset_minutes = 6*24*60
		else:
			raise LocationParseError('Unable to parse "{0}" as day.'.format(day))

		return day_offset_minutes


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
	Accepts a day string and a list of (start, end) string tuples.
	Returns a list of (start, end) integer tuples that correspond to minutes from
	the beginning of the week.

	Note: the day string can be 'all' in which it will return ranges for all
	days of the week
	"""
	def get_ranges (self, day, range_pairs):
		day = day.strip().lower()

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
				s_hour += s_hour_offset

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
				elif 'pm' in end:
					e_hour_offset += 12
					end = end.replace('pm', '').strip()
					e_hour, e_minute = self.process_hours_minutes(end)
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
			if e_hour < s_hour:
				# add 12 hours until we get to the next day
				while e_hour < 24:
					e_hour += 12

			# Calculate the minute offset
			stotal = s_hour*60 + s_minute
			etotal = e_hour*60 + e_minute

			out_ranges.append((stotal, etotal))

		out_shifted = []
		# Add in the offset for the day of the week
		if day == 'all':
			for offset in range(0, 7*24*60, 24*60):
				for r in out_ranges:
					out_shifted.append((r[0]+offset, r[1]+offset))

		else:
			day_offset_minutes = self.process_day(day)

			out_shifted = []
			for r in out_ranges:
				out_shifted.append((r[0]+day_offset_minutes, r[1]+day_offset_minutes))

		return out_shifted





