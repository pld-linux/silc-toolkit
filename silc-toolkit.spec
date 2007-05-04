%define	snap	beta1
Summary:	SILC toolkit
Name:		silc-toolkit
Version:	1.1
Release:	0.%{snap}.1
License:	LGPL
Group:		Networking
URL:		http://silcnet.org/
Source0:	http://silcnet.org/download/toolkit/sources/%{name}-%{version}-%{snap}.tar.bz2
# Source0-md5:	aebfb27becdb48f70b2c69ed05629163
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

This package provides development related files for any application
that has SILC support.

%package	devel
Summary:	SILC toolkit
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}

%description	devel
SILC (Secure Internet Live Conferencing) is a protocol which provides
secure conferencing services on the Internet over insecure channel.
SILC is IRC-like software although internally they are very different.
The biggest similarity between SILC and IRC is that they both provide
conferencing services and that SILC has almost the same commands as
IRC. Other than that they are nothing alike. Major differences are
that SILC is secure what IRC is not in any way. The network model is
also entirely different compared to IRC.

This package contains all development related files for developing or
compiling applications using SILC protocol.

%package	static
Summary:	SILC toolkit
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description	static
SILC (Secure Internet Live Conferencing) is a protocol which provides
secure conferencing services on the Internet over insecure channel.
SILC is IRC-like software although internally they are very different.
The biggest similarity between SILC and IRC is that they both provide
conferencing services and that SILC has almost the same commands as
IRC. Other than that they are nothing alike. Major differences are
that SILC is secure what IRC is not in any way. The network model is
also entirely different compared to IRC.

This package contains static SILC libraries.

%prep
%setup -q -n %{name}-%{version}-%{snap}

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

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES README TODO doc/*.txt doc/*.conf doc/toolkit
%dir %{_libdir}/silc
%dir %{_libdir}/silc/modules
%attr(755,root,root) %{_libdir}/silc/modules/*.so
%attr(755,root,root) %{_libdir}/lib*.so.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/silc
%{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
