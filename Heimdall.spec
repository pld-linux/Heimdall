Summary:	Flash firmware on to Samsung Galaxy S devices
Name:		Heimdall
Version:	1.4.2
Release:	1
License:	MIT
Group:		Development/Tools
Source0:	https://github.com/Benjamin-Dobell/Heimdall/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	49a6537f647b50057a3096180c4f0ac3
Source1:	%{name}.desktop
URL:		http://glassechidna.com.au/heimdall/
BuildRequires:	Qt5Widgets-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libusb-devel >= 1.0.8
BuildRequires:	pkgconfig
BuildRequires:	qt5-build
BuildRequires:	cmake
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

# remove unneeded files
rm -rf Win32
rm -rf OSX

%build
install -d build
cd build
%cmake \
        ../
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_desktopdir},/lib/udev/rules.d}

install build/bin/heimdall{,-frontend} $RPM_BUILD_ROOT%{_bindir}/
install heimdall/60-heimdall.rules $RPM_BUILD_ROOT/lib/udev/rules.d/

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}/heimdall.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Linux/README
%attr(755,root,root) %{_bindir}/heimdall
/lib/udev/rules.d/60-heimdall.rules

%files frontend
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/heimdall-frontend
%{_desktopdir}/heimdall.desktop
