Summary:	Flash firmware on to Samsung Galaxy S devices
Name:		Heimdall
Version:	1.4.1
Release:	1
License:	MIT
Group:		Development/Tools
Source0:	https://github.com/Benjamin-Dobell/Heimdall/archive/v1.4.1/%{name}-%{version}.tar.gz
# Source0-md5:	22c911e9042f5ed8fd90cbeeb9589015
Source1:	%{name}.desktop
Patch0:		%{name}-udev-rules.patch
URL:		http://glassechidna.com.au/heimdall/
BuildRequires:	QtGui-devel
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.10
BuildRequires:	libstdc++-devel
BuildRequires:	libusb-devel >= 1.0.8
BuildRequires:	pkgconfig
BuildRequires:	qt4-build
BuildRequires:	qt4-qmake
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Heimdall is a cross-platform open-source tool suite used to flash
firmware (aka ROMs) onto Samsung mobile devices.

%package frontend
Summary:	Qt4 based frontend for Heimdall
Group:		X11/Development/Tools
Requires:	%{name} = %{version}-%{release}

%description frontend
Heimdall is a cross-platform open-source tool suite used to flash
firmware (aka ROMs) onto Samsung mobile devices.

This package provides Qt4 based frontend for Heimdall.

%prep
%setup -q
%patch0 -p1

sed -i -e 's|/usr/local/bin|%{_bindir}|g' heimdall-frontend/heimdall-frontend.pro

# remove unneeded files
rm -rf libusbx-1.0
rm -rf Win32
rm -rf heimdall-frontend/lib/win32
rm -rf heimdall-frontend/include
rm -rf heimdall/autom4te.cache
rm -rf libpit/autom4te.cache
rm -rf OSX
rm -f heimdall/postremove-pak
rm -f heimdall/postinstall-pak

%build
cd libpit
%configure
%{__make}
cd ..

cd heimdall
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}
cd ..

cd heimdall-frontend
qmake-qt4
%{__make}
cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_desktopdir}

%{__make} -C heimdall install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C heimdall-frontend install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}/heimdall.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/heimdall
/lib/udev/rules.d/60-heimdall.rules

%files frontend
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/heimdall-frontend
%{_desktopdir}/heimdall.desktop
