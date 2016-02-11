# dynamic.py

dynamic.py is a script that resolves a domain name to an IP address, then
adds that IP address to your /etc/hosts file.

## Motivation

I log into my home server remotely, and I need to have a way to find its
new IP address if it changes. I set up a dynamic DNS address, but it's
cumbersome to type the whole thing.

## Usage

dynamic.py will read your /etc/hosts file and look for special directives
that tell it what domain names to look up.

The basic pattern is a pound, followed by the domain name you want to resolve,
followed by one or more aliases that you want to resolve to the domain name.

Example:

    #subdomain.dynamic-dns.tld	server1-ext	nas1-ext	DYNAMIC

Then, I add dynamic.py to root's crontab, like so:

    */30 * * * * /path/to/dynamic.py

This re-resolves the domain name frequently enough for my purposes.
