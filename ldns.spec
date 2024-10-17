%define major 1
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}

%define build_python 1

Summary:	Lowlevel DNS(SEC) library with API
Name:		ldns
Version:	1.6.13
Release:	2
License:	BSD
Group:		System/Libraries
URL:		https://www.nlnetlabs.nl/ldns/
Source0:	http://www.nlnetlabs.nl/downloads/ldns/ldns-%{version}.tar.gz
Patch0:		ldns-1.6.11-avoid-version.diff
Patch1:		ldns-1.6.11-build_only_once.diff
BuildRequires:	automake autoconf libtool
BuildRequires:	openssl-devel
BuildRequires:	doxygen
%if %{build_python}
BuildRequires:	swig
BuildRequires:	python-devel
%endif

%description
ldns is a library with the aim to simplify DNS programing in C. All
lowlevel DNS/DNSSEC operations are supported. We also define a higher
level API which allows a programmer to (for instance) create or sign
packets.

%package -n	%{name}-utils
Summary:	DNS(SEC) utility
Group:		Networking/Other

%description -n	%{name}-utils
This package contains various utilities used to manage
and validate DNSSEC zones using ldns library. 

%package -n	%{libname}
Summary:	Lowlevel DNS(SEC) library with API
Group:		System/Libraries

%description -n	%{libname}
ldns is a library with the aim to simplify DNS programing in C. All
lowlevel DNS/DNSSEC operations are supported. We also define a higher
level API which allows a programmer to (for instance) create or sign
packets.

%package -n	%{develname}
Summary:	Development package that includes the ldns header files
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{develname}
The devel package contains the ldns library and the include files

%if %{build_python}
%package -n 	python-%{name}
Summary:	Python extensions for ldns
Group:		Development/Python

%description -n python-%{name}
Python extensions for ldns
%endif

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure2_5x \
	--disable-rpath \
%if %{build_python}
        --with-pyldns \
%endif
	--disable-static

( cd examples ; %configure2_5x --disable-rpath )
( cd drill ; %configure2_5x --disable-rpath )

%make
( cd examples ; %make )
( cd drill ; %make )

%install
%makeinstall_std
( cd examples ; %makeinstall_std )
( cd drill ; %makeinstall_std )

# cleanup and fix --short-circuit
rm -rf docs; mkdir -p docs
cp -rp doc docs/
rm -rf docs/doc/man
rm -f docs/doc/doxyparse.pl
rm -f docs/doc/ldns_manpages
rm -rf docs/doc/.svn

#we don't want these
find %{buildroot} -name "*.la" -exec rm -rf {} \;

%if %{build_python}
#remove executable bit
chmod a-x %{buildroot}%{py_platsitedir}/*py
%endif

%files -n %{libname}
%doc README LICENSE 
%{_libdir}/lib*so.%{major}*

%files -n %{develname}
%doc docs/* Changelog README
%dir %{_includedir}/ldns
%{_includedir}/ldns/*
%{_libdir}/lib*.so
%{_mandir}/man3/*
%{_bindir}/%{name}-config

%files -n %{name}-utils
%{_bindir}/*
%exclude %{_bindir}/%{name}-config
%{_mandir}/man1/*

%if %{build_python}
%files -n python-%{name}
%{py_platsitedir}/*
%endif


%changelog
* Mon Jul 16 2012 Alexander Khrukin <akhrukin@mandriva.org> 1.6.13-1
+ Revision: 809816
- version update 1.6.13

* Wed Jan 11 2012 Alexander Khrukin <akhrukin@mandriva.org> 1.6.12-1
+ Revision: 760141
- version update 1.6.12

* Sat Nov 05 2011 Oden Eriksson <oeriksson@mandriva.com> 1.6.11-2
+ Revision: 719584
- bump release
- fix build
- 1.6.11 (fixes CVE-2011-3581)

* Sun Jun 12 2011 Oden Eriksson <oeriksson@mandriva.com> 1.6.10-1
+ Revision: 684325
- 1.6.10

* Wed Jun 01 2011 Oden Eriksson <oeriksson@mandriva.com> 1.6.9-1
+ Revision: 682253
- 1.6.9

* Wed Mar 16 2011 Stéphane Téletchéa <steletch@mandriva.org> 1.6.8-1
+ Revision: 645249
- update to new version 1.6.8

* Fri Oct 29 2010 Michael Scherer <misc@mandriva.org> 1.6.6-3mdv2011.0
+ Revision: 590007
- rebuild for python 2.7

* Mon Oct 25 2010 Jani Välimaa <wally@mandriva.org> 1.6.6-2mdv2011.0
+ Revision: 589267
- add more conditionals for building python subpackage

* Mon Oct 25 2010 Jani Välimaa <wally@mandriva.org> 1.6.6-1mdv2011.0
+ Revision: 589266
- new version 1.6.6
- build python extensions
- minor spec cleaning
- disable static build

* Tue Oct 19 2010 Michael Scherer <misc@mandriva.org> 1.6.4-3mdv2011.0
+ Revision: 586687
- add a ldns-utils subpackage with various utilities

* Tue Apr 20 2010 Funda Wang <fwang@mandriva.org> 1.6.4-2mdv2010.1
+ Revision: 536962
- rebuild

* Tue Mar 02 2010 Sandro Cazzaniga <kharec@mandriva.org> 1.6.4-1mdv2010.1
+ Revision: 513634
- update to 1.6.4

* Fri Jul 31 2009 Frederik Himpe <fhimpe@mandriva.org> 1.6.0-1mdv2010.0
+ Revision: 405233
- Update to new version 1.6.0

* Thu Mar 26 2009 Oden Eriksson <oeriksson@mandriva.com> 1.5.1-1mdv2009.1
+ Revision: 361325
- 1.5.1 (fixes CVE-2009-1086)

* Mon Dec 08 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.0-0.20081103.1mdv2009.1
+ Revision: 311881
- 1.4.0 (from unbound-1.1.1.tar.gz)

* Mon Dec 08 2008 Oden Eriksson <oeriksson@mandriva.com> 1.3.0-4mdv2009.1
+ Revision: 311861
- 1.3.0 (final)

* Fri Aug 08 2008 Thierry Vignaud <tv@mandriva.org> 1.3.0-3.20080229.2mdv2009.0
+ Revision: 267800
- rebuild early 2009.0 package (before pixel changes)

* Fri May 30 2008 Oden Eriksson <oeriksson@mandriva.com> 1.3.0-0.20080229.2mdv2009.0
+ Revision: 213295
- fix deps

* Thu May 29 2008 Oden Eriksson <oeriksson@mandriva.com> 1.3.0-0.20080229.1mdv2009.0
+ Revision: 213178
- import ldns

