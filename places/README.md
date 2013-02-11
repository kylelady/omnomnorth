Places
======

All places are specified in a text file ending with the `.loc` extension. 
Organization of locations is done with folders. The folder tree looks like:

	places/<region name>/<group name>/<place>.loc

Adding a place is as simple as creating a new `.loc` file in the proper folder.


.loc File Format
----------------

`.loc` files are designed to be easy to write. Here is the format:

~~~~~~~~~~~~~~~~~~~
name: <name>
address: <address>
url: <url>
description: <some description>
hours:
	[<month>/<day> - <month>/<day>]
	<day>: <time>[am|pm]-<time>[am|pm]
	<day>-<day>: <time>-<time>
	<day>,<day>,<day>: <time>-<time>
happy hour:
	<same format as hours>
~~~~~~~~~~~~~~~~~~~~

Name, address, url, and description are just text fields. Hours can take a
series of optional date ranges with hours that pertain to each date range. Hours
are listed for each day, range of days, or list of days. Starting times are
assumed to be AM, ending times are assumed to be PM. Use am/pm specifiers to
override this default. Days can look like: `m|mo|mon|monday`. Times can look
like: `10|10:30|noon|midnight`. If no day is specified, all 7 days are assumed.
If a day is missing, it is assumed to be closed for that day.

### Example 1

~~~~~~
name: Grizzly Peak
url: http://www.grizzlypeak.net/
description: Brewpub in Ann Arbor
address: 120 West Washington, Ann Arbor, MI 48104

hours:
	mon-th: 11-11
	f: 11-2am
	saturday: 11-midnight
	su: noon-11

happy hour:
	m-f: 5pm-6pm
~~~~~

### Example 2

~~~~~
name: Ugos

hours:
	5/1 - 8/31
	m-th: 8-8:30
	f: 8-6

	9/1 - 4/31
	m-th: 8-1am
	f: 8-8
	sa: noon-6
	su: noon-midnight
~~~~~

### Aliases

Many sections can be refernced by a couple names, if one makes you happier.

~~~~~~~
NAME:      ['name'],
URL:       ['url', 'website'],
DESC:      ['desc', 'description'],
HOURS:     ['hours', 'hour'],
ADDRESS:   ['location', 'loc', 'address', 'addr'],
HAPPYHOUR: ['happy hour', 'happy hours', 'happy'],
~~~~~~~


Group Ordering
--------------

Inside a region, groups are ordered based on an `order.txt` file in the region
folder. This list is simply contains the group folder names in the order they
should be displayed. If a group is not included it will not be displayed. If
there is no `order.txt` file, the order is unspecified and will probably be
alphabetical but this is not guaranteed.

### Example

~~~~~
order.txt:
oncampus
prfe
krogerville
plymouth
west
~~~~~




