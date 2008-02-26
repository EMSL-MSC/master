#!/usr/bin/python

from distutils.core import setup

setup(name='master', version='0.1',
	author="Evan Felix",
	author_email="e@pnl.gov",
	description="""A asset managment system, designed to watch the cluster and also manage its state""",
	package_dir= {'master':'lib/master'},
	packages=['master'],
	scripts = ['client/master','client/sark','server/mcp'],
	data_files = [ ("/etc/init.d",["client/master-sark"])]
)
		
