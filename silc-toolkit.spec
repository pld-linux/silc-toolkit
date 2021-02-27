Summary:	SILC toolkit
Summary(pl.UTF-8):	Zestaw narzędzi do SILC
Name:		silc-toolkit
Version:	1.1.12
Release:	1
License:	GPL v2 or BSD
Group:		Libraries
#Source0Download: http://silcnet.org/dev.html
Source0:	http://downloads.sourceforge.net/silc/%{name}-%{version}.tar.bz2
# Source0-md5:	560dbf1125b031c39a148a26bbe1440d
Patch0:		%{name}-soname.patch
URL:		http://silcnet.org/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1.0
BuildRequires:	libtool
BuildRequires:	rpm-build >= 4.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SILC (Secure Internet Live Conferencing) is a protocol which provides
secure conferencing services on the Internet over insecure channel.
SILC is IRC-like software although internally they are very different.
The biggest similarity between SILC and IRC is that they both provide
conferencing services and that SILC has almost the same commands as
IRC. Other than that they are nothing alike. Major differences are
that SILC is secure what IRC is not in any way. The network model is
also entirely different compared to IRC.

This package provides files for any application that has SILC support.

%description -l pl.UTF-8
SILC (Secure Internet Live Conferencing) to protokół udostępniający
usługi bezpiecznej konferencji poprzez Internet z niezabezpieczonym
kanałem. SILC to oprogramowanie podobne do IRC, ale wewnętrznie bardzo
się różniące. Największe podobieństwo między SILC a IRC jest takie, że
oba udostępniają usługi konferencyjne oraz że SILC ma prawie takie
same polecenia. Wszystko inne nie ma nic wspólnego. Największe różnice
to to, że SILC jest bezpieczny, a IRC w żaden sposób. Model sieciowy
też jest całkowicie inny.

Ten pakiet udostępnia pliki dla wszystkich aplikacji z obsługą SILC.

%package devel
Summary:	SILC toolkit - development files
Summary(pl.UTF-8):	Zestaw narzędzi SILC - pliki programistyczne
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains all development related files for developing or
compiling applications using SILC protocol.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki programistyczne do rozwijania lub
kompilowania aplikacji przy użyciu protokołu SILC.

%package static
Summary:	SILC toolkit - static libraries
Summary(pl.UTF-8):	Zestaw narzędzi SILC - biblioteki statyczne
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package contains static SILC libraries.

%description static -l pl.UTF-8
Ten pakiet zawiera biblioteki statyczne SILC.

%package doc
Summary:	SILC toolkit documentation
Summary(pl.UTF-8):	Dokumentacja do biblioteki narzędziowej SILC
Group:		Documentation
BuildArch:	noarch

%description doc
Extensive SILC toolkit documentation, including standard drafts, API
documentation and tutorial.

%description doc -l pl.UTF-8
Obszerna dokumentacja biblioteki narzędziowej SILC, wraz ze szkicami
standardów, dokumentacją API oraz przewodnikiem.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--includedir=%{_includedir}/silc \
	--enable-ipv6 \
	--enable-shared \
	--with-logsdir=%{_var}/log/silc \
	--with-perl=module \
	--with-perl-lib=vendor \
	--with-simdir=%{_libdir}/silc/modules \
	--with-silcd-pid-file=%{_var}/run/silcd.pid \
	--without-irssi \
	--without-silcd

# parallel will succeed but produce broken library
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_docdir}

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libsilc*.la

# packaged as %doc in base; the rest in -docs
%{__rm} $RPM_BUILD_ROOT%{_docdir}/silc-toolkit/{BSD,COPYING,CREDITS,ChangeLog,CodingStyle,FAQ,GPL,INSTALL,README*,TODO}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc BSD COPYING CREDITS ChangeLog README TODO doc/*.conf
%attr(755,root,root) %{_libdir}/libsilc-1.1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsilc-1.1.so.4
%attr(755,root,root) %{_libdir}/libsilcclient-1.1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsilcclient-1.1.so.4
%dir %{_libdir}/silc
%dir %{_libdir}/silc/modules
%attr(755,root,root) %{_libdir}/silc/modules/*.sim.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsilc.so
%attr(755,root,root) %{_libdir}/libsilcclient.so
%{_includedir}/silc
%{_pkgconfigdir}/silc.pc
%{_pkgconfigdir}/silcclient.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libsilc.a
%{_libdir}/libsilcclient.a

%files doc
%defattr(644,root,root,755)
%{_docdir}/silc-toolkit
