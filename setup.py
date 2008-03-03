#!/usr/bin/python

from setuptools import setup,find_packages

setup(name='master', version='0.1',
	author="Evan Felix",
	author_email="e@pnl.gov",
	description="""A asset managment system, designed to watch the cluster and also manage its state""",
	package_dir= {'master':'lib/master'},
	packages=['master'],
	scripts = ['client/master','client/sark'],
	data_files = [ ("/etc/init.d",["client/master-sark"]),("/usr/sbin",["server/mcp"]) ],
	requires=['python (>=2.4)']
)
		
