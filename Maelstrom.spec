%define version  3.0.6
%define release  14
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



%changelog
* Mon Jan 03 2011 Funda Wang <fwang@mandriva.org> 3.0.6-13mdv2011.0
+ Revision: 627689
- fix build

* Mon Jul 28 2008 Thierry Vignaud <tv@mandriva.org> 3.0.6-13mdv2009.0
+ Revision: 251663
- rebuild

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Tue Dec 18 2007 Thierry Vignaud <tv@mandriva.org> 3.0.6-11mdv2008.1
+ Revision: 132317
- auto-convert XDG menu entry
- kill re-definition of %%buildroot on Pixel's request
- use %%mkrel
- buildrequires X11-devel instead of XFree86-devel
- import Maelstrom


* Mon May 15 2006 Stefan van der Eijk <stefan@eijk.nu> 3.0.6-11mdk
- rebuild for sparc

* Mon Sep  5 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 3.0.6-10mdk
- 64-bit fixes

* Sat Aug 28 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 3.0.6-9mdk
- add BuildRequires: automake1.4

* Wed Aug 18 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 3.0.6-8mdk
- Rebuild with new menu

* Mon Jun  7 2004 Götz Waschk <waschk@linux-mandrake.com> 3.0.6-7mdk
- fix menu
- remove some BRs
- patch for new g++

* Tue Jul 22 2003 Götz Waschk <waschk@linux-mandrake.com> 3.0.6-6mdk
- fix update from old releases

* Mon Jul 21 2003 Götz Waschk <waschk@linux-mandrake.com> 3.0.6-5mdk
- move files to the right dirs

* Wed Apr  2 2003 Götz Waschk <waschk@linux-mandrake.com> 3.0.6-4mdk
- spec fixes
- make binary sgid games and fix location of the highscores (bug #2840)

* Thu Jan 16 2003 Lenny Cartier <lenny@mandrakesoft.com> 3.0.6-3mdk
- rebuild

* Thu Oct 24 2002 Stew Benedict <sbenedict@mandrakesoft.com> 3.0.6-2mdk
- allow build on other arches (no i586 in spec)

* Wed Oct 23 2002 Lenny Cartier <lenny@mandrakesoft.com> 3.0.6-1mdk
- 3.0.6

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.0.5-8mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Thu Jul 25 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.0.5-7mdk
- Automated rebuild with gcc3.2

* Tue May 07 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.0.5-6mdk
- Automated rebuild in gcc3.1 environment

* Mon Apr 29 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 3.0.5-5mdk
- rebuild for new alsa

* Wed Apr 24 2002 Lenny Cartier <lenny@mandrakesoft.com> 3.0.5-4mdk
- remove latest conflicts
- remove playwave

* Wed Apr 24 2002  Lenny Cartier <lenny@mandrakesoft.com> 3.0.5-3mdk
- conflicts : SDL_mixer-player 

* Fri Jan 18 2002 Stefan van der Eijk <stefan@eijk.nu> 3.0.5-2mdk
- BuildRequires

* Mon Jan 14 2002 Lenny Cartier <lenny@mandrakesoft.com> 3.0.5-1mdk
- 3.0.5
- convert xpms to pngs

* Sun Jul  8 2001 Stefan van der Eijk <stefan@eijk.nu> 3.0.1-10mdk
- BuildRequires:	libSDL-devel

* Wed Jun 13 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 3.0.1-9mdk
- recompile with new SDL

* Sat Mar 17 2001 Lenny Cartier <lenny@mandrakesoft.com> 3.0.1-8mdk
- fix icons

* Fri Nov 10 2000 Lenny Cartier <lenny@mandrakesoft.com> 3.0.1-7mdk
- patch to fix build with gcc-2.96

* Wed Sep 27 2000 Vincent Saugey <vince@mandrakesoft.com> 3.0.1-6mdk
- really fix menu entry

* Wed Sep 27 2000 Lenny Cartier <lenny@mandrakesoft.com> 3.0.1-5mdk
- fix menu entry

* Fri Jul 28 2000 Lenny Cartier <lenny@mandrakesoft.com> 3.0.1-4mdk
- macro
- bm
- menu

* Wed Apr 19 2000 Lenny Cartier <lenny@mandrakesoft.com> 3.0.1-3mdk
- fix group
- fix source permission

* Thu Dec 09 1999 Lenny Cartier <lenny@mandrakesoft.com>
- new in contribs
- mandrake adaptations

* Tue Sep 21 1999 Sam Lantinga <slouken@devolution.com>

- first attempt at a spec file

