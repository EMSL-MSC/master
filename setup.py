#!/usr/bin/env python3
# vim: noet:ts=4:sw=4

#from setuptools import setup,find_packages
import sys
import tempfile
from distutils import sysconfig
from distutils.core import setup, Distribution
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
		l = []
		for k, v in self.blds.items():
			print(k, v)
			l += v.scripts
		return l

	def mkbld(self, thedir):
		b = build_scripts(self.distribution)
		b.build_dir = self.build_dir + thedir
		b.scripts = []
		b.force = self.force
		if sysconfig.get_config_var("VERSION") != "2.3":
			b.executable = self.executable
		b.outfiles = None
		return b

	def finalize_options(self):
		build_scripts.finalize_options(self)
		# build up a dictionary of commands for sub scripting
		self.blds = {}

		for d, files in self.scripts:
			if d not in self.blds:
				self.blds[d] = self.mkbld(d)
			self.blds[d].scripts += files

		# for k,v in self.blds.items():
		#	print k,'=>',self.blds[k].scripts,self.blds[k].build_dir

	def run(self):
		for k, v in self.blds.items():
			v.run()


class local_bdist_rpm(bdist_rpm):
	def finalize_options(self):
		if not self.post_install:
			self.post_install = 'misc/redhat_post_install'
		self.fix_python = True

		bdist_rpm.finalize_options(self)


binDir = '/usr/bin'
sbinDir = '/usr/sbin'

paths = [f'{binDir}/', "/usr/lib/systemd/system/", f"{sbinDir}/"]
scr = [['client/master', 'client/sark', 'client/sark-sma',
        'client/nadmin', 'client/mcehandler', 'client/sark-ddn'],
       ["client/master-sark.service", "server/master-mcp.service"], ["server/mcp"]]
thescripts = list(zip(paths, scr))

mcp_bin_dirs = open('misc/mcp-bin-dirs.sh', 'w')
mcp_bin_dirs.write(
	f'#!/bin/sh\nexport MASTER_BIN_DIR={binDir}\nexport MASTER_SBIN_DIR={sbinDir}\n')
mcp_bin_dirs.close()

setup(name='master', version='0.19',
      author="Evan Felix",
      author_email="e@pnl.gov",
      description="An asset managment system, designed to watch the cluster and also manage its state",
      url="https://gitlab.emsl.pnl.gov/msc_ops/master",
      package_dir={'master': 'lib/master'},
      packages=['master'],
      # distclass=svnDistribution,

      scripts=thescripts,
      data_files=[('/etc/', ['misc/mcp.conf', 'misc/mcp-priv.conf',
                             'misc/mcp-bin-dirs.sh']), ('/usr/share/master/', ['server/master.sql', 'server/master-data.sql'])],
      #requires=['python (>=2.4)','hostlist','postgresql-python'],
      cmdclass={
          'install_scripts': local_install_scripts,
          'build_scripts': local_build_scripts,
          'bdist_rpm': local_bdist_rpm
      }
      )
