Summary:	SILC toolkit
Summary(pl.UTF-8):	Zestaw narzędzi do SILC
Name:		silc-toolkit
Version:	1.1.1
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://silcnet.org/download/toolkit/sources/%{name}-%{version}.tar.bz2
# Source0-md5:	cc10836e5ffc665eddd1bac6bc3b1382
URL:		http://silcnet.org/
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%prep
%setup -q

%build
%configure \
	--with-logsdir=%{_var}/log/silc \
	--with-simdir=%{_libdir}/silc/modules \
	--with-silcd-pid-file=%{_var}/run/silcd.pid \
	--enable-ipv6 \
	--enable-shared \
	--with-perl=module \
	--with-perl-lib=vendor \
	--without-silcd \
	--without-irssi \
	--includedir=%{_includedir}/silc

# parallel will succeed but produce broken library
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_docdir}

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_prefix}/doc

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES README TODO doc/*.txt doc/*.conf doc/toolkit
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%dir %{_libdir}/silc
%dir %{_libdir}/silc/modules
%attr(755,root,root) %{_libdir}/silc/modules/*.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/silc
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
