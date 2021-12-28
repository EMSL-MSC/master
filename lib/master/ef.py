#!/usr/bin/python

# This file is part of the MASTER project and is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.

# this file depends on the DDN SFA management API mondified to work with the ef3015 array
# it will probably work with many of the arrays by dothill.com that are brnaded by various vendors
# it takes directly to the SMI-S port and gathers various information controlled by the Props tuples
import sys
from ddn.ef.api import *
from ddn.ef.tools import *

_ControllerProps = (
	'ElementName',
	'HealthState',
	'Name',
)
_DiskSoftwareIdentityProps = (
	'SerialNumber',
	'VersionString',
	'Manufacturer',
)
_ControllerSoftwareIdentityProps = (
	'ElementName',
	'VersionString',
	'Manufacturer',
)
_DiskDriveProps = (
	'HealthState',
	'DiskType',
)
_VolumeProps = (
	'HealthState',
	'NoSinglePointOfFailure',
	'CurrentOwner',
)
_PSUProps = (
	'HealthState',
	'Name',
)
_PSUFanProps = (
	'HealthState',
	'Name',
)
_DiskSASPortProps = (
	'HealthState',
)
_SASPortProps = (
	'HealthState',
)
_TopComputerSystemProductProps = (
	'ElementName',
	'Version',
)
_FCPortProps = (
	'HealthState',
	'Name',
	'ElementName',
	'PermanentAddress',
	'Speed',
)
_PSUPhysicalPackageProps = (
	'SerialNumber',
	'HealthState',
	'PartNumber',
)


def emit(key, value):
	print(key, "=", value)


def main():

	# s=DiskSoftwareIdentity.getAll()
	# s=Controller.getAll()
	# s=ControllerSoftwareIdentity.getAll()
	# s=DiskDrive.getAll()
	# s=Volume.getAll()
	s = TopComputerSystemProduct.getAll()
	for i in s:
		i.writeProperties(sys.stdout)


def dumpKeys(code=False):
	for c in (Controller, DiskSoftwareIdentity, ControllerSoftwareIdentity, DiskDrive, Volume, PSU, PSUFan, DiskExtent, DiskSASPort, SASPort, TopComputerSystemProduct, FCPort, PSUPhysicalPackage):
		item = c.getAll()[0]
		if code:
			print("_" + item.cimName[4:] + "Props = (")
			for k in list(c.cimProps.keys()):
				print("\t'" + k + "'")
			print(")")
		else:
			print(c)
			item.writeProperties(sys.stdout)

		print("\f")


def dumpProps(prefix, item, props):
	d = {}
	for p in props:
		v = item.__getattribute__(p)
		try:
			# deal with API enums
			v = next((key for key, val in v.values.items() if v == val), "BADVALUE")
		except AttributeError:
			# take the value as it stands
			pass
		d[prefix + "." + p] = str(v)
	return d


def dumpControllers():
	d = {}
	list = Controller.getAll()
	for item in list:
		p = "controller" + str(item.ElementName).replace("Controller ", "")
		d.update(dumpProps(p, item, _ControllerProps))
	return d


def dumpBasic(cls, prefix, props):
	d = {}
	list = cls.getAll()
	for item in list:
		p = prefix
		d.update(dumpProps(p, item, props))
	return d


def dumpSimpleName(cls, prefix, props):
	d = {}
	list = cls.getAll()
	for item in list:
		p = prefix + str(item.Name)
		d.update(dumpProps(p, item, props))
	return d


def dumpSimple(cls, prefix, props):
	d = {}
	list = cls.getAll()
	for item in list:
		p = prefix + str(item.ElementName)
		d.update(dumpProps(p, item, props))
	return d


def gatherEFInfo(hostlist, user, password):
	d = {}

	for host in hostlist:
		try:
			APIConnect("https://" + host, auth=(user, password))
			d.update(dumpControllers())
			d.update(dumpSimple(DiskSoftwareIdentity, "", _DiskSoftwareIdentityProps))
			d.update(dumpSimple(DiskDrive, "", _DiskDriveProps))
			d.update(dumpSimple(Volume, "volume.", _VolumeProps))
			d.update(dumpSimple(PSU, "", _PSUProps))
			d.update(dumpSimple(PSUFan, "", _PSUFanProps))
			d.update(dumpSimple(PSUPhysicalPackage, "", _PSUPhysicalPackageProps))
			d.update(dumpSimple(DiskSASPort, "disksasport", _DiskSASPortProps))
			d.update(dumpSimpleName(FCPort, "fcport", _FCPortProps))
			d.update(dumpBasic(TopComputerSystemProduct,
                            "system", _TopComputerSystemProductProps))
			break
		except APIException as msg:
			print("Error", msg)
		APIDisconnect()
	return d


if __name__ == "__main__":
	APIConnect("https://ef3015-a", auth=("manage", "!manage"))
	# main()
	# dumpControllers()
	# dumpSimple(DiskSoftwareIdentity,"",_DiskSoftwareIdentityProps)
	# dumpSimple(DiskDrive,"",_DiskDriveProps)
	# dumpSimple(Volume,"volume.",_VolumeProps)
	# dumpSimple(PSU,"",_PSUProps)
	# dumpSimple(PSUFan,"",_PSUFanProps)
	# dumpSimple(PSUPhysicalPackage,"",_PSUPhysicalPackageProps)
	# dumpSimple(DiskSASPort,"disksasport",_DiskSASPortProps)
	# dumpSimpleName(FCPort,"fcport",_FCPortProps)
	# dumpBasic(TopComputerSystemProduct,"system",_TopComputerSystemProductProps)
	dumpKeys()
	APIDisconnect()
