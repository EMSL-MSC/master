#!/usr/bin/env python3

# This file is part of the MASTER project and is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.

# this file depends on the DDN SFA management API


import sys
from ddn.sfa.api import *
from ddn.sfa.tools import *
from logging import *

_systemProps = (
	"HealthState",
)
_slotProps = (
	"HealthState",
	"Fault",
	"PredictFailure",
	"Present",
)
_expanderProps = (
	"HealthState",
	"Fault",
	"PredictFailure",
	"Present",
	"FirmwareVersion",
	"Location",
)
_sepProps = (
    "HealthState",
    "PredictFailure",
    "Present",
    "FirmwareVersion",
    "Location",
    "SerialNumber",
)
_internalDiskProps = {
	"HealthState",
	"Model",
	"SerialNumber",
	"Version",
	"Fault",
}
_diskProps = (
	"HealthState",
	"DiskHealthState",
	"Failed",
	"InterposerBootLoaderVersion",
	"InterposerConfigDataVersion",
	"InterposerFWRevision",
	"InterposerHWRevision",
	"InterposerProductID",
	"InterposerProductRevision",
	"InterposerSerialNumber",
	"MemberState",
	"ProductID",
	"ProductRevision",
	"RotationSpeed",
	"SerialNumber",
	"State",
	"VendorID",
)
_enclosureProps = (
	"BaseboardSerialNumber",
	"BaseboardVersion",
	"BiosVersion",
	"BmcVersion",
	"ChassisSerialNumber",
	"FirmwareVersion",
	"HealthState",
	"Manufacturer",
	"Model",
	"PredictFailure",
	"Revision",
	"SerialNumber",
	"Version",
)
_controllerProps = (
	"FWSourceVersion",
	"FWRelease",
	"HealthState",
	"Manufacturer",
	"Primary",
	"State",
	"Name",
	"SerialNumber",
)
_upsProps = (
	"ACFailure",
	"Enabled",
	"EstimatedRunTime",
	"Fault",
	"FirmwareVersion",
	"HealthState",
	"PartNumber",
	"PredictFailure",
	"Present",
	"SerialNumber",
	"UPSFailure",
	"WarningStatus",
)
_powerProps = (
	"ACFailure",
	"DCFailure",
	"Fault",
	"FirmwareVersion",
	"HardwareRevision",
	"HealthState",
	"PartNumber",
	"PowerState",
	"Location",
	"PredictFailure",
	"Present",
	"SerialNumber",
	"TemperatureFailure",
	"TemperatureWarning",
)
_fanProps = (
	"Fault",
	"HealthState",
	"Location",
	"Position",
	"PoweredOn",
	"PredictFailure",
	"Present",
)
_poolProps = (
	"HealthState",
	"NumDisks",
	"RebuildJobsPresent",
	"MemberCount",
)
_virtualdiskProps = {
	"BadBlockCount",
	"HealthState",
	"RebuildJobsPresent",
	"MemberCount",
	"State",
}
_vitualmachineProps = {
	"CoreCount",
	"HealthState",
	"Image",
	"IOCMACAddresses",
	"IsRunning",
}

def main():
	s = SFAController.getAll()
	for i in s:
		i.writeProperties(sys.stdout)


def dumpKeys():
	for c in (SFAController, SFADiskDrive, SFADiskSlot, SFAEnclosure, SFAExpander, SFAFan, SFAPowerSupply, SFAStoragePool, SFAStorageSystem, SFAUPS,SFAInternalDiskDrive,SFAVirtualDisk,SFAVirtualMachine):
		print(c)
		item = c.getAll()[0]
		keys = item.cimProps
		for key in sorted(keys.keys()):
			try:
				print("  %-40s   %s" % (key, item.__getattribute__(key)))
			except AttributeError as msg:
				print("  ", key, msg)
			except APIClientException as msg:
				print("  ", key, msg)
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
		d[f"{prefix}.{p}"] = str(v)
	return d


def dumpPools():
	d = {}
	list = SFAStoragePool.getAll()
	for item in list:
		p = "pool." + str(item.Name)
		d.update(dumpProps(p, item, _poolProps))
	return d

def dumpDisks():
	d = {}
	list = SFADiskDrive.getAll()
	for item in list:
		p = f"enclosure{str(item.EnclosureIndex)}.disk{str(item.DiskSlotNumber)}"
		d.update(dumpProps(p, item, _diskProps))
	return d


def dumpEncPart(cls, prefix, props):
	d = {}
	list = cls.getAll()
	for item in list:
		p = f"enclosure{str(item.EnclosureIndex)}.{prefix}{str(item.Position)}"
		d.update(dumpProps(p, item, props))
	return d


def dumpSimple(cls, prefix, props):
	d = {}
	list = cls.getAll()
	for item in list:
		p = prefix + str(item.Index)
		d.update(dumpProps(p, item, props))
	return d


def gatherSFAInfo(hostlist, user, password):
	d = {}

	for host in hostlist:
		try:
			APIConnect("https://" + host, auth=(user, password))

			d.update(dumpSimple(SFAEnclosure, "enclosure", _enclosureProps))
			d.update(dumpSimple(SFAController, "controller", _controllerProps))
			d.update(dumpSimple(SFAStorageSystem, "system", _systemProps))
			d.update(dumpDisks())
			d.update(dumpEncPart(SFADiskSlot, "slot", _slotProps))
			d.update(dumpEncPart(SFAUPS, "ups", _upsProps))
			d.update(dumpEncPart(SFAPowerSupply, "power", _powerProps))
			d.update(dumpEncPart(SFAFan, "fan", _fanProps))
			d.update(dumpEncPart(SFAExpander, "expander", _expanderProps))
			d.update(dumpEncPart(SFASEP, "sep", _sepProps))
			d.update(dumpEncPart(SFAInternalDiskDrive,"internaldisk",_internalDiskProps))
			d.update(dumpPools())
			d.update(dumpSimple(SFAVirtualDisk,"virtualdisk",_virtualdiskProps))
			d.update(dumpSimple(SFAVirtualMachine,"virtualmachine",_vitualmachineProps))
			break
		except APIException as msg:
			print("Error", msg)
		finally:
			APIDisconnect()
	return d


if __name__ == "__main__":
	#APIConnect("https://172.22.128.43", auth=("user", "user"))
	# main()
	#dumpSimple(SFAEnclosure, "enclosure", _enclosureProps)
	#dumpSimple(SFAController, "controller", _controllerProps)
	#dumpSimple(SFAStorageSystem, "system", _systemProps)
	#dumpDisks()
	#dumpEncPart(SFADiskSlot, "slot", _slotProps)
	#dumpEncPart(SFAUPS, "ups", _upsProps)
	#dumpEncPart(SFAPowerSupply, "power", _powerProps)
	#dumpEncPart(SFAFan, "fan", _fanProps)
	#dumpEncPart(SFAExpander, "expander", _expanderProps)
	#dumpEncPart(SFASEP, "sep", _sepProps)
	#dumpPools()
	#dumpEncPart(SFAInternalDiskDrive,"internaldisk",_internalDiskProps)
	#dumpSimple(SFAVirtualDisk,"virtualdisk",_virtualdiskProps)
	#dumpSimple(SFAVirtualMachine,"virtualmachine",_vitualmachineProps)
			#dumpKeys()
	d=gatherSFAInfo(["172.22.128.43","172.22.128.44"],"user","user")
	for k,v in d.items():
		print(k,":",v)
	APIDisconnect()
