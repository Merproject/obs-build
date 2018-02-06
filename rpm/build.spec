#
# spec file for package build
#
# Copyright (c) 2012 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

%define _binaries_in_noarch_packages_terminate_build 0

Name:           build
Summary:        A Script to Build SUSE Linux RPMs
License:        GPL-2.0+
Group:          Development/Tools/Building
Version:        20140801
Release:        mer2
#!BuildIgnore:  build-mkbaselibs
Source:         build-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
# Manual requires to avoid hard require to bash-static
AutoReqProv:    off
# Keep the following dependencies in sync with obs-worker package
Requires:       bash
Requires:       perl
Requires:       binutils
Requires:       tar
%if 0%{?fedora}
Requires:       perl-MD5
Requires:       perl-TimeDate
%endif
Conflicts:      bsdtar < 2.5.5
Provides:       perl(Build)
Provides:       perl(Build::Arch)
Provides:       perl(Build::Deb)
Provides:       perl(Build::Kiwi)
Provides:       perl(Build::Rpm)
Provides:       perl(Build::Susetags)
Provides:       perl(Build::Zypp)
%if 0%{?suse_version} > 1000
# None of them are actually required for core features.
# Perl helper scripts use them.
Recommends:     perl(Date::Language)
Recommends:     perl(Date::Parse)
Recommends:     perl(LWP::UserAgent)
Recommends:     perl(Pod::Usage)
Recommends:     perl(Time::Zone)
Recommends:     perl(URI)
Recommends:     perl(XML::Parser)
Recommends:     bsdtar
%endif

%if 0%{?suse_version} > 1120 || ! 0%{?suse_version}
Requires:       build-mkbaselibs
%endif

%if 0%{?suse_version} > 1120 || 0%{?mdkversion}
Recommends:     build-mkdrpms
%endif

%description
This package provides a script for building RPMs for SUSE Linux in a
chroot environment.


%if 0%{?suse_version} > 1120 || ! 0%{?suse_version}

%package mkbaselibs
Summary:        Tools to generate base lib packages
Group:          Development/Tools/Building
# NOTE: this package must not have dependencies which may break boot strapping (eg. perl modules)

%description mkbaselibs
This package contains the parts which may be installed in the inner build system
for generating base lib packages.

%package mkdrpms
Summary:        Tools to generate delta rpms
Group:          Development/Tools/Building
Requires:       deltarpm
# XXX: we wanted to avoid that but mkdrpms needs Build::Rpm::rpmq
Requires:       build

%description mkdrpms
This package contains the parts which may be installed in the inner build system
for generating delta rpm packages.

%endif

%define initvm_arch %{_host_cpu}
%if %{_host_cpu} == "i686"
%define initvm_arch i586
%endif
%package initvm-%{initvm_arch}
Summary:        Virtualization initializer for emulated cross architecture builds
Group:          Development/Tools/Building
Requires:       build
BuildRequires:  gcc
BuildRequires:  glibc-devel
Provides:       build-initvm
Obsoletes:      build-initvm
%if 0%{?suse_version} > 1200
BuildRequires:  glibc-devel-static
%endif
%if 0%{?fedora}
BuildRequires:  glibc-static
%endif

%description initvm-%{initvm_arch}
This package provides a script for building RPMs for SUSE Linux in a
chroot or a secure virtualized

%prep
%setup -q

%build

%install
make DESTDIR=$RPM_BUILD_ROOT install
cd $RPM_BUILD_ROOT/usr/lib/build/configs/
%if 0%{?suse_version}
%if 0%{?sles_version}
 ln -s sles%{sles_version}.conf default.conf
%else
 V=%suse_version
 ln -s sl${V:0:2}.${V:2:1}.conf default.conf
%endif
test -e default.conf
%endif

%files
%defattr(-,root,root)
%doc README
/usr/bin/build
/usr/bin/buildvc
/usr/bin/unrpm
/usr/lib/build
%{_mandir}/man1/build.1*

%if 0%{?suse_version} > 1120 || ! 0%{?suse_version}
%exclude /usr/lib/build/mkbaselibs
%exclude /usr/lib/build/baselibs*
%exclude /usr/lib/build/mkdrpms

%files mkbaselibs
%defattr(-,root,root)
%dir /usr/lib/build
/usr/lib/build/mkbaselibs
/usr/lib/build/baselibs*

%files mkdrpms
%defattr(-,root,root)
%dir /usr/lib/build
/usr/lib/build/mkdrpms
%endif

%changelog
