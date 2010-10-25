%define major 1
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}

%define build_python 1

Summary:	Lowlevel DNS(SEC) library with API
Name:		ldns
Version:	1.6.6
Release:	%mkrel 1
License:	BSD
Group:		System/Libraries
URL:		http://www.nlnetlabs.nl/ldns/
Source0:	http://www.nlnetlabs.nl/downloads/ldns/ldns-%{version}.tar.gz
BuildRequires:	libtool
BuildRequires:	openssl-devel
BuildRequires:	doxygen
BuildRequires:	swig
BuildRequires:	python-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
rm -rf %{buildroot}
%makeinstall_std
( cd examples ; %makeinstall_std )
( cd drill ; %makeinstall_std )

# don't package building script in doc
rm doc/doxyparse.pl

#remove doc stubs
rm -rf doc/.svn

#remove double set of man pages
rm -rf doc/man

#we don't want these
find %{buildroot} -name "*.la" -exec rm -rf {} \;

%if %{build_python}
#remove executable bit
chmod a-x %{buildroot}%{python_sitelib}/*py
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc README LICENSE 
%{_libdir}/lib*so.%{major}*

%files -n %{develname}
%defattr(-,root,root,-)
%doc doc Changelog README
%dir %{_includedir}/ldns
%{_includedir}/ldns/*
%{_libdir}/lib*.so
%{_mandir}/man3/*
%{_bindir}/%{name}-config

%files -n %{name}-utils
%defattr(-,root,root)
%{_bindir}/*
%exclude %{_bindir}/%{name}-config
%{_mandir}/man1/*

%if %{build_python}
%files -n python-%{name}
%defattr(-,root,root)
%{python_sitelib}/*
%endif
