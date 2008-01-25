#!/usr/bin/python
""" A Semi-Colon separated file reader """

testformat="""

List of Controllers in the system

Controllers

ID;Status;Name;Slot ID;State;Firmware Version;Minimum Required Firmware Version;Driver Version;Minimum Required Driver Version;Number of Connectors;Rebuild Rate;BGI Rate;Check Consistency Rate;Reconstruct Rate;Alarm State;Cluster Mode;SCSI Initiator ID;Cache Memory Size;Patrol Read Mode;Patrol Read State;Patrol Read Rate;Patrol Read Iterations;
0;Non-Critical;PERC 5/i Integrated;Embedded;Degraded;5.2.1-0067;Not Applicable;00.00.03.05 ;00.00.03.13;2;30%;30%;30%;30%;Not Applicable;Not Applicable;Not Applicable;256 MB;Auto;Stopped;30%;2
1;Non-Critical;PERC 5/E Adapter;PCI Slot 1;Degraded;5.2.1-0066;Not Applicable;00.00.03.05 ;00.00.03.13;2;80%;30%;30%;30%;Enabled;Not Applicable;Not Applicable;256 MB;Auto;Stopped;30%;1
2;Non-Critical;PERC 5/E Adapter;PCI Slot 2;Degraded;5.2.1-0066;Not Applicable;00.00.03.05 ;00.00.03.13;2;30%;30%;30%;30%;Enabled;Not Applicable;Not Applicable;256 MB;Auto;Stopped;30%;0

"""

def getSSVDicts(fileobj):
    for line in fileobj:
        if line[0:3] == "ID;":
            break
    else: #uh does this work like i think?
        return []
        
    headers=line.split(";")

    return [(dict(zip(headers,line.split(";")))) for line in fileobj if len(line)>1]


def _test():
    import StringIO
    out=getSSVDicts(StringIO.StringIO(testformat))
    for i in out:
        print i

if __name__ == "__main__":
        _test()

