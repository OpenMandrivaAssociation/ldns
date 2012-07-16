%define major 1
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}

%define build_python 1

Summary:	Lowlevel DNS(SEC) library with API
Name:		ldns
Version:	1.6.13
Release:	1
License:	BSD
Group:		System/Libraries
URL:		http://www.nlnetlabs.nl/ldns/
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
