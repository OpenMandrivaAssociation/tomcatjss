Name:     tomcatjss
Version:  2.1.1
Release:  3
Summary:  JSSE implementation using JSS for Tomcat
URL:      https://pki.fedoraproject.org/
License:  LGPLv2+
Group:    System/Libraries

BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

Source0:  http://pki.fedoraproject.org/pki/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires:    ant
BuildRequires:    java-devel >= 0:1.6.0
BuildRequires:    jpackage-utils
%if 0%{?fedora} >= 15
BuildRequires:    tomcat6 >= 6.0.30-6
%else
BuildRequires:    tomcat6
%endif
BuildRequires:    jss >= 4.2.6-15

Requires:         java >= 0:1.6.0
Requires:         jpackage-utils
%if 0%{?fedora} >= 15
Requires:         tomcat6 >= 6.0.30-6
%else
Requires:         tomcat6
%endif
Requires:         jss >= 4.2.6-15

# The 'tomcatjss' package conflicts with the 'tomcat-native' package
# because it uses an underlying NSS security model rather than the
# OpenSSL security model, so these two packages may not co-exist.
# (see Bugzilla Bug #441974 for details)
Conflicts:        tomcat-native

%if 0%{?rhel}
# For EPEL, override the '_sharedstatedir' macro on RHEL
%define           _sharedstatedir    /var/lib
%endif

%description
A Java Secure Socket Extension (JSSE) implementation
using Java Security Services (JSS) for Tomcat 6.

NOTE:  The 'tomcatjss' package conflicts with the 'tomcat-native' package
       because it uses an underlying NSS security model rather than the
       OpenSSL security model, so these two packages may not co-exist.

%prep

%setup -q

%build

ant -f build.xml
ant -f build.xml dist

%install
rm -rf %{buildroot}

# Unpack the files we just built
cd dist/binary
unzip %{name}-%{version}.zip -d %{buildroot}

# Install our files
cd %{buildroot}%{_javadir}
mv %{name}.jar %{name}-%{version}.jar
ln -s %{name}-%{version}.jar %{name}.jar
mkdir -p %{buildroot}%{_datadir}/doc/%{name}-%{version}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc %attr(644,root,root) README LICENSE
%attr(00755,root,root) %{_datadir}/doc/%{name}-%{version}
%{_javadir}/*

