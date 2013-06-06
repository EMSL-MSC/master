%define name master
%define version 0.2

Summary: An asset managment system, designed to watch the cluster and also manage its state
Name: %{name}
Version: %{version}
Release: 1%{?dist}
Source0: %{name}-%{version}.tar.gz
License: UNKNOWN
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Url: https://cvs.pnl.gov/mscf/wiki/MASTER
BuildRequires: python2-devel
#BuildRequires: tcl-devel
#BuildRequires: tk-devel
Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts

%description
UNKNOWN

%if 0%{?rhel} && 0%{?rhel} <= 5
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif




%prep
%setup

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --root=%{buildroot} 


%clean
rm -rf %{buildroot}

%post
# This adds the proper /etc/rc*.d links for the script
/sbin/chkconfig --add master-sark

%preun
if [ $1 -eq 0 ] ; then
    /sbin/service master-sark stop >/dev/null 2>&1
    /sbin/chkconfig --del master-sark
fi


%files
%defattr(-,root,root)
%{_bindir}/*
%{_sysconfdir}/init.d/master*
%{_sysconfdir}/mcp*
#%{python_sitearch}/%{name}/*
%{_sbindir}/*
