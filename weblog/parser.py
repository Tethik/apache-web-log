#!/usr/bin/python
import pytz
import re, sys, os, shutil
from geoip import geolite2
from dateutil import parser
from datetime import datetime
import ConfigParser
from weblog.models import db, Visit, Setting
import gzip
from weblog import app



# From https://github.com/lethain/apache-log-parser/blob/master/apache_parser.py
# Modified
def parse(filename):
	'Return tuple of dictionaries containing file data.'
	def make_model(x):
		visit = Visit()
		visit.uri = x.group('uri')
		visit.status_code = x.group('status_code')
		visit.referral = x.group('referral')
		visit.agent = x.group('agent')
		visit.ip = x.group('ip')

		country = geolite2.lookup(visit.ip)
		visit.country = country.country if country else 'ZZ'

		try:
			time = list(x.group('time'))
			time[11] = ' '
			visit.time = parser.parse("".join(time))
		except:
			pass

		return visit

	log_re = '(?P<ip>[.:0-9a-fA-F]+) - - \[(?P<time>.*?)\] "GET (?P<uri>.*?) HTTP/1.\d" (?P<status_code>\d+) \d+ "(?P<referral>.*?)" "(?P<agent>.*?)"'
	search = re.compile(log_re).search
	try:

		if filename.endswith(".gz"):
			f = gzip.open(filename, 'r')
		else:
			f = open(filename)
		matches = (search(line) for line in f)
		# print(f.read())
		return (make_model(x) for x in matches if x)
	except Exception as ex:
		print("error")
		print(ex)
		return []

def iterate_files(directory, filename_pattern, old_date):
	"""
	Runs and parses through log files with same filename and with .gz attached.
	domain.access.log.1
	domain.access.log.22.gz etc

	Ignores rows older than the latest parsed date.
	"""
	all_rows = []

	def key_func(x):
		try:
			i = int(re.search('\d+',x).group(0))
			return i
		except:
			return 0

	max_date = old_date
	for fn in sorted(os.listdir(directory), key=key_func):
		if filename_pattern not in fn:
			continue

		rows = 0
		for r in parse(directory + fn):
			if r.time > old_date:
				if r.time > max_date:
					max_date = r.time
				db.session.add(r)
				rows += 1

		print(fn, rows)
		if rows == 0:
			break
		db.session.commit()

	return max_date

if __name__ == "__main__":
	db.create_all()
	s = Setting.get("LatestRowDate")
	print(s)
	dt = pytz.utc.localize(datetime.min)
	if s:
		dt = parser.parse(s)

	dt = iterate_files(app.config["LOG_DIRECTORY"], app.config["LOG_FILE_PATTERN"], dt)

	Setting.set("LatestRowDate", str(dt))
