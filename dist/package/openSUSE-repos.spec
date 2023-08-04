#
# spec file
#
# Copyright (c) 2022 SUSE LLC
# Copyright (c) 2022 Neal Gompa <ngompa13@gmail.com>
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


%global debug_package %{nil}

%if "@BUILD_FLAVOR@" == ""
ExclusiveArch:  do_not_build
%endif

# Each openSUSE release package has a suggests for openSUSE-repos-$flavor.
%global flavor @BUILD_FLAVOR@%nil

%if 0%{?is_opensuse} && 0%{?suse_version} >= 1550
# Tumbleweed
%if "%flavor" == "openSUSE-repos-Tumbleweed"
%define theme Tumbleweed
%define branding tumbleweed
%endif
%if "%flavor" == "openSUSE-repos-MicroOS"
%define theme MicroOS
%define branding microos
%endif
# ALP -> Leap 16 does not use sle_version, ALP also uses is_opensuse 1
%if "%flavor" == "openSUSE-repos-Leap16"
%define theme Leap16
%define branding leap16
%endif
%endif

%if 0%{?sle_version}
# Leap
%if 0%{?is_leapmicro}
%if "%flavor" == "openSUSE-repos-LeapMicro"
%define theme LeapMicro
%define branding leap-micro
%endif
%else
%if "%flavor" == "openSUSE-repos-Leap"
%define theme Leap
%define branding leap
%endif
%endif
%endif

%if "%{?theme}" == ""
ExclusiveArch:  do_not_build
%endif

%if "@BUILD_FLAVOR@" == ""
Name:           openSUSE-repos
%else
Name:           openSUSE-repos-%{theme}
%endif
Version:        0
Release:        0
Summary:        openSUSE package repositories
License:        MIT
Group:          System/Management
URL:            https://github.com/openSUSE/openSUSE-repos
Source:         openSUSE-repos-%{version}.tar.xz
#boo#1203715
BuildRequires:  -post-build-checks
Requires:       zypper
Conflicts:      otherproviders(openSUSE-repos)
Provides:       openSUSE-repos
%if "%{?theme}" == "Tumbleweed"
Obsoletes:      openSUSE-repos-Leap
Obsoletes:      openSUSE-repos-LeapMicro
%endif
%if "%{?theme}" == "MicroOS"
Obsoletes:      openSUSE-repos-Leap
Obsoletes:      openSUSE-repos-LeapMicro
%endif
%if "%{?theme}" == "Leap16"
Obsoletes:      openSUSE-repos-Leap
Obsoletes:      openSUSE-repos-LeapMicro
%endif
# Ensure we install matching packages on given distribution
# openSUSE-release has suggest on particular theme based on distribution
Suggests:       openSUSE-repos-%{theme}-NVIDIA

%description
Definitions for openSUSE repository management via zypp-services

%package NVIDIA
Summary:        openSUSE NVIDIA repository definitions
Requires:       openSUSE-repos
Provides:       openSUSE-repos-NVIDIA
%if "%{?theme}" == "Tumbleweed"
Obsoletes:      openSUSE-repos-Leap-NVIDIA
Obsoletes:      openSUSE-repos-LeapMicro-NVIDIA
%endif
%if "%{?theme}" == "MicroOS"
Obsoletes:      openSUSE-repos-Leap-NVIDIA
Obsoletes:      openSUSE-repos-LeapMicro-NVIDIA
%endif
%if "%{?theme}" == "Leap16"
Obsoletes:      openSUSE-repos-Leap-NVIDIA
Obsoletes:      openSUSE-repos-LeapMicro-NVIDIA
%endif

%description NVIDIA
Definitions for NVIDIA repository management via zypp-services

%files

%dir %{_datadir}/zypp/local/
%dir %{_datadir}/zypp/local/service
%dir %{_datadir}/zypp/local/service/openSUSE
%dir %{_datadir}/zypp/local/service/openSUSE/repo
%ghost %{_datadir}/zypp/local/service/openSUSE/repo/repoindex.xml
%ghost %{_sysconfdir}/zypp/services.d/openSUSE.service
%{_sysconfdir}/zypp/vars.d/DIST_ARCH

%if "%{theme}" == "Tumbleweed"
%ifarch %{ix86} x86_64
%{_datadir}/zypp/local/service/openSUSE/repo/opensuse-%{branding}-repoindex.xml
%else
%{_datadir}/zypp/local/service/openSUSE/repo/opensuse-%{branding}-ports-repoindex.xml
%endif
%endif

%if "%{theme}" == "MicroOS"
%ifarch x86_64 aarch64
%{_datadir}/zypp/local/service/openSUSE/repo/opensuse-%{branding}-repoindex.xml
%endif
%endif

%if "%{theme}" == "LeapMicro"
%ifarch x86_64 aarch64
%{_datadir}/zypp/local/service/openSUSE/repo/opensuse-%{branding}-repoindex.xml
%endif
%endif

%if "%{theme}" == "Leap"
%ifarch %{ix86} x86_64 aarch64 ppc64le s390x
%{_datadir}/zypp/local/service/openSUSE/repo/opensuse-%{branding}-repoindex.xml
%else
%{_datadir}/zypp/local/service/openSUSE/repo/opensuse-%{branding}-ports-repoindex.xml
%endif
%endif

%if "%{theme}" == "Leap16"
%ifarch %{ix86} x86_64 aarch64
%{_datadir}/zypp/local/service/openSUSE/repo/opensuse-%{branding}-repoindex.xml
%else
%{_datadir}/zypp/local/service/openSUSE/repo/opensuse-%{branding}-ports-repoindex.xml
%endif
%endif

%if "0%{?with_nvidia}"
%files NVIDIA
%dir %{_datadir}/zypp/local/service/NVIDIA
%dir %{_datadir}/zypp/local/service/NVIDIA/repo
%ghost %{_datadir}/zypp/local/service/NVIDIA/repo/repoindex.xml
/usr/share/zypp/local/service/NVIDIA/repo/nvidia-%{branding}-repoindex.xml
%ghost %{_sysconfdir}/zypp/services.d/openSUSE.service
%{_datadir}/zypp/local/service/NVIDIA/repo/nvidia-%{branding}-repoindex.xml
%endif

%prep
%setup -q -n openSUSE-repos-%{version}

%build
# Nothing to build

%install

mkdir -p %{buildroot}%{_datadir}/zypp/local/service/openSUSE/repo
mkdir -p %{buildroot}%{_datadir}/zypp/local/service/NVIDIA/repo
mkdir -p %{buildroot}%{_sysconfdir}/zypp/vars.d/

# Setup for primary arches
%if "%{theme}" == "Tumbleweed"
%ifarch %{ix86} x86_64
install opensuse-%{branding}-repoindex.xml -pm 0644 %{buildroot}%{_datadir}/zypp/local/service/openSUSE/repo
%else ifarch aarch64 %{arm} %{power64} ppc s390x riscv64
install opensuse-%{branding}-ports-repoindex.xml -pm 0644 %{buildroot}%{_datadir}/zypp/local/service/openSUSE/repo
%endif
%endif

%if "%{theme}" == "MicroOS"
%ifarch x86_64 aarch64
install opensuse-%{branding}-repoindex.xml -pm 0644 %{buildroot}%{_datadir}/zypp/local/service/openSUSE/repo
%endif
%endif

%if "%{theme}" == "LeapMicro"
%ifarch x86_64 aarch64
install opensuse-%{branding}-repoindex.xml -pm 0644 %{buildroot}%{_datadir}/zypp/local/service/openSUSE/repo
%endif
%endif

%if "%{theme}" == "Leap"
%ifarch %{ix86} x86_64 aarch64 ppc64le s390x
install opensuse-%{branding}-repoindex.xml -pm 0644 %{buildroot}%{_datadir}/zypp/local/service/openSUSE/repo
%else
install opensuse-%{branding}-ports-repoindex.xml -pm 0644 %{buildroot}%{_datadir}/zypp/local/service/openSUSE/repo
%endif
%endif

%if "0%{?with_nvidia}"
install nvidia-%{branding}-repoindex.xml -pm 0644 %{buildroot}%{_datadir}/zypp/local/service/NVIDIA/repo
%endif

%ifarch %{ix86}
echo "x86" >  %{buildroot}%{_sysconfdir}/zypp/vars.d/DIST_ARCH
%endif

%ifarch x86_64
echo "x86_64" >  %{buildroot}%{_sysconfdir}/zypp/vars.d/DIST_ARCH
%endif

%ifarch aarch64
echo "aarch64" >  %{buildroot}%{_sysconfdir}/zypp/vars.d/DIST_ARCH
%endif

%ifarch armv6l armv6hl
echo "armv6hl" >  %{buildroot}%{_sysconfdir}/zypp/vars.d/DIST_ARCH
%endif

%ifarch armv7l armv7hl
echo "armv7hl" >  %{buildroot}%{_sysconfdir}/zypp/vars.d/DIST_ARCH
%endif

%ifarch ppc ppc64 ppc64le
echo "ppc" >  %{buildroot}%{_sysconfdir}/zypp/vars.d/DIST_ARCH
%endif

%ifarch riscv64
echo "riscv" >  %{buildroot}%{_sysconfdir}/zypp/vars.d/DIST_ARCH
%endif

%ifarch s390x
echo "zsystems" >  %{buildroot}%{_sysconfdir}/zypp/vars.d/DIST_ARCH
%endif

%post
%if "%{theme}" == "Tumbleweed"
%ifarch %{ix86} x86_64
ln -sf opensuse-%{branding}-repoindex.xml %{_datadir}/zypp/local/service/openSUSE/repo/repoindex.xml
%else
ln -sf opensuse-%{branding}-ports-repoindex.xml %{_datadir}/zypp/local/service/openSUSE/repo/repoindex.xml
%endif
%endif

%if "%{theme}" == "MicroOS"
%ifarch x86_64 aarch64
ln -sf opensuse-%{branding}-repoindex.xml %{_datadir}/zypp/local/service/openSUSE/repo/repoindex.xml
%endif
%endif

%if "%{theme}" == "LeapMicro"
%ifarch x86_64 aarch64
ln -sf opensuse-%{branding}-repoindex.xml %{_datadir}/zypp/local/service/openSUSE/repo/repoindex.xml
%endif
%endif

%if "%{theme}" == "Leap"
%ifarch %{ix86} x86_64 aarch64 ppc64le s390x
ln -sf opensuse-%{branding}-repoindex.xml %{_datadir}/zypp/local/service/openSUSE/repo/repoindex.xml
%else
ln -sf opensuse-%{branding}-ports-repoindex.xml %{_datadir}/zypp/local/service/openSUSE/repo/repoindex.xml
%endif
%endif

# Disable all non-zypp-service managed repos with default filenames

for repo_file in \
repo-backports-debug-update.repo repo-oss.repo repo-backports-update.repo \
repo-sle-debug-update.repo repo-debug-non-oss.repo repo-sle-update.repo \
repo-debug.repo repo-source.repo repo-debug-update.repo repo-update.repo \
repo-debug-update-non-oss.repo repo-update-non-oss.repo repo-non-oss.repo \
openSUSE-*-0.repo download.opensuse.org-oss.repo download.opensuse.org-tumbleweed.repo \
repo-openh264.repo; do
  if [ -f %{_sysconfdir}/zypp/repos.d/$repo_file ]; then
    echo "Content of $repo_file will be newly managed by zypp-services."
    echo "Storing old copy as {_sysconfdir}/zypp/repos.d/$repo_file.rpmsave"
    mv %{_sysconfdir}/zypp/repos.d/$repo_file %{_sysconfdir}/zypp/repos.d/$repo_file.rpmsave
  fi
done

# We hereby declare that running this will not influence existing transaction
ZYPP_READONLY_HACK=1 zypper addservice %{_datadir}/zypp/local/service/openSUSE openSUSE

%if "0%{?with_nvidia}"
%post NVIDIA
ln -sf nvidia-%{branding}-repoindex.xml %{_datadir}/zypp/local/service/NVIDIA/repo/repoindex.xml

# Disable user-defined with default filename from wiki
# https://en.opensuse.org/SDB:NVIDIA_drivers#Zypper
for repo_file in NVIDIA.repo ; do
  if [ -f %{_sysconfdir}/zypp/repos.d/$repo_file ]; then
    echo "Content of $repo_file will be newly managed by zypp-services."
    echo "Storing old copy as {_sysconfdir}/zypp/repos.d/$repo_file.rpmsave"
    mv %{_sysconfdir}/zypp/repos.d/$repo_file %{_sysconfdir}/zypp/repos.d/$repo_file.rpmsave
  fi
done

# We hereby declare that running this will not influence existing transaction
ZYPP_READONLY_HACK=1 zypper addservice %{_datadir}/zypp/local/service/NVIDIA NVIDIA
%endif

%postun
if [ "$1" = 0 ] ; then
  # We hereby declare that running this will not influence existing transaction
  ZYPP_READONLY_HACK=1 zypper removeservice openSUSE
  if [ -L "%{_datadir}/zypp/local/service/openSUSE/repo/repoindex.xml" ] ; then
    rm -f %{_datadir}/zypp/local/service/openSUSE/repo/repoindex.xml
  fi
fi

%postun NVIDIA
if [ "$1" = 0 ] ; then
  # We hereby declare that running this will not influence existing transaction
  ZYPP_READONLY_HACK=1 zypper removeservice NVIDIA
  if [ -L "%{_datadir}/zypp/local/service/NVIDIA/repo/repoindex.xml" ] ; then
    rm -f %{_datadir}/zypp/local/service/NVIDIA/repo/repoindex.xml
  fi
fi

%changelog
