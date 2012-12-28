
import RangeBinaryTree

def enum(**enums):
	return type('Enum', (), enums)


details = enum(NAME=1, URL=2, DESC=3, HOURS=4, GROUP=5)


name = ''
url = ''
description = ''
group = ''
hours = RangeBinaryTree.RangeBinaryTree()
current_category = None


class LocationParseError(Exception):
	def __init__ (self, err_str):
		self.err_str = err_str
	def __str__ (self):
		return self.err_str	



def get_detail_category (s):
	s = s.strip().lower()
	if s == 'name':
		return details.NAME
	elif s == 'url':
		return details.URL
	elif s == 'desc' or s == 'description':
		return details.DESC
	elif s == 'group':
		return details.GROUP
	elif s == 'hours':
		return details.HOURS
	return None


def process_remainder (s):
	global name, url, description, hours, current_category
	s = s.strip()

	if current_category == details.NAME:
		name += s
	elif current_category == details.URL:
		url += s
	elif current_category == details.DESC:
		description += s
	elif current_category == details.HOURS:
		if '/' in s:
			# date range
			pass
		else:
			# should be a day of the week then colon then hour info
			hsplit = s.split(':', 1)
			if len(hsplit) < 2:
				return
			day   = hsplit[0].strip()
			times = hsplit[1].split('and')
			range_pairs = []
			for t in times:
				print t.strip()
				tsplit = t.split('-')
				range_pairs.append((tsplit[0], tsplit[1]))
			ranges = get_ranges(day, range_pairs)
			for r in ranges:
				hours.insert(r[0], r[1])

# returns base minute offset
def process_day (day):
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
def process_hours_minutes (s):
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
"""
def get_ranges (day, range_pairs):
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
			s_hour, s_minute = process_hours_minutes(start)
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
				e_hour, e_minute = process_hours_minutes(end)
			elif 'pm' in end:
				e_hour_offset += 12
				end = end.replace('pm', '').strip()
				e_hour, e_minute = process_hours_minutes(end)
			else:
				# don't know am or pm, try to figure it out
				e_hour, e_minute = process_hours_minutes(end)
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

	# Add in the offset for the day of the week
	day_offset_minutes = process_day(day)

	out_shifted = []
	for r in out_ranges:
		out_shifted.append((r[0]+day_offset_minutes, r[1]+day_offset_minutes))

	return out_shifted




f = open('gpeak.loc', 'r')

lines = f.readlines()

for l in lines:
	l = l.strip('\n')

	if len(l) == 0:
		continue

	elif l[0] == '#':
		#comment
		continue

	elif l[0] == '\t' or l[0:3] == '    ':
		# same category
		process_remainder(l)

	else:
		# check for a new category and possibly process whats on the line
		lsplit = l.split(':', 1)
		print lsplit

		current_category = get_detail_category(lsplit[0])
		if current_category == None:
			continue

		if len(lsplit) == 1:
			# nothing on the rest of this line, loop and try the next line
			continue

		# now that we have a category, process whats left on this line in that
		# context.
		process_remainder(lsplit[1])



hours.printTree()



