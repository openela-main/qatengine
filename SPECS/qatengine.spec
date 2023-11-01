# SPDX-License-Identifier: MIT

%global githubname QAT_Engine
%global enginesdir %(pkg-config --variable=enginesdir libcrypto)

Name:           qatengine
Version:        1.0.0
Release:        1%{?dist}
Summary:        Intel QuickAssist Technology (QAT) OpenSSL Engine
# Most of the source code is BSD, with the following exceptions:
#  - e_qat.txt, e_qat_err.c, and e_qat_err.h are OpenSSL
#  - qat/config/* are (BSD or GPLv2), but are not used during compilation
#  - qat_contig_mem/* are GPLv2, but are not used during compilation
License:        BSD and OpenSSL
URL:            https://github.com/intel/%{githubname}
Source0:        https://github.com/intel/%{githubname}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc make pkg-config
BuildRequires:  autoconf automake libtool
BuildRequires:  openssl-devel >= 1.1.1
BuildRequires:  qatlib-devel >= 21.08.0
# https://bugzilla.redhat.com/show_bug.cgi?id=1909065
ExcludeArch:    %{arm} aarch64 %{power64} s390x i686

%description
This package provides the Intel QuickAssist Technology OpenSSL Engine
(an OpenSSL Plug-In Engine) which provides cryptographic acceleration
for both hardware and optimized software using Intel QuickAssist Technology
enabled Intel platforms.

%prep
%autosetup -n %{githubname}-%{version}

%build
autoreconf -ivf
%configure
%make_build

%install
%make_install

%files
%license LICENSE*
%doc README.md docs*
%{enginesdir}/qatengine.so
%exclude %{enginesdir}/qatengine.la

%changelog
* Fri Mar 31 2023 Vladis Dronov <vdronov@redhat.com> - 1.0.0-1
- Update to qatengine v1.0.0 (bz 2176893)

* Tue Mar 07 2023 Vladis Dronov <vdronov@redhat.com> - 0.6.19-1
- Update to qatengine v0.6.19 (bz 2176893)

* Tue Sep 06 2022 Vladis Dronov <vdronov@redhat.com> - 0.6.15-2
- Rebuild due to soverion bump (bz 2048036)

* Mon Aug 29 2022 Vladis Dronov <vdronov@redhat.com> - 0.6.15-1
- Update to qatengine v0.6.15 (bz 2048036)

* Wed Aug 10 2022 Vladis Dronov <vdronov@redhat.com> - 0.6.14-2
- Rebuild due to soverion bump (bz 2048036)

* Fri Jul 22 2022 Vladis Dronov <vdronov@redhat.com> - 0.6.14-1
- Update to qatengine v0.6.14 (bz 2048036)

* Mon Nov 15 2021 Vladis Dronov <vdronov@redhat.com> - 0.6.10-1
- Update to qatengine v0.6.10 (bz 1995565)

* Fri Aug 27 2021 Vladis Dronov <vdronov@redhat.com> - 0.6.7-1
- Update to qatengine v0.6.7 (bz 1920338)

* Tue Jun  8 2021 Vladis Dronov <vdronov@redhat.com> - 0.6.6-1
- Update to qatengine v0.6.6 (bz 1920338)

* Tue Feb  9 2021 Vladis Dronov <vdronov@redhat.com> - 0.6.3-3
- Add OSCI testing harness (bz 1924868)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 30 2020 Yogaraj Alamenda <yogarajx.alamenda@intel.com> 0.6.3-1
- Update to qatengine v0.6.3
- Update License and library installation

* Wed Nov 18 2020 Dinesh Balakrishnan <dineshx.balakrishnan@intel.com> 0.6.2-1
- Update to qatengine v0.6.2
- Address review comments

* Tue Sep 08 2020 Dinesh Balakrishnan <dineshx.balakrishnan@intel.com> 0.6.1-1
- Initial version of rpm package
