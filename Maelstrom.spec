%define version  3.0.6
%define release  %mkrel 13
%define name Maelstrom

Summary:   Maelstrom
Name:      %{name}
Version:   %{version}
Release:   %{release}
License: LGPL
Group:     Games/Arcade
Source0:   %{name}-%{version}.tar.bz2
Source10: %name.16.png
Source11: %name.32.png
Source12: %name.48.png
Patch1:    Maelstrom-3.0.6-scorefile.patch
Patch2:	   Maelstrom-3.0.6-datadir.patch
Patch3:	   Maelstrom-3.0.6-gcc3.4.patch
Patch4:    Maelstrom-3.0.6-64bit-fixes.patch
URL:       http://www.devolution.com/~slouken/Maelstrom/
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires:	SDL_net-devel
BuildRequires:	SDL-devel

%description
Maelstrom is a rockin' asteroids game ported from the Macintosh
Originally written by Andrew Welch of Ambrosia Software, and ported
to UNIX and then SDL by Sam Lantinga <slouken@devolution.com>

%prep
%setup -q
%patch1 -b .scores
%patch2 -p1 -b .libdir
%patch3 -p1
%patch4 -p1 -b .64bit-fixes

touch ChangeLog NEWS AUTHORS

%build
autoreconf -fi
%configure2_5x --disable-rpath --bindir=%_gamesbindir --libdir=%_gamesdatadir

%make

%install
rm -rf %buildroot
%makeinstall_std GAME_INSTALLDIR=%buildroot/%_gamesdatadir/%name
install -D -m755 Maelstrom %buildroot/%_gamesbindir/Maelstrom
install -D -m755 Maelstrom-netd %buildroot/%_gamesbindir/Maelstrom-netd

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=%_gamesbindir/Maelstrom
Name=Maelstrom
Comment=Asteroids game
Categories=Game;ArcadeGame;
Icon=Maelstrom
EOF

mkdir -p $RPM_BUILD_ROOT%{_miconsdir}
mkdir -p $RPM_BUILD_ROOT%{_liconsdir}
install -m 644 %{SOURCE10} $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -m 644 %{SOURCE11} $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m 644 %{SOURCE12} $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

mkdir -p %buildroot/var/lib/games/
mv %buildroot%_gamesdatadir/Maelstrom/Maelstrom-Scores %buildroot/var/lib/games/Maelstrom-Scores

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%pre
# in Maelstrom <= 3.0.6-4mdk %_gamesbindir/Maelstrom is a directory
if [ -d %_gamesbindir/Maelstrom ]; then
  rm -rf %_gamesbindir/Maelstrom
fi

%files
%defattr(-, root, root)
%doc COPYING CREDITS README* Changelog Docs
%attr(2755,root,games) %_gamesbindir/Maelstrom*
%_gamesdatadir/Maelstrom
%{_datadir}/applications/mandriva-*.desktop
%_iconsdir/*.png
%_miconsdir/*
%_liconsdir/*
%attr(0664,root,games) /var/lib/games/Maelstrom-Scores

