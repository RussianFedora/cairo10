%define pixman_version 0.18.4
%define freetype_version 2.1.9
%define fontconfig_version 2.0

%global shortname cairo

Summary:	A 2D graphics library
Name:		%{shortname}10
Version:	1.10.2
Release:	1.el6.R
URL:		http://cairographics.org
#VCS:		git:git://git.freedesktop.org/git/cairo
Source0:	http://cairographics.org/snapshots/%{shortname}-%{version}.tar.gz
#Source0:	http://cairographics.org/releases/%{name}-%{version}.tar.gz
Patch0:		cairo-1.10.0-buggy_gradients.patch
License:	LGPLv2 or MPLv1.1
Group:		System Environment/Libraries
Provides:	%{shortname} = %{version}-%{release}

# Use poppler14 package
Patch1:		cairo10-poppler14.patch
# Use pixman184 package
Patch2:		cairo10-pixman184.patch

BuildRequires: pkgconfig
BuildRequires: libXrender-devel
BuildRequires: libX11-devel
BuildRequires: libpng-devel
BuildRequires: libxml2-devel
BuildRequires: pixman-devel >= %{pixman_version}
BuildRequires: freetype-devel >= %{freetype_version}
BuildRequires: fontconfig-devel >= %{fontconfig_version}
BuildRequires: glib2-devel
BuildRequires: poppler-glib-devel >= 0.14.0
BuildRequires: librsvg2-devel

%description
Cairo is a 2D graphics library designed to provide high-quality display
and print output. Currently supported output targets include the X Window
System, OpenGL (via glitz), in-memory image buffers, and image files (PDF,
PostScript, and SVG).

Cairo is designed to produce consistent output on all output media while
taking advantage of display hardware acceleration when available (e.g.
through the X Render Extension or OpenGL).

%package devel
Summary: Development files for cairo10
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libXrender-devel
Requires: libpng-devel
Requires: pixman-devel >= %{pixman_version}
Requires: freetype-devel >= %{freetype_version}
Requires: fontconfig-devel >= %{fontconfig_version}
Requires: poppler-glib-devel >= 0.14.0
Requires: librsvg2-devel
Requires: pkgconfig
Provides: %{shortname}-devel = %{version}-%{release}

%description devel
Cairo is a 2D graphics library designed to provide high-quality display
and print output.

This package contains libraries, header files and developer documentation
needed for developing software which uses the cairo graphics library.

%package gobject
Summary: GObject bindings for cairo10
Group: System Environment/Libraries
Provides: %{shortname}-gobject = %{version}-%{release}

%description gobject
Cairo is a 2D graphics library designed to provide high-quality display
and print output.

This package contains functionality to make cairo graphics library
integrate well with the GObject object system used by GNOME.

%package gobject-devel
Summary: Development files for cairo-gobject
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}
Requires: pkgconfig
Provides: %{shortname}-gobject-devel = %{version}-%{release}

%description gobject-devel
Cairo is a 2D graphics library designed to provide high-quality display
and print output.

This package contains libraries, header files and developer documentation
needed for developing software which uses the cairo Gobject library.

%package tools
Summary: Development tools for cairo
Group: Development/Tools
Provides: %{shortname}-tools = %{version}-%{release}

%description tools
Cairo is a 2D graphics library designed to provide high-quality display
and print output.

This package contains tools for working with the cairo graphics library.
 * cairo-trace: Record cairo library calls for later playback

%prep
%setup -q -n %{shortname}-%{version}

%patch0 -p0 -b .nvidia-sux
%patch1 -p1 -b .poppler14
#patch2 -p1 -b .pixman184

sed -i "s|libcairo|libcairo10|g" src/Makefile.in
sed -i "s|libcairo|libcairo10|g" util/Makefile.in
sed -i "s|libcairo|libcairo10|g" util/cairo-gobject/Makefile.in
sed -i "s|libcairo|libcairo10|g" util/cairo-script/Makefile.in

%build
%configure --disable-static 	\
	--enable-warnings 	\
	--enable-xlib 		\
	--enable-freetype 	\
	--enable-ps 		\
	--enable-pdf 		\
	--enable-svg 		\
	--enable-tee		\
        --enable-gobject        \
	--disable-gtk-doc
make V=1 %{?_smp_mflags}

%install

make install V=1 DESTDIR=%{buildroot}
rm %{buildroot}%{_libdir}/*.la

mv %{buildroot}%{_includedir}/%{shortname} %{buildroot}%{_includedir}/%{name}

pushd %{buildroot}%{_libdir}/pkgconfig
for i in *.pc; do
	NEWNAME=`echo $i | sed 's|cairo|cairo10|g'`
	sed -i 's|cairo|cairo10|g' $i
	mv $i $NEWNAME
done

mv %{buildroot}%{_datadir}/gtk-doc/html/%{shortname} %{buildroot}%{_datadir}/gtk-doc/html/%{name}
mv %{buildroot}%{_bindir}/%{shortname}-trace %{buildroot}%{_bindir}/%{name}-trace
mv %{buildroot}%{_libdir}/%{shortname} %{buildroot}%{_libdir}/%{name}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS BIBLIOGRAPHY BUGS COPYING COPYING-LGPL-2.1 COPYING-MPL-1.1 NEWS README
%{_libdir}/lib%{name}.so.*
%{_libdir}/lib%{name}-script-interpreter.so.*

%files devel
%defattr(-,root,root,-)
%doc ChangeLog PORTING_GUIDE
%{_includedir}/%{name}/cairo-deprecated.h
%{_includedir}/%{name}/cairo-features.h
%{_includedir}/%{name}/cairo-ft.h
%{_includedir}/%{name}/cairo.h
%{_includedir}/%{name}/cairo-pdf.h
%{_includedir}/%{name}/cairo-ps.h
%{_includedir}/%{name}/cairo-script-interpreter.h
%{_includedir}/%{name}/cairo-svg.h
%{_includedir}/%{name}/cairo-tee.h
%{_includedir}/%{name}/cairo-version.h
%{_includedir}/%{name}/cairo-xlib-xrender.h
%{_includedir}/%{name}/cairo-xlib.h
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}-script-interpreter.so
%{_libdir}/pkgconfig/%{name}-fc.pc
%{_libdir}/pkgconfig/%{name}-ft.pc
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/%{name}-pdf.pc
%{_libdir}/pkgconfig/%{name}-png.pc
%{_libdir}/pkgconfig/%{name}-ps.pc
%{_libdir}/pkgconfig/%{name}-svg.pc
%{_libdir}/pkgconfig/%{name}-tee.pc
%{_libdir}/pkgconfig/%{name}-xlib.pc
%{_libdir}/pkgconfig/%{name}-xlib-xrender.pc
%{_datadir}/gtk-doc/html/%{name}

%files gobject
%defattr(-,root,root,-)
%{_libdir}/lib%{name}-gobject.so.*

%files gobject-devel
%defattr(-,root,root,-)
%{_includedir}/%{name}/cairo-gobject.h
%{_libdir}/lib%{name}-gobject.so
%{_libdir}/pkgconfig/%{name}-gobject.pc

%files tools
%defattr(-,root,root,-)
%{_bindir}/%{name}-trace
%{_libdir}/%{name}

%changelog
* Fri Oct 28 2011 Arkady L. Shane <ashejn@russianfedora> - 1.10.2-1.el6.R
- build compat package for cairo 1.8.8

* Tue Feb  1 2011 Tom Callaway <spot@fedoraproject.org> - 1.10.2-2
- enable tee support

* Mon Jan 17 2011 Tom Callaway <spot@fedoraproject.org> - 1.10.2-1
- Update to 1.10.2
- Re-enable the buggy_gradients workaround, as using hardware gradients
  causes rendering issues and slowness when using the nvidia binary
  driver (#649955)

* Thu Nov 11 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.10.0-4
- package for firefox4

* Wed Sep 29 2010 jkeating - 1.10.0-3
- Rebuilt for gcc bug 634757

* Thu Sep 16 2010 Matthias Clasen <mclasen@redhat.com> - 1.10.0-2
- Drop the explicit dep on the wrong package from -gobject-devel

* Tue Sep 07 2010 Benjamin Otte <otte@redhat.com> - 1.10.0-1
- Update to 1.10.0
- Add cairo-gobject package

* Mon Jul 26 2010 Benjamin Otte <otte@redhat.com> - 1.9.14-1
- Update to 1.9.14 snapshot

* Sun Jul 04 2010 Benjamin Otte <otte@redhat.com> - 1.9.12-1
- Update to 1.9.12 snapshot
- Remove now unnecessary patch

* Sun Jul 04 2010 Benjamin Otte <otte@redhat.com> - 1.9.10-3
- Add patch to force linking with gcc, not g++. (#606523)

* Sun Jul 04 2010 Benjamin Otte <otte@redhat.com> - 1.9.10-2
- Don't use silent rules, we want verbose output in builders

* Thu Jun 27 2010 Benjamin Otte <otte@redhat.com> - 1.9.10-1
- Update to 1.9.10 snapshot

* Thu Jun 17 2010 Benjamin Otte <otte@redhat.com> - 1.9.8-1
- Update to 1.9.8 snapshot

* Sun Feb 21 2010 Matthias Clasen <mclasen@redhat.com> - 1.8.10-1
- Update to 1.8.10

* Sun Aug  2 2009 Matthias Clasen <mclasen@redhat.com> - 1.8.8-3
- Move ChangeLog to -devel to save space

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Matthias Clasen <mclasen@redhat.com> 1.8.8-1
- Update to 1.8.8

* Wed Apr 08 2009 Adam Jackson <ajax@redhat.com> 1.8.6-3
- cairo-1.8.6-repeat-modes.patch: Enable the repeat and pad blend modes in
  the xlib backend to make firefox performance slightly less dire.

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan  7 2009 Matthias Clasen <mclasen@redhat.com> 1.8.6-1
- Update to 1.8.6

* Sun Dec 14 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> 1.8.0-3
- Rebuild for pkgconfig provides

* Fri Nov 21 2008 Matthias Clasen <mclasen@redhat.com> 1.8.0-2
- Tweak %%summary and %%documentation

* Thu Sep 25 2008 Behdad Esfahbod <besfahbo@redhat.com> 1.8.0-1
- Update to 1.8.0
- Update dep versions

* Mon Sep 22 2008 Behdad Esfahbod <besfahbo@redhat.com> 1.7.6-1
- Update to 1.7.6

* Mon Aug 11 2008 Matthias Clasen <mclasen@redhat.com> 1.7.4-1
- Update to 1.7.4

* Wed May 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.6.4-3
- fix license tag

* Sun May  4 2008 Matthias Clasen <mclasen@redhat.com> 1.6.4-2
- Fix source url

* Fri Apr 11 2008 Carl Worth <cworth@redhat.com> 1.6.2-1
- Update to 1.6.2

* Thu Apr 10 2008 Carl Worth <cworth@redhat.com> 1.6.0-1
- Update to 1.6.0

* Tue Apr  8 2008 Carl Worth <cworth@redhat.com> 1.5.20-1
- Update to 1.5.20

* Sun Apr  6 2008 Carl Worth <cworth@redhat.com> 1.5.18-1
- Update to 1.5.18

* Thu Apr  3 2008 Matthias Clasen <mclasen@redhat.com> 1.5.16-1
- Update to 1.5.16

* Fri Mar 21 2008 Matthias Clasen <mclasen@redhat.com> 1.5.14-1
- Update to 1.5.14

* Wed Feb 20 2008 Behdad Esfahbod <besfahbo@redhat.com>
- Point Source to cairographics.org/snapshots.  Change back to /releases
  when 1.6.0 is out.

* Wed Jan 30 2008 Behdad Esfahbod <besfahbo@redhat.com> 1.5.8-2
- Remove TODO and ROADMAP as they were removed from tarball upstream.

* Wed Jan 30 2008 Behdad Esfahbod <besfahbo@redhat.com> 1.5.8-1
- Update to 1.5.8

* Thu Jan 17 2008 Behdad Esfahbod <besfahbo@redhat.com> 1.5.6-1
- Update to 1.5.6

* Thu Dec  6 2007 Matthias Clasen <mclasen@redhat.com> - 1.5.4-1
- Update to 1.5.4

* Wed Oct 31 2007 Behdad Esfahbod <besfahbo@redhat.com> 1.5.2-1
- Update to 1.5.2
- Switch to external pixman.

* Wed Aug 22 2007 Adam Jackson <ajax@redhat.com> - 1.4.10-2
- Rebuild for PPC toolchain bug

* Wed Jun 27 2007 Carl Worth <cworth@redhat.com> 1.4.10-1
- Update to 1.4.10

* Sat Jun 9 2007 Behdad Esfahbod <besfahbo@redhat.com> 1.4.8-1
- Update to 1.4.8

* Tue May  1 2007 Carl Worth <cworth@redhat.com> 1.4.6-1
- Update to 1.4.6

* Mon Apr 16 2007 Carl Worth <cworth@redhat.com> 1.4.4-1
- Update to 1.4.4

* Tue Mar 20 2007 Carl Worth <cworth@redhat.com> 1.4.2-1
- Update to 1.4.2

* Tue Mar  6 2007 Carl Worth <cworth@redhat.com> 1.4.0-1
- Update to 1.4.0

* Wed Feb 14 2007 Carl Worth <cworth@redhat.com> 1.3.14-1
- Update to 1.3.14

* Sat Jan 20 2007 Carl Worth <cworth@redhat.com> 1.3.12-1
- Update to 1.3.12

* Sat Dec 23 2006 Carl Worth <cworth@redhat.com> 1.3.10-1
- Update to 1.3.10

* Thu Dec 14 2006 Carl Worth <cworth@redhat.com> 1.3.8-1
- Update to 1.3.8

* Sat Dec  9 2006 Matthias Clasen <mclasen@redhat.com> 1.3.6-2
- Small spec file cleanups

* Wed Dec  6 2006 Matthias Clasen <mclasen@redhat.com> 1.3.6-1
- Update to 1.3.6

* Thu Nov 23 2006 Matthias Clasen <mclasen@redhat.com> 1.3.4-1
- Update to 1.3.4

* Wed Nov 15 2006 Carl Worth <cworth@redhat.com> 1.3.2-1
- Update to 1.3.2

* Sun Nov  5 2006 Matthias Clasen <mclasen@redhat.com> 1.2.6-1
- Update to 1.2.6

* Sun Aug 20 2006 Behdad Esfahbod <besfahbo@redhat.com> 1.2.4-1
- Update to 1.2.4
- Drop libXt-devel BuildReq as it shouldn't need it anymore.

* Wed Aug  9 2006 Behdad Esfahbod <besfahbo@redhat.com> 1.2.2-3
- Remove unnecessary --disable-* arguments to configure, add --enable-*
  for those backends we really want to make sure are enabled.

* Wed Aug  9 2006 Ray Strode <rstrode@redhat.com> - 1.2.2-2
- add lame libXt-devel BuildReq to get things building again.
- small spec tweaks to follow conventions

* Wed Aug  9 2006 Behdad Esfahbod <besfahbo@redhat.com> 1.2.2-1
- Update to 1.2.2

* Tue Jul 18 2006 Matthias Clasen <mclasen@redhat.com> - 1.2.0-2
- rebuild

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.2.0-1.1
- rebuild

* Mon Jul  3 2006 Matthias Clasen <mclasen@redhat.com> 1.2.0-1
- Update to 1.2.0

* Fri Jun 16 2006 Carl Worth <cworth@redhat.com> 1.1.10-1
- Update to 1.1.10 (fixes crash on 16-bit X servers like Xvnc)

* Wed Jun 14 2006 Matthias Clasen <mclasen@redhat.com> 1.1.8-1
- Update to 1.1.8

* Tue May 16 2006 Karsten Hopp <karsten@redhat.de> 1.1.6-6
- buildrequire libxml2-devel

* Fri May  5 2006 Carl Worth <cworth@redhat.com> - 1.1.6-2
- Refuse to build pdf2svg to avoid depending on newer poppler

* Fri May  5 2006 Carl Worth <cworth@redhat.com> - 1.1.6-1
- Update to new upstream 1.1.6

* Wed May  3 2006 Carl Worth <cworth@redhat.com> - 1.1.4-2
- Revert upstream commit that introduced a dependency on a newer
  poppler version for the PDF tests.

* Wed May  3 2006 Carl Worth <cworth@redhat.com> - 1.1.4-1
- Update to new upstream 1.1.4
- Drop both embedded-bitmaps and XRenderAddGlyphs patches as both now
  have upstream versions

* Fri Apr 28 2006 Carl Worth <cworth@redhat.com> - 1.1.2-2
- Add suggested patch for XRenderAddGlyphs crash of bug #4705
  https://bugs.freedesktop.org/show_bug.cgi?id=4705

* Tue Apr 25 2006 Carl Worth <cworth@redhat.com> - 1.1.2-1
- Update to new upstream 1.1.2
- Port forward the embedded bitmaps patch (now committed upstream to
  1.1.3)
- Drop build-fix and chunk-glyphs patches which now come from upstream

* Wed Mar 15 2006 Matthias Clasen <mclasen@redhat.com> - 1.0.4-1
- Update to 1.0.4
- Drop upstreamed patches

* Fri Mar  3 2006 Carl Worth <cworth@redhat.com> - 1.0.2-5
- add patch to chunk Xlib glyph compositing (bug 182416 and
  CVE-20060528)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0.2-4.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.2-4.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 31 2006 Ray Strode <rstrode@redhat.com> 1.0.2-4
- add patch from Tim Mayberry to support embbedded bitmap
  fonts (bug 176910)

* Tue Jan  3 2006 Jesse Keating <jkeating@redhat.com> 1.0.2-3.2
- rebuilt again

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Oct 31 2005 Matthias Clasen <mclasen@redhat.com> 1.0.2-3
- Require libXrender-devel instead of xorg-X11-devel

* Tue Oct 11 2005 Kristian Høgsberg <krh@redhat.com> 1.0.2-2
- Rebuild against freetype-2.10 to pick up FT_GlyphSlot_Embolden.

* Thu Oct  6 2005 Kristian Høgsberg <krh@redhat.com> - 1.0.2-1
- Update to cairo-1.0.2.

* Wed Aug 24 2005 Kristian Høgsberg <krh@redhat.com> - 1.0.0-1
- Update to cairo-1.0.0.
- Drop cairo-0.9.2-cache-eviction-fix.patch and
  cairo-0.9.2-dont-hash-null-string.patch.

* Fri Aug 19 2005 Kristian Høgsberg <krh@redhat.com> 0.9.2-3
- Add cairo-0.9.2-dont-hash-null-string.patch to avoid crash when
  creating a cairo font from a FT_Face.

* Tue Aug 16 2005 Kristian Høgsberg <krh@redhat.com> - 0.9.2-2
- Rebuild against new freetype to get rid of --rpath in cairo.pc.

* Mon Aug 15 2005 Kristian Høgsberg <krh@redhat.com> 0.9.2-1
- Also obsolete libpixman-debuginfo.
- Add cairo-0.9.2-cache-eviction-fix.patch to fix ft font cache eviction.

* Sun Aug 14 2005 Kristian Høgsberg <krh@redhat.com> 0.9.2-1
- Update to cairo 0.9.2.  Add Obsoletes: for libpixman <= 0.1.6.
- Drop cairo-0.6.0-font-options-to-scaled-font.patch.

* Tue Aug  2 2005 Kristian Høgsberg <krh@redhat.com> - 0.6.0-2
- Add cairo-0.6.0-font-options-to-scaled-font.patch to make sure font
  cache eviction works correctly (#164664).

* Thu Jul 28 2005 Owen Taylor <otaylor@devserv.devel.redhat.com> 0.6.0-1
- Update to cairo-0.6.0

* Mon Jul 18 2005 Kristian Høgsberg <krh@redhat.com> 0.5.2-1
- Update to cairo-0.5.2 and drop bitmap font patch.

* Wed Jul  6 2005 Kristian Høgsberg <krh@redhat.com> - 0.5.1-5
- Fix typo in use of libpixman_version macro (Thanks to Michael
  Schwendt, #162550).

* Sun Jun 26 2005 Kristian Høgsberg <krh@redhat.com> - 0.5.1-4
- Add more missing devel package requires (libpng-devel and
  xorg-x11-devel) (#161688)
- Add Owens patch (cairo-0.5.1-bitmap-fonts.patch) to make bitmap
  fonts work with cairo (#161653).

* Wed Jun 22 2005 Kristian Høgsberg <krh@redhat.com> - 0.5.1-3
- Add requirement on libpixman-devel for devel package.

* Tue Jun 21 2005 Kristian Høgsberg <krh@redhat.com> - 0.5.1-2
- Package gtk docs as part of devel package.
- Nuke static library.
- Update devel files so /usr/include/cairo is owned by devel package.

* Mon Jun 20 2005 Kristian Høgsberg <krh@redhat.com> - 0.5.1-1
- Update to cairo 0.5.1.
- Remove gtk-doc files, since --disable-gtk-doc doesn't work.
- Disable gtk-doc and add freetype and fontconfig BuildRequires.

* Tue Jun 14 2005 Kristian Høgsberg <krh@redhat.com> - 0.5.0-2
- Add libpixman-devel BuildRequires.
- Explicitly disable win32 backend.

* Tue May 17 2005 Kristian Høgsberg <krh@redhat.com> - 0.5.0-1
- Update to 0.5.0.

* Sun Jan 23 2005 Kristian Høgsberg <krh@redhat.com> - 0.3.0-1
- Update to 0.3.0, explicitly disable more backends.

* Tue Nov 16 2004 Kristian Høgsberg <krh@redhat.com> - 0.2.0-1
- Incorporate changes suggested by katzj: Require: ldconfig and run it
  in %%post and %%postun, don't pass CFLAGS to make.

* Mon Aug  9 2004 Kristian Høgsberg <krh@redhat.com> - 0.2.0-1
- Update license, explicitly disable glitz.
- Create package.
