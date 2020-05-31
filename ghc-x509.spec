#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	x509
Summary:	X509 reader and writer
Name:		ghc-%{pkgname}
Version:	1.7.5
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/x509
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	838bf3fc8bf7d08e07faeaacd234a24c
URL:		http://hackage.haskell.org/package/x509
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-asn1-encoding
BuildRequires:	ghc-asn1-parse >= 0.9.3
BuildRequires:	ghc-asn1-types >= 0.3.1
BuildRequires:	ghc-cryptonite >= 0.24
BuildRequires:	ghc-hourglass
BuildRequires:	ghc-memory
BuildRequires:	ghc-pem >= 0.1
%if %{with prof}
BuildRequires:	ghc-prof
BuildRequires:	ghc-asn1-encoding-prof
BuildRequires:	ghc-asn1-parse-prof >= 0.9.3
BuildRequires:	ghc-asn1-types-prof >= 0.3.1
BuildRequires:	ghc-cryptonite-prof >= 0.24
BuildRequires:	ghc-hourglass-prof
BuildRequires:	ghc-memory-prof
BuildRequires:	ghc-pem-prof >= 0.1
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	ghc-asn1-encoding
Requires:	ghc-asn1-parse >= 0.9.3
Requires:	ghc-asn1-types >= 0.3.1
Requires:	ghc-cryptonite >= 0.24
Requires:	ghc-hourglass
Requires:	ghc-memory
Requires:	ghc-pem >= 0.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
X509 reader and writer.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-asn1-encoding-prof
Requires:	ghc-asn1-parse-prof >= 0.9.3
Requires:	ghc-asn1-types-prof >= 0.3.1
Requires:	ghc-cryptonite-prof >= 0.24
Requires:	ghc-hourglass-prof
Requires:	ghc-memory-prof
Requires:	ghc-pem-prof >= 0.1

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/X509
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/X509/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/X509/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/X509/*.p_hi
%endif
