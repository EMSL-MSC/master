#!/usr/bin/python
#vim: noet:ts=4:sw=4

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
        print "DebugCommands(%s)"% (args,)

    def get_node_status(self, nodename):
        print "get_node_status(%s)"% nodename

    def get_nodes_status(self, nodelist):
        print "get_nodes_status(%s)"% (nodelist,)

    def check_nodes_in_use(self, nodelist=[]):
        print "check_nodes_in_use(%s)"% (nodelist,)

    def mark_nodes_for_maint(self, comment, nodelist=[]):
        print "mark_nodes_for_maint(%s, %s)"% (comment, nodelist,)

    def mark_nodes_available(self, comment, nodelist=[]):
        print "mark_nodes_available(%s, %s)"% (comment, nodelist,)


class SlurmCommands(ClusterCommands):
	def __init__(self, scontrol_bin='/usr/bin/scontrol'):
		if not os.access(scontrol_bin, os.X_OK):
			raise AssertionError("%s is not executable or does not exist."% scontrol_bin)
		self.scontrol_bin = scontrol_bin
		self.scontrol_cmd = self.scontrol_bin + ' -a show node "%s"'

	def get_node_status(self, nodename):
		(child_stdin, child_stdout) = os.popen2('%s "%s"'% (self.scontrol_cmd, nodename))
		return self.parse_slurm_output(child_stdout)[nodename]
	
	def get_nodes_status(self, nodelist):
		(child_stdin, child_stdout) = os.popen2(self.scontrol_cmd% (' '.join(nodelist)))
		return self.parse_slurm_output(child_stdout)

	def check_nodes_in_use(self, nodelist=[]):
		if len(nodelist) == 0:
			(child_stdin, child_stdout) = os.popen2('%s show node'% self.scontrol_bin)
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
		cmd = '%s update NodeName="%s" State="DRAIN" Reason="%s"'% (
				self.scontrol_bin,
				' '.join(nodelist),
				comment)
		cmd_result = os.system(cmd)
		return cmd_result
	
	def mark_nodes_available(self, nodelist, comment=''):
		cmd = '%s update NodeName="%s" State="RESUME"'% (
				self.scontrol_bin,
				' '.join(nodelist))
		if comment != '':
			cmd += ' Reason="%s"'% (comment,)
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
