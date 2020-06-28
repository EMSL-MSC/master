#!/usr/bin/python
# -*- coding: UTF-8 -*-
# vim: noet:ts=4:sw=4
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


class ClusterCommands(object):
	def get_node_status(self, nodename):
		"""get_node_status(nodename) -> string

		Returns a string representing the status of this node.
		"""
		raise NotImplementedError

	def get_nodes_status(self, nodelist):
		"""get_nodes_status(nodelist) -> dictionary

		Returns a dictionary of (nodename, status) pairs.
		"""
		raise NotImplementedError

	def check_nodes_in_use(self, nodelist=[]):
		"""check_nodes_in_use(nodelist) -> dictionary

		Returns a dictionary of (nodename, boolean) pairs
		True indicating a node is in use False indicating it is
		not currently used.
		"""
		raise NotImplementedError

	def mark_nodes_for_maint(self, comment, nodelist=[]):
		"""mark_nodes_for_main(nodelist) -> Int

		Sets the nodes into a pending maintenance mode in the
		cluster's node control mechanism.

		Returns 0 on Success > 0 on failure.
		"""
		raise NotImplementedError

	def mark_nodes_available(self, comment, nodelist=[]):
		"""mark_nodes_available(nodelist) -> None

		Sets the nodes into an available status is the cluster's
		node control mechanism.

		Return 0 on Success > 0 on failure.
		"""
		raise NotImplementedError


class DebugCommands(ClusterCommands):
    def __init__(self, *args):
        print "DebugCommands(%s)" % (args,)

    def get_node_status(self, nodename):
        print "get_node_status(%s)" % nodename

    def get_nodes_status(self, nodelist):
        print "get_nodes_status(%s)" % (nodelist,)

    def check_nodes_in_use(self, nodelist=[]):
        print "check_nodes_in_use(%s)" % (nodelist,)

    def mark_nodes_for_maint(self, comment, nodelist=[]):
        print "mark_nodes_for_maint(%s, %s)" % (comment, nodelist,)

    def mark_nodes_available(self, comment, nodelist=[]):
        print "mark_nodes_available(%s, %s)" % (comment, nodelist,)


class SlurmCommands(ClusterCommands):
	def __init__(self, scontrol_bin='/usr/bin/scontrol'):
		if not os.access(scontrol_bin, os.X_OK):
			raise AssertionError(
				"%s is not executable or does not exist." % scontrol_bin)
		self.scontrol_bin = scontrol_bin
		self.scontrol_cmd = self.scontrol_bin + ' -a show node "%s"'

	def get_node_status(self, nodename):
		(child_stdin, child_stdout) = os.popen2(
			'%s "%s"' % (self.scontrol_cmd, nodename))
		return self.parse_slurm_output(child_stdout)[nodename]

	def get_nodes_status(self, nodelist):
		(child_stdin, child_stdout) = os.popen2(
			self.scontrol_cmd % (' '.join(nodelist)))
		return self.parse_slurm_output(child_stdout)

	def check_nodes_in_use(self, nodelist=[]):
		if len(nodelist) == 0:
			(child_stdin, child_stdout) = os.popen2('%s show node' % self.scontrol_bin)
			nodestatus = self.parse_slurm_output(child_stdout)
		else:
			nodestatus = self.get_nodes_status(nodelist)
		for (node, state) in nodestatus.iteritems():
			if state.find('ALLOC') < 0 and (state.find('DRAIN') >= 0 or state.find('DOWN') >= 0):
				nodestatus[node] = False
			else:
				nodestatus[node] = True
		return nodestatus

	def mark_nodes_for_maint(self, comment, nodelist):
		comment = comment.replace('"', '\\"')
		nodelist = ' '.join(nodelist).replace('"', '\\"')
		cmd = '%s update NodeName="%s" State="DRAIN" Reason="%s"' % (
                    self.scontrol_bin,
                    nodelist,
                    comment)
		cmd_result = os.system(cmd)
		return cmd_result

	def mark_nodes_available(self, nodelist, comment=''):
		comment = comment.replace('"', '\\"')
		nodelist = ' '.join(nodelist).replace('"', '\\"')
		cmd = '%s update NodeName="%s" State="RESUME"' % (
                    self.scontrol_bin,
                    nodelist)
		if comment != '':
			cmd += ' Reason="%s"' % (comment,)
		return os.system(cmd)

	def parse_slurm_output(self, fhandle):
		retval = {}
		line = fhandle.readline().strip()
		while line:
			if line.startswith('NodeName'):
				line += fhandle.readline().strip()
				lparts = line.split()
				try:
					node_name = lparts[0].split('=')[1].strip()
					state = lparts[1].split('=')[1]
					retval[node_name] = state
				except IndexError:
					pass
			line = fhandle.readline().strip()
		return retval
