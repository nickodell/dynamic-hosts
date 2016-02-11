#!/usr/bin/python
import re
import socket
import StringIO

class LineBuffer():
	def __init__(self, fh):
		self.text_array = fh.read()
		self.text_array = self.text_array.split("\n")
		self.current_line = self.text_array.pop(0)
	def next_line(self):
		self.current_line = self.text_array.pop(0)

VERSION = "v0.01"
HEADER_TEXT = """# dynamic.py: version %s
# dynamic.py: resolved %s hosts in %s sections
# dynamic.py: %s errors
"""

HOSTFILE_PATH = "/etc/hosts"
hostfile_handle = open(HOSTFILE_PATH, "rt")
last_resolution_successful = False
lb = LineBuffer(hostfile_handle)
hostfile_handle.close()
out = StringIO.StringIO()
errors = 0
sections = 0
hosts = 0
try:
	while True:
		match_obj = re.match("\s*#(.*DYNAMIC)\s*", lb.current_line)
		if match_obj:
			tokens = match_obj.group(1).split()
			aliases = tokens[1:-1] # Strip first and last token
			hostname_to_resolve = tokens[0]
			sections += 1
			hosts += len(aliases)
			try:
				ip = socket.gethostbyname(hostname_to_resolve)
				out.write(lb.current_line + "\n")
				out.write(ip + "\t" + "\t".join(aliases) + " # dynamically resolved\n")
				last_resolution_successful = True
			except socket.gaierror:
				out.write(lb.current_line + "\n")
				out.write("# Unable to resolve hostname\n")
				last_resolution_successful = False
				errors += 1
		elif "# dynamically resolved" in lb.current_line:
			# This is a line from a previous invocation
			# Delete it if we were able to resolve it this time
			if last_resolution_successful:
				pass
			else:
				out.write(lb.current_line + "\n")

		elif "# Unable to resolve hostname" in lb.current_line:
			pass
		elif "# dynamic.py" in lb.current_line:
			pass
		else:
			out.write(lb.current_line + "\n")
		lb.next_line()
except IndexError:
	pass

new_hostfile = HEADER_TEXT % (VERSION, hosts, sections, errors) + out.getvalue()

# Fix bug where the hostfile expands by one newline each time
new_hostfile = new_hostfile[:-1] if new_hostfile[-1] == "\n" else new_hostfile

print new_hostfile

hostfile_handle = open(HOSTFILE_PATH, "wt")
hostfile_handle.write(new_hostfile)
hostfile_handle.close()
