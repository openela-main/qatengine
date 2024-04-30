# SPDX-License-Identifier: MIT

# Define the directory where the OpenSSL engines are installed
%global enginesdir %(pkg-config --variable=enginesdir libcrypto)

Name:           qatengine
Version:        1.4.0
Release:        1%{?dist}
Summary:        Intel QuickAssist Technology (QAT) OpenSSL Engine

# Most of the source code is BSD, with the following exceptions:
#  - e_qat.txt, e_qat_err.c, and e_qat_err.h are OpenSSL
#  - qat/config/* are (BSD or GPLv2), but are not used during compilation
#  - qat_contig_mem/* are GPLv2, but are not used during compilation
License:        BSD-3-Clause AND OpenSSL
URL:            https://github.com/intel/QAT_Engine
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# https://bugzilla.redhat.com/show_bug.cgi?id=1909065
ExclusiveArch:  x86_64

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  openssl-devel >= 1.1.1
BuildRequires:  qatlib-devel >= 23.02.0
%if !0%{?rhel}
BuildRequires:  intel-ipp-crypto-mb-devel >= 1.0.6
BuildRequires:  intel-ipsec-mb-devel >= 1.3.0
BuildRequires:  openssl
%endif

%description
This package provides the Intel QuickAssist Technology OpenSSL Engine
(an OpenSSL Plug-In Engine) which provides cryptographic acceleration
for both hardware and optimized software using Intel QuickAssist Technology
enabled Intel platforms.

%prep
%autosetup -n QAT_Engine-%{version}

%build
autoreconf -ivf
%if !0%{?rhel}
# Enable QAT_HW & QAT_SW Co-existence acceleration
%configure --enable-qat_sw
%else
# QAT_HW only acceleration for RHEL
%configure
%endif
%make_build

%install
%make_install

%if 0%{?rhel}
find %{buildroot} -name "*.la" -delete
%endif

%if !0%{?rhel}
%check
export OPENSSL_ENGINES=%{buildroot}%{enginesdir}
openssl engine -v %{name}
%endif

%files
%license LICENSE*
%doc README.md docs*
%{enginesdir}/%{name}.so

%changelog
* Mon Nov 20 2023 Vladis Dronov <vdronov@redhat.com> - 1.4.0-1
- Update to qatengine v1.4.0 (RHEL-15636)
- Enable QAT_HW & QAT SW Co-ex Acceleration for non RHEL distros

* Fri Mar 31 2023 Vladis Dronov <vdronov@redhat.com> - 1.0.0-1
- Update to qatengine v1.0.0 (bz 2082432)

* Tue Mar 07 2023 Vladis Dronov <vdronov@redhat.com> - 0.6.19-1
- Update to qatengine v0.6.19 (bz 2082432)

* Tue Sep 06 2022 Vladis Dronov <vdronov@redhat.com> - 0.6.15-2
- Rebuild due to soverion bump (bz 2047717)

* Mon Aug 29 2022 Vladis Dronov <vdronov@redhat.com> - 0.6.15-1
- Update to qatengine v0.6.15 (bz 2047717)

* Wed Aug 10 2022 Vladis Dronov <vdronov@redhat.com> - 0.6.14-2
- Rebuild due to soverion bump (bz 2047717)

* Fri Jul 22 2022 Vladis Dronov <vdronov@redhat.com> - 0.6.14-1
- Update to qatengine v0.6.14 (bz 2047717)

* Mon Nov 15 2021 Vladis Dronov <vdronov@redhat.com> - 0.6.10-1
- Update to qatengine v0.6.10 (bz 2012945)
- Add OSCI testing harness

* Wed Aug 18 2021 Vladis Dronov <vdronov@redhat.com> - 0.6.7-1
- Update to qatengine v0.6.7 with openssl-3 support (bz 1874206, bz 1953498)
- Add documentation files to a package

* Tue Aug 10 2021 Mohan Boddu <mboddu@redhat.com> - 0.6.4-4
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 0.6.4-3
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Fri Dec 11 2020 Yogaraj Alamenda <yogarajx.alamenda@intel.com> 0.6.4-1
- Update to qatengine v0.6.4

* Mon Nov 30 2020 Yogaraj Alamenda <yogarajx.alamenda@intel.com> 0.6.3-1
- Update to qatengine v0.6.3
- Update License and library installation

* Wed Nov 18 2020 Dinesh Balakrishnan <dineshx.balakrishnan@intel.com> 0.6.2-1
- Update to qatengine v0.6.2
- Address review comments

* Tue Sep 08 2020 Dinesh Balakrishnan <dineshx.balakrishnan@intel.com> 0.6.1-1
- Initial version of rpm package
