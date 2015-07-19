%define beta a23
# Build system doesn't support DI generation
%define debug_package %{nil}

Name: cdrtools
Version: 3.01
Release: 5
Source0: ftp://ftp.berlios.de/pub/cdrecord/alpha/%{name}-%{version}%{?beta:%{beta}}.tar.bz2
Summary: Tools for working with writable CD, DVD and BluRay media
URL: http://cdrecord.berlios.de/
License: Various Open Source Licenses (GPL, CDDL, BSD)
Group: Archiving/Cd burning
BuildRequires: %{_lib}cap-devel
Obsoletes: cdrkit < 1.1.11-11
Obsoletes: cdrkit-genisoimage < 1.1.11-11
Provides: cdrecord = %{EVRD}
Provides: mkisofs = %{EVRD}
Requires(post): libcap-utils
 
%description
Cdrtools is a set of command line programs that allows to
record CD/DVD/BluRay media.

The suite includes the following programs:

  cdrecord  A CD/DVD/BD recording program 
  readcd    A program to read CD/DVD/BD media with CD-clone features 
  cdda2wav  The most evolved CD-audio extraction program with paranoia support 
  mkisofs   A program to create hybrid ISO9660/JOLIET/HFS filesystes
            with optional Rock Ridge attributes 
  isodebug  A program to print mkisofs debug information from media 
  isodump   A program to dump ISO-9660 media 
  isoinfo   A program to analyse/verify ISO/9660/Joliet/Rock-Ridge Filesystems 
  isovfy    A program to verify the ISO-9660 structures 
  rscsi     A Remote SCSI enabling daemon 

%prep
%setup -q
sed -i -e 's,^INS_BASE=.*,INS_BASE=%{_prefix},g' DEFAULTS/*

%build
# The Makefile system isn't 100% ready for an SMP build
make

%install
%makeinstall_std

# Not much of a point in shipping static libs and headers for libs used
# only by cdrtools
rm -rf \
	%{buildroot}%{_prefix}/lib/profiled \
	%{buildroot}%{_prefix}/lib/*.a \
	%{buildroot}%{_includedir}

# We get this from dvd+rw-tools
rm -f %{buildroot}%{_bindir}/btcflash

%post
%{_sbindir}/setcap cap_sys_resource,cap_dac_override,cap_sys_admin,cap_sys_nice,cap_net_bind_service,cap_ipc_lock,cap_sys_rawio+ep %{_bindir}/cdrecord
%{_sbindir}/setcap cap_dac_override,cap_sys_admin,cap_sys_nice,cap_net_bind_service,cap_sys_rawio+ep %{_bindir}/cdda2wav

%files
%{_bindir}/*
%{_sbindir}/rscsi
%{_prefix}/lib/siconv
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_sysconfdir}/default/cdrecord
%{_sysconfdir}/default/rscsi
%doc %{_docdir}/mkisofs
%doc %{_docdir}/libparanoia
%doc %{_docdir}/rscsi
%doc %{_docdir}/cdda2wav
%doc %{_docdir}/cdrecord
