#!/bin/bash


# Author: Brock Erwin

cd `dirname $0`

if [ x$1 = x ]; then
	release=1
else
	release=$1
fi

# This should be a comma separated list of required RPM packages
required_rpms="hostparser, python-twisted-core, python-twisted-names, python-twisted-web, postgresql-python"


# I would like to just use distutils, but I don't think there is a way to force the RPM spec file to add the Requires
# Keyword in the specfile


rpmbuild_cmd=`python setup.py bdist_rpm --release="$release" | grep rpmbuild`

rpmbuild_cmd=`echo $rpmbuild_cmd | sed "s+--define \(.*\) --+--define '\1' --+g"`

spec_file=`find build -name '*.spec'`

# Add a requirement to the .spec file - this package requires python-ply
cp $spec_file /tmp/orig.spec
echo 'Requires: '$required_rpms > $spec_file
cat /tmp/orig.spec >> $spec_file

echo running $rpmbuild_cmd
eval $rpmbuild_cmd

echo
echo '***************************************************************'
echo '* your built rpm is now in build/*/rpm/RPMS/*master*.rpm  *'
echo '***************************************************************'
