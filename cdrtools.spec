%define beta a07
# Build system doesn't support DI generation
%define debug_package %{nil}

%bcond_with alsa
%bcond_with pulse

Name: cdrtools
Version: 3.02
Release: 2
Source0: http://downloads.sourceforge.net/cdrtools/%{name}-%{version}%{?beta:%{beta}}.tar.bz2
Summary: Tools for working with writable CD, DVD and BluRay media
URL: http://cdrtools.sourceforge.net/
License: Various Open Source Licenses (CDDL.Schily, GPL-2.0, LGPL-2.1, BSD)
Group: Archiving/Cd burning
BuildRequires: %{_lib}cap-devel
%if %{with alsa}
BuildRequires: pkgconfig(alsa)
%endif
%if %{with pulse}
BuildRequires: pkgconfig(libpulse)
%endif
Obsoletes: cdrkit < 1.1.11-11
Obsoletes: cdrkit-genisoimage < 1.1.11-11
Provides: cdrecord = %{EVRD}
Provides: mkisofs = %{EVRD}
Requires(post): libcap-utils
Conflicts: man-pages < 4.05-1

%description
Cdrtools is a set of command line programs that allows to
record CD/DVD/BluRay media.

The suite includes the following programs:

  cdrecord  A CD/DVD/BD recording program 
  readcd    A program to read CD/DVD/BD media with CD-clone features 
  cdda2wav  The most evolved CD-audio extraction program with paranoia support 
  mkisofs   A program to create hybrid ISO-9660/Joliet/HFS filesystems
            with optional Rock Ridge attributes 
  isodebug  A program to print mkisofs debug information from media 
  isodump   A program to dump ISO-9660 media 
  isoinfo   A program to analyse/verify ISO-9660/Joliet/Rock-Ridge filesystems 
  isovfy    A program to verify the ISO-9660 structures 
  rscsi     A Remote SCSI enabling daemon 

%prep
%setup -q
sed -i -e 's,^INS_BASE=.*,INS_BASE=%{_prefix},g' DEFAULTS/*
sed -i -e 's,-noclobber,,' cdrecord/Makefile.dfl
# Remove lib*/*_p.mk to skip the compilation of profiled libs
rm -f lib*/*_p.mk
%ifarch %ix86
# doesnt work with clang on i586
sed -i -e 's,^DEFCCOM=.*,DEFCCOM=gcc,g' DEFAULTS/*
%endif

%build
# The Makefile system isn't 100% ready for an SMP build
%make -j1

%install
%makeinstall_std

# Not much of a point in shipping static libs and headers for libs used
# only by cdrtools
rm -rf \
	%{buildroot}%{_prefix}/lib/*.a \
	%{buildroot}%{_includedir}

# We get this from dvd+rw-tools
rm -f %{buildroot}%{_bindir}/btcflash

rm -rf %{buildroot}%{_mandir}/man3/fexecve.3* \
	%{buildroot}%{_mandir}/man3/fnmatch.3* \
	%{buildroot}%{_mandir}/man3/fprintf.3* \
	%{buildroot}%{_mandir}/man3/getline.3* \
	%{buildroot}%{_mandir}/man3/printf.3* \
	%{buildroot}%{_mandir}/man3/sprintf.3* \
	%{buildroot}%{_mandir}/man3/strlen.3* \
	%{buildroot}%{_mandir}/man3/error.3*

%post
%{_sbindir}/setcap cap_sys_resource,cap_dac_override,cap_sys_admin,cap_sys_nice,cap_net_bind_service,cap_ipc_lock,cap_sys_rawio+ep %{_bindir}/cdrecord
%{_sbindir}/setcap cap_dac_override,cap_sys_admin,cap_sys_nice,cap_net_bind_service,cap_sys_rawio+ep %{_bindir}/cdda2wav
%{_sbindir}/setcap cap_dac_override,cap_sys_admin,cap_net_bind_service,cap_sys_rawio+ep %{_bindir}/readcd

%files
%{_bindir}/*
%{_sbindir}/rscsi
%{_prefix}/lib/siconv
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_sysconfdir}/default/cdrecord
%{_sysconfdir}/default/rscsi
%doc %{_docdir}/mkisofs
%doc %{_docdir}/libparanoia
%doc %{_docdir}/rscsi
%doc %{_docdir}/cdda2wav
%doc %{_docdir}/cdrecord
