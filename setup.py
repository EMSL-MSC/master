#!/usr/bin/python
# vim: noet:ts=4:sw=4

#from setuptools import setup,find_packages
import sys
import tempfile
from distutils import sysconfig
from distutils.core import setup, Distribution
from distutils.command.install_scripts import install_scripts
from distutils.command.build_scripts import build_scripts
from distutils.command.bdist_rpm import bdist_rpm

def committed_rev():
	try:
		import pysvn,os,sys
		client = pysvn.Client()
		revs = []
		for root, dirs, files in os.walk(sys.path[0]):
			if '.svn' in dirs:
				dirs.remove('.svn')

			for f in files:
				try:
					entry = client.info(os.path.join(root,f))

					if not entry or entry.commit_revision.kind !=  pysvn.opt_revision_kind.number:
						raise Exception("Entry not in subversion.")
					revs.append(entry.commit_revision.number)
				except:
					pass
		return max(revs)
	except Exception, msg:
		try:
			import _version

			return int(_version.revision)
		except:
			print "Unable to read _version."
			pass
		print msg,
		print '-- aborting search for subversion repository revision number'
		return 0

class svnDistribution(Distribution):
	def __init__(self, attrs):
		build_num = committed_rev()
		if build_num:
			attrs['revision'] = '%i'% build_num
			attrs['version'] = '%s_r%s'% (attrs['version'],attrs['revision'])
			try:
				filename, format = attrs['version_file']
				file(filename, 'w').write(format% (build_num,attrs['version']))
			except KeyError:
				pass
		try:
			del attrs['version_file']
		except KeyError:
			pass
		try:
			del attrs['revision']
		except KeyError:
			pass
		Distribution.__init__(self, attrs)
		

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

		#little hack to avoid pyc and pyo files
		filename=tempfile.mkstemp()[1]
		print filename
		string='%s setup.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES\n'%(sys.executable)
		string+="sed -i -e 's/\(.*\.py$\)/\\1\\n\\1c\\n\\1o/' INSTALLED_FILES\n"
		o=open(filename,'w')
		o.write(string)
		o.close()
		self.install_script = filename
		#end hack

		bdist_rpm.finalize_options(self)

#crappy chinook hack
import sys
if "--chinook" in sys.argv:
	sys.argv.remove("--chinook")
	binDir = '/mscf/mscf/bin'
	sbinDir = '/mscf/mscf/sbin'
else:
	binDir = '/usr/bin'
	sbinDir = '/usr/sbin'

paths = [ '%s/' % binDir, "/etc/init.d", "%s/" % sbinDir ]
scr = [['client/master','client/sark','client/sark-sma',
		'client/nadmin', 'client/mcehandler'],
		["client/master-sark","server/master-mcp"], ["server/mcp"] ]
thescripts = zip (paths,scr)

mcp_bin_dirs = open('misc/mcp-bin-dirs.sh', 'w')
mcp_bin_dirs.write('#!/bin/sh\nexport MASTER_BIN_DIR=%s\nexport MASTER_SBIN_DIR=%s\n' % (binDir, sbinDir))
mcp_bin_dirs.close()

setup(name='master', version='0.4',
	author="Evan Felix",
	author_email="e@pnl.gov",
	description="An asset managment system, designed to watch the cluster and also manage its state",
	url="https://cvs.pnl.gov/mscf/wiki/MASTER",
	package_dir= {'master':'lib/master'},
	packages=['master'],
	distclass=svnDistribution,

	scripts = thescripts,
	data_files = [('/etc/',['misc/mcp.conf','misc/mcp-priv.conf','misc/mcp-bin-dirs.sh'])],
	#requires=['python (>=2.4)','hostparser','postgresql-python'],
	cmdclass = {
		'install_scripts': local_install_scripts,
		'build_scripts': local_build_scripts,
		'bdist_rpm':local_bdist_rpm
	}
)

