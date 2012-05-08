#!/usr/bin/env python
#
# Copyright © 2008,2009, Battelle Memorial Institute
# All rights reserved.
# 
# 1.	Battelle Memorial Institute (hereinafter Battelle) hereby grants permission
# 	to any person or entity lawfully obtaining a copy of this software and
# 	associated documentation files (hereinafter “the Software”) to redistribute
# 	and use the Software in source and binary forms, with or without
# 	modification.  Such person or entity may use, copy, modify, merge, publish,
# 	distribute, sublicense, and/or sell copies of the Software, and may permit
# 	others to do so, subject to the following conditions:
# 
# 	•	Redistributions of source code must retain the above copyright
# 		notice, this list of conditions and the following disclaimers. 
# 	•	Redistributions in binary form must reproduce the above copyright
# 		notice, this list of conditions and the following disclaimer in the
# 		documentation and/or other materials provided with the distribution.
# 	•	Other than as used herein, neither the name Battelle Memorial
# 		Institute or Battelle may be used in any form whatsoever without the
# 		express written consent of Battelle.  
# 	•	Redistributions of the software in any form, and publications based
# 		on work performed using the software should include the following
# 		citation as a reference:
# 
# 			(A portion of) The research was performed using EMSL, a
# 			national scientific user facility sponsored by the
# 			Department of Energy's Office of Biological and
# 			Environmental Research and located at Pacific Northwest
# 			National Laboratory.
# 
# 2.	THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# 	AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# 	IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# 	ARE DISCLAIMED. IN NO EVENT SHALL BATTELLE OR CONTRIBUTORS BE LIABLE FOR ANY
# 	DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# 	(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# 	LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# 	ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# 	(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# 	THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# 3.	The Software was produced by Battelle under Contract No. DE-AC05-76RL01830
# 	with the Department of Energy.  The U.S. Government is granted for itself
# 	and others acting on its behalf a nonexclusive, paid-up, irrevocable
# 	worldwide license in this data to reproduce, prepare derivative works,
# 	distribute copies to the public, perform publicly and display publicly, and
# 	to permit others to do so.  The specific term of the license can be
# 	identified by inquiry made to Battelle or DOE.  Neither the United States
# 	nor the United States Department of Energy, nor any of their employees,
# 	makes any warranty, express or implied, or assumes any legal liability or
# 	responsibility for the accuracy, completeness or usefulness of any data,
# 	apparatus, product or process disclosed, or represents that its use would
# 	not infringe privately owned rights.  
# 

import os
import sys
try:
	import xml.etree.ElementTree
	myelementtree = xml.etree.ElementTree
except ImportError:
	import elementtree.ElementTree
	myelementtree = elementtree.ElementTree
from util import mapit
import master
import pexpect

#globals... no threading!!!
_dicts=[]
_dict={}
_key=None


class smamgr:

	def __init__(self, server, sma):
		self.server = server
		self.sma = sma
		self.thessh = pexpect.spawn("ssh -l root -t %s sssu"%(server),timeout=300)
		#self.thessh.logfile=sys.stderr

		c=self.thessh

		c.expect("Manager:")
		c.sendline(self.sma)
		c.expect("Username:")
		c.sendline("Administrator") #should be in config
		c.expect("Password")
		c.sendline("hpinvent")

		c.expect("NoSystemSelected>")
		c.sendline("set options NOCOMMAND_DELAY DISPLAY_STATUS display_width=500")
		c.expect("NoSystemSelected>")


	def runcmdstoxml(self,*cmds):
		data=""

		for c in cmds:
			master.debug("Command:"+c)
			self.thessh.sendline(c)

			#self.thessh.expect('[A-Za-z0-9]*>')
			#self.thessh.expect('(NoSystemSelected|hsv\D)>')
			self.thessh.expect("Status : \d")
			data += self.thessh.before

		return "<wrapper>"+data+"</wrapper>"




	def runcmdstoxml_old(self,*cmds):
		#create script file
		f=open("/tmp/tmp.sssu.script","w")
		f.write("set options command_delay=0 display_width=500\n")
		f.write("select manager %s USERNAME=administrator password=hpinvent\n"%(self.sma))
		for c in cmds:
			master.debug("SMA command:"+c)
			f.write("%s\n"%(c))
		f.write("exit\n")
		f.close()
	
		#copy it
		os.system("scp -q /tmp/tmp.sssu.script %s:/tmp/tmp.sssu.script"%(self.server))

		#execute it	
		output=os.popen("""ssh %s 'sssu "file /tmp/tmp.sssu.script"'"""%(self.server),"r");
		l = output.readlines();
		
		return "<wrapper>"+''.join(l)+"</wrapper>"

		
	def gethsvinfo(self):
		map = { 'objectwwn'			:'wwn',
				'firmwareversion'	:'fwver',
				'operationalstate'	:'state',
				# 'statestring'		:'statestring', #huh?
				'totalstoragespace'	:'totalspace',
				'usedstoragespace'	:'usedspace',
				'availablestoragespace':	'availablespace',
				'operationalstatedetail':	'statedetail' }

	
		hsvs={}
		#e = xml.etree.ElementTree.fromstring(self.runcmdstoxml("ls system full xml"))
		e = myelementtree.fromstring(self.runcmdstoxml("ls system full xml"))
		for o in e.getiterator("object"):
			d={}
			for k,v in map.items():
				d[v] = o.find(k).text

			d.update(self.getcontrollerinfo(o.findtext("objectname")))
			d.update(self.getdiskshelfinfo(o.findtext("objectname")))
			d.update(self.getdiskinfo(o.findtext("objectname")))
			d.update(self.getvdiskinfo(o.findtext("objectname")))

			hsvs[o.find("objectname").text]=d

		return hsvs

	def getvdiskinfo(self,hsvname):
		map = { 'onlinecontroller/controllername'          :'onlinecontroller',
				'operationalstate'		:'state',
				'operationalstatedetail':	'statedetail' }

		e = myelementtree.fromstring(self.runcmdstoxml("select cell %s"%(hsvname),"ls vdisk full xml"))
		d={}

		for o in e.getiterator("object"):
			e=o.findtext("familyname")
			prefix=e+"."

			for k,v in map.items():
				d[prefix+v] = o.findtext(k)

		return d

	def getdiskshelfinfo(self,hsvname):
		map = { 'operationalstate'		: 'state',
				'wwnodename'			: 'wwn',
				'looppair'				: 'looppair',
				'emu/operationalstate'	: 'emu.state',
				'emu/firmwareversion'	: 'emu.fwver',
				'operationalstatedetail':	'statedetail' }

		e = myelementtree.fromstring(self.runcmdstoxml("select cell %s"%(hsvname),"ls diskshelf full xml"))
		d={}

		for o in e.getiterator("object"):
			e=o.findtext("diskshelfname")
			if e:
				e=e.replace("Disk Enclosure ","diskenclosure")
			else:
				e="UnknownDiskShelf_"+o.findtext("wwnodename")
			prefix=e+"."

			for k,v in map.items():
				d[prefix+v] = o.findtext(k)

			for e in o.findall("powersupplies/powersupply"):
				d[prefix+e.findtext("name")]=e.findtext("operationalstate")

			for e in o.findall("cooling/sensors/sensor"):
				d[prefix+e.findtext("name")]=e.findtext("operationalstate")

			for e in o.findall("cooling/fans/fan"):
				d[prefix+e.findtext("name")]=e.findtext("operationalstate")
				d[prefix+e.findtext("name")+".speed"]=e.findtext("speed")

			#for e in o.findall("diskslotstatus/diskslot"):
			#	d[prefix+e.findtext("name")]=e.findtext("state")
			#	d[prefix+e.findtext("name")+".disk"]=e.findtext("diskstatus")

		return d

	def getdiskinfo(self,hsvname):

		map = { 'nodewwid'			:'wwid',
				'firmwareversion'		:'fwver',
				'operationalstate'		:'state',
				'modelnumber'			:'model',
				'formattedcapacity'	: 'capacity',
				'migrationstate'		: 'migrationstate',
				'diskbaynumber'			: 'diskbay',
				'shelfnumber'			: 'shelfnumber',
				'operationalstatedetail':	'statedetail' }


		e = myelementtree.fromstring(self.runcmdstoxml("select cell %s"%(hsvname),"ls disk full xml"))
		d={}

		for o in e.getiterator("object"):
			c=o.findtext("diskname")
			if c:
				c=c.replace("Disk ","disk")
			else:
				c="UnknownDisk_"+o.findtext("nodewwid") # not sure if this will catch things right
			prefix=c+"."

			for k,v in map.items():
				d[prefix+v] = o.findtext(k)

			for e in o.findall("loops/loop"):  
				d[prefix+e.findtext("loopname")]=e.findtext("loopstate")

		return d

	def getcontrollerinfo(self,hsvname):

		map = { 'serialnumber'			:'serial',
				'firmwareversion'		:'fwver',
				'operationalstate'		:'state',
				'modelnumber'			:'model',
				'controllertemperaturestatus'	: 'tempstatus',
				'operationalstatedetail':	'statedetail' }


		e = myelementtree.fromstring(self.runcmdstoxml("select cell %s"%(hsvname),"ls controller full xml"))
		d={}

		for o in e.getiterator("object"):
			c=o.findtext("controllername")
			c=c.replace("Controller ","controller")
			prefix=c+"."

			for k,v in map.items():
				d[prefix+v] = o.findtext(k)

			for e in o.findall("fans/fan"):
				d[prefix+e.findtext("fanname")]=e.findtext("status")

			for e in o.findall("powersources/source"):
				d[prefix+e.findtext("type")]=e.findtext("state")

			for e in o.findall("hostports/hostport"):
				d[prefix+e.findtext("portname")]=e.findtext("operationalstate")

			for e in o.findall("deviceports/deviceport")[:2]:  # only first two are used in our EVA's
				d[prefix+e.findtext("portname")]=e.findtext("operationalstate")

			for e in o.findall("cachebattery/modules")[0:0]:  # only first one is used in our EVA's
				d[prefix+e.findtext("name")]=e.findtext("operationalstate")

		return d


def get_hsv_info(ioserver,hosts):
	d={};
	
	for h in hosts:
		s = smamgr(ioserver,h);
		d.update(s.gethsvinfo())

	return d


if __name__ == "__main__":
	s = smamgr("tio1","tsma");

	for k,v in s.gethsvinfo().items():
		print k
		for dk,dv in v.items():
			print "\t",dk,dv

	#x = "<wrapper>"+s.runcmdstoxml(sma,"ls system full xml")+"</wrapper>"
	#print x
	#e = xml.etree.ElementTree.fromstring(x)
	#for o in e.getiterator("object"):
	#	print o.find("statestring").text

