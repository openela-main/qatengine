# SPDX-License-Identifier: MIT

# Build as an OpenSSL provider instead of as an engine
%bcond provider %[0%{?fedora} >= 41 || 0%{?rhel} >= 10]
# QAT_HW only acceleration for RHEL
%bcond sw %{undefined rhel}

# Define the directory where the OpenSSL engines are installed
%if %{with provider}
%global modulesdir %(pkg-config --variable=modulesdir libcrypto)
%else
%global enginesdir %(pkg-config --variable=enginesdir libcrypto)
%endif

Name:           qatengine
Version:        1.7.0
Release:        1%{?dist}
Summary:        Intel QuickAssist Technology (QAT) OpenSSL Engine

# Most of the source code is BSD, with the following exceptions:
#  - e_qat.txt, e_qat_err.c, and e_qat_err.h are OpenSSL
#  - qat_hw_config/* are (BSD or GPLv2), but are not used during compilation
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
%endif
BuildRequires:  openssl

%description
This package provides the Intel QuickAssist Technology OpenSSL Engine
(an OpenSSL Plug-In Engine) which provides cryptographic acceleration
for both hardware and optimized software using Intel QuickAssist Technology
enabled Intel platforms.

%prep
%autosetup -n QAT_Engine-%{version}

%build
autoreconf -ivf
%configure %{?with_sw:--enable-qat_sw} %{?with_provider:--enable-qat_provider}
%make_build

%install
%make_install

%if 0%{?rhel}
find %{buildroot} -name "*.la" -delete
%endif

%check
%if %{with provider}
export OPENSSL_MODULES=%{buildroot}%{modulesdir}
openssl list -providers -provider qatprovider
%else
export OPENSSL_ENGINES=%{buildroot}%{enginesdir}
openssl engine -v %{name}
%endif

%files
%license LICENSE*
%doc README.md docs*
%if %{with provider}
%{modulesdir}/qatprovider.so
%else
%{enginesdir}/%{name}.so
%endif

%changelog
* Thu Nov 07 2024 Vladis Dronov <vdronov@redhat.com> - 1.7.0-1
- Update to qatengine v1.7.0 @ ceb9d4ac (RHEL-54171)
- Remove qat_contig_mem from upstream package
- Build as a provider for RHEL-10

* Tue Oct 29 2024 Troy Dawson <tdawson@redhat.com> - 1.6.0-3
- Bump release for October 2024 mass rebuild (RHEL-64018)

* Mon Jun 24 2024 Troy Dawson <tdawson@redhat.com> - 1.6.0-2
- Bump release for June 2024 mass rebuild

* Fri Mar 22 2024 Vladis Dronov <vdronov@redhat.com> - 1.6.0-1
- Update to qatengine v1.6.0 (RHEL-20177)

* Fri Jan 26 2024 Vladis Dronov <vdronov@redhat.com> - 1.5.0-3
- Initial import from Fedora 40
