#!/usr/bin/python
# vim: noet:ts=4:sw=4


#from setuptools import setup,find_packages
from distutils import sysconfig
from distutils.core import setup
from distutils.command.install_scripts import install_scripts
from distutils.command.build_scripts import build_scripts
from distutils.command.bdist_rpm import bdist_rpm

class local_install_scripts(install_scripts):

	def finalize_options(self):
		self.set_undefined_options('install', ('root', 'install_dir'))
		install_scripts.finalize_options(self)

class local_build_scripts(build_scripts):

	def initialize_options(self):
		build_scripts.initialize_options(self)

	def get_source_files(self):
		l=[]
		for k,v in self.blds.items():
			print k,v
			l += v.scripts
		return l

	def mkbld(self,thedir):
		b = build_scripts(self.distribution)
		b.build_dir = self.build_dir+thedir
		b.scripts = []
		b.force = self.force
		if sysconfig.get_config_var("VERSION") != "2.3":
			b.executable = self.executable
		b.outfiles = None
		return b

	def finalize_options(self):
		build_scripts.finalize_options(self)
		# build up a dictionary of commands for sub scripting
		self.blds={}

		for d,files in self.scripts:
			if not self.blds.has_key(d):
				self.blds[d]=self.mkbld(d)
			self.blds[d].scripts += files

		#for k,v in self.blds.items():
		#	print k,'=>',self.blds[k].scripts,self.blds[k].build_dir

	def run(self):
		for k,v in self.blds.items():
			v.run()

class local_bdist_rpm(bdist_rpm):
	def finalize_options(self):
		if not self.post_install:
			self.post_install = 'misc/redhat_post_install'
		self.fix_python = True
		bdist_rpm.finalize_options(self)

#crappy chinook hack
import sys
if "--chinook" in sys.argv:
	sys.argv.remove("--chinook")
	paths = ['/mscf/mscf/bin/',"/etc/init.d","/mscf/mscf/sbin/"]
else:
	paths = ['/usr/bin/',"/etc/init.d","/usr/sbin"]
scr = [['client/master','client/sark',
		'client/nadmin', 'client/mcehandler.py'],
		["client/master-sark","server/master-mcp"], ["server/mcp"] ]
thescripts = zip (paths,scr)


setup(name='master', version='0.1',
	author="Evan Felix",
	author_email="e@pnl.gov",
	description="An asset managment system, designed to watch the cluster and also manage its state",
	url="https://cvs.pnl.gov/mscf/wiki/MASTER",
	package_dir= {'master':'lib/master'},
	packages=['master'],

	scripts = thescripts,
	data_files = [('/etc/',['misc/mcp.conf','misc/mcp-priv.conf'])],
	#requires=['python (>=2.4)','hostparser','postgresql-python'],
	cmdclass = {
		'install_scripts': local_install_scripts,
		'build_scripts': local_build_scripts,
		'bdist_rpm':local_bdist_rpm
	}
)

