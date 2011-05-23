%define epiphany_ver %(rpm -q --whatprovides epiphany-devel --queryformat "%{VERSION}")
%define epiphany_minor %(echo %epiphany_ver | awk -F. '{print $2}')
%define epiphany_major 2.%epiphany_minor
%define epiphany_next_major %(echo 2.$((%epiphany_minor+1)))

Summary:	Download Manager for the GNOME
Name:     	gget
Version:	0.0.4
Release:	%mkrel 10
License:	GPLv2+
Group:		Networking/File transfer
Source0: 	http://ftp.gnome.org/pub/GNOME/sources/%name/0.0/%name-%version.tar.bz2
Patch0:		gget-0.0.4-epiphany-2.28.patch
Patch1:		gget-0.0.4-pythonver.patch
URL:		http://live.gnome.org/GGet
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
%py_requires -d
BuildRequires:	gnome-python-extras
BuildRequires:	gnome-python-devel
BuildRequires:	python-dbus
BuildRequires:	python-notify
BuildRequires:	pygtk2.0-devel
BuildRequires:	epiphany-devel
BuildRequires:	intltool
BuildRequires:	gnome-common

Requires:	gnome-python-extras
Requires:	gnome-python-gconf
Requires:	gnome-python-gnomevfs
Requires:	gnome-python-applet
Requires:	python-dbus
Requires:	python-notify

%description
GGet is the name of an upcoming Download Manager for the GNOME desktop.

%package -n epiphany-%name
Summary:	Epiphany extension, using gget as downloader
Group: 		Networking/File transfer
Requires:	%name = %{version}
Requires:	epiphany >= %epiphany_major
Requires:	epiphany < %epiphany_next_major

%description -n epiphany-%name
GGet is the name of an upcoming Download Manager for the GNOME desktop.

This package contains epiphany extesion of gget.

%prep
%setup -q
%patch0 -p1 -b .epi
%patch1 -p1
gnome-autogen.sh

%build
%configure2_5x --disable-schemas-install
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

%{find_lang} %{name}

%if %mdkversion < 200900
%post
%post_install_gconf_schemas %name
%{update_menus}
%{update_desktop_database}
%update_icon_cache hicolor
%endif

%preun
%preun_uninstall_gconf_schemas %name

%if %mdkversion < 200900
%postun
%{clean_menus}
%{clean_desktop_database}
%clean_icon_cache hicolor
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-, root, root)
%doc AUTHORS NEWS TODO
%{_sysconfdir}/gconf/schemas/gget.schemas
%{_bindir}/%name
%{_datadir}/%name
%{_datadir}/applications/*.desktop
%{_datadir}/dbus-1/services/org.gnome.gget.service
%{_iconsdir}/hicolor/*/*/*
%{python_sitelib}/%name

%if 0
%files -n epiphany-%name
%defattr(-, root, root)
%{_libdir}/epiphany/*/extensions/gget*
%endif
