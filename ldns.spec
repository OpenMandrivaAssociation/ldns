%define major 1
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}

Summary:	Lowlevel DNS(SEC) library with API
Name:		ldns
Version:	1.6.4
Release:	%mkrel 1
License:	BSD
Group:		System/Libraries
URL:		http://www.nlnetlabs.nl/ldns/
Source0:	http://www.nlnetlabs.nl/downloads/ldns/ldns-%{version}.tar.gz
BuildRequires:	libtool
BuildRequires:	openssl-devel
BuildRequires:	doxygen
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
ldns is a library with the aim to simplify DNS programing in C. All
lowlevel DNS/DNSSEC operations are supported. We also define a higher
level API which allows a programmer to (for instance) create or sign
packets.

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
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{develname}
The devel package contains the ldns library and the include files

%prep
%setup -q

%build
%configure2_5x \
    --disable-rpath

%make

%install
rm -rf %{buildroot}
%makeinstall_std

# don't package building script in doc
rm doc/doxyparse.pl

#remove doc stubs
rm -rf doc/.svn

#remove double set of man pages
rm -rf doc/man

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
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
%{_libdir}/lib*.*a
%{_mandir}/man3/*
%{_bindir}/%{name}-config
