#
# Conditional build:
%bcond_without	tests		# do not perform "make test"
#
%define		pdir	Data
%define		pnam	Dump-Streamer
%include	/usr/lib/rpm/macros.perl
Summary:	Data::Dump::Streamer - Accurately serialize a data structure as Perl code
Name:		perl-Data-Dump-Streamer
Version:	2.39
Release:	1
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/Data/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	5cd6fe67653c8de544fa41930de157b7
URL:		http://search.cpan.org/dist/Data-Dump-Streamer/
BuildRequires:	perl-Module-Build
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
BuildRequires:	perl-B-Utils
BuildRequires:	perl-PadWalker
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Given a list of scalars or reference variables, writes out their
contents in perl syntax. The references can also be objects. The
contents of each variable is output using the least number of Perl
statements as convenient, usually only one. Self-referential
structures, closures, and objects are output correctly.

The return value can be evaled to get back an identical copy of the
original reference structure. In some cases this may require the use
of utility subs that Data::Dump::Streamer will optionally export.

This module is very similar in concept to the core module
Data::Dumper, with the major differences being that this module is
designed to output to a stream instead of constructing its output in
memory (trading speed for memory), and that the traversal over the
data structure is effectively breadth first versus the depth first
traversal done by the others.

In fact the data structure is scanned twice, first in breadth first
mode to perform structural analysis, and then in depth first mode to
actually produce the output, but obeying the depth relationships of
the first pass.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
%{__perl} Build.PL NODDS \
	destdir=$RPM_BUILD_ROOT \
	installdirs=vendor
./Build

%{?with_tests:./Build test}

%install
rm -rf $RPM_BUILD_ROOT

./Build install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README
%dir %{perl_vendorarch}/Data/Dump
%{perl_vendorarch}/Data/Dump/*.pm
%{perl_vendorarch}/Data/Dump/Streamer
%dir %{perl_vendorarch}/auto/Data/Dump
%dir %{perl_vendorarch}/auto/Data/Dump/Streamer
%attr(755,root,root) %{perl_vendorarch}/auto/Data/Dump/Streamer/Streamer.so
%{_mandir}/man3/*
