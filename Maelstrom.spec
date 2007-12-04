%define version  3.0.6
%define release  %mkrel 11
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
Patch:     maelstrom-snd2wav.patch.bz2
Patch1:    Maelstrom-3.0.6-scorefile.patch.bz2
Patch2:	   Maelstrom-3.0.6-datadir.patch.bz2	
Patch3:	   Maelstrom-3.0.6-gcc3.4.patch.bz2
Patch4:    Maelstrom-3.0.6-64bit-fixes.patch.bz2
URL:       http://www.devolution.com/~slouken/Maelstrom/
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires:	SDL_net-devel
BuildRequires:	X11-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	esound-devel
BuildRequires:	texinfo
BuildRequires:	automake1.4

%description
Maelstrom is a rockin' asteroids game ported from the Macintosh
Originally written by Andrew Welch of Ambrosia Software, and ported
to UNIX and then SDL by Sam Lantinga <slouken@devolution.com>

%prep
%setup -q
%patch0 -p1
%patch1 -b .scores
%patch2 -p1 -b .libdir
%patch3 -p1
%patch4 -p1 -b .64bit-fixes

%build
aclocal-1.4
automake-1.4 -a
autoconf
%configure2_5x --disable-rpath --bindir=%_gamesbindir --libdir=%_gamesdatadir

%make

%install
rm -rf %buildroot
%makeinstall_std GAME_INSTALLDIR=%buildroot/%_gamesdatadir/%name
# %_bindir=%buildroot/%_gamesbindir

(cd $RPM_BUILD_ROOT
mkdir -p ./%_menudir
cat > ./%_menudir/%{name} << EOF
?package(%{name}):\
command="%_gamesbindir/Maelstrom"\
title="Maelstrom"\
longtitle="Asteroids game"\
section="Amusement/Arcade" \
needs="x11"\
icon="Maelstrom.png"
EOF
) 

mkdir -p $RPM_BUILD_ROOT%{_miconsdir}
mkdir -p $RPM_BUILD_ROOT%{_liconsdir}
install -m 644 %{SOURCE10} $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -m 644 %{SOURCE11} $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m 644 %{SOURCE12} $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

mkdir -p %buildroot/var/lib/games/
mv %buildroot%_gamesdatadir/Maelstrom/Maelstrom-Scores %buildroot/var/lib/games/Maelstrom-Scores

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus

%postun
%clean_menus

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
%_menudir/*
%_iconsdir/*.png
%_miconsdir/*
%_liconsdir/*
%attr(0664,root,games) /var/lib/games/Maelstrom-Scores

