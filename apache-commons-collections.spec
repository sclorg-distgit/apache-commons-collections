%{?scl:%scl_package apache-%{short_name}}
%{!?scl:%global pkg_name %{name}}

%global base_name       collections
%global short_name      commons-%{base_name}

Name:           %{?scl_prefix}apache-%{short_name}
Version:        3.2.2
Release:        4.2%{?dist}
Summary:        Provides new interfaces, implementations and utilities for Java Collections
License:        ASL 2.0
URL:            http://commons.apache.org/%{base_name}/
Source0:        http://www.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz

Patch0:         0001-Port-to-Java-8.patch

BuildArch:      noarch

BuildRequires:  %{?scl_prefix}ant
BuildRequires:  %{?scl_prefix}maven-local
BuildRequires:  %{?scl_prefix}mvn(org.apache.commons:commons-parent:pom:)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.plugins:maven-antrun-plugin)

%description
The introduction of the Collections API by Sun in JDK 1.2 has been a
boon to quick and effective Java programming. Ready access to powerful
data structures has accelerated development by reducing the need for
custom container classes around each core object. Most Java2 APIs are
significantly easier to use because of the Collections API.
However, there are certain holes left unfilled by Sun's
implementations, and the Jakarta-Commons Collections Component strives
to fulfill them. Among the features of this package are:
- special-purpose implementations of Lists and Maps for fast access
- adapter classes from Java1-style containers (arrays, enumerations) to
Java2-style collections.
- methods to test or create typical set-theory properties of collections
such as union, intersection, and closure.

%package testframework
Summary:        Testframework for %{pkg_name}
Requires:       %{name} = %{version}-%{release}

%description testframework
%{summary}.

%package javadoc
Summary:        Javadoc for %{pkg_name}
Provides:       %{name}-testframework-javadoc = %{version}-%{release}

%description javadoc
%{summary}.

%prep
%setup -q -n %{short_name}-%{version}-src

# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;
find . -name "*.class" -exec rm -f {} \;

%patch0 -p1

# Fix file eof
sed -i 's/\r//' LICENSE.txt PROPOSAL.html README.txt NOTICE.txt

%mvn_package :%{short_name}-testframework testframework
%mvn_file ':%{short_name}{,-testframework}' %{pkg_name}@1 %{short_name}@1

%build
%mvn_build

ant tf.javadoc -Dtf.build.docs=target/site/apidocs/

%mvn_artifact %{short_name}:%{short_name}-testframework:%{version} target/%{short_name}-testframework-%{version}.jar

%install
%mvn_install

# Workaround for RPM bug #646523 - can't change symlink to directory
%pretrans javadoc -p <lua>
dir = "%{_javadocdir}/%{pkg_name}"
dummy = posix.readlink(dir) and os.remove(dir)

%files -f .mfiles
%doc PROPOSAL.html README.txt LICENSE.txt NOTICE.txt

%files testframework -f .mfiles-testframework

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt

%changelog
* Thu Jun 22 2017 Michael Simacek <msimacek@redhat.com> - 3.2.2-4.2
- Mass rebuild 2017-06-22

* Wed Jun 21 2017 Java Maintainers <java-maint@redhat.com> - 3.2.2-4.1
- Automated package import and SCL-ization

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Mar 23 2016 Michael Simacek <msimacek@redhat.com> - 3.2.2-3
- Add workaround for symlink->directory rpm bug

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 16 2015 Michael Simacek <msimacek@redhat.com> - 3.2.2-1
- Update to upstream version 3.2.2
- Merge two javadoc subpackages
- Install with XMVn
- Specfile cleanup

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Oct 23 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.1-25
- Remove requires on apache-commons-parent

* Fri Oct 17 2014 Timothy St. Clair <tstclair@redhat.com> - 3.2.1-24
- Fix broken Java 8 build

* Tue Oct 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.1-23
- Remove legacy Obsoletes/Provides for jakarta-commons

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.1-21
- Use .mfiles generated during build

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.2.1-20
- Use Requires: java-headless rebuild (#1067528)

* Mon Aug 12 2013 Mat Booth <fedora@matbooth.co.uk> - 3.2.1-19
- Fix FTBFS rhbz #991965

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 29 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.1-17
- Remove unneeded BR: maven-idea-plugin

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 3.2.1-15
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 08 2012 Jaromir Capik <jcapik@redhat.com> 3.2.1-13
- saxon dependency removed - not needed
- minor spec file changes according to the latest guidelines

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 6 2011 Chris Spike <spike@fedoraproject.org> 3.2.1-11
- Added *-testframework depmap entries.

* Wed Mar 16 2011 Alexander Kurtakov <akurtako@redhat.com> 3.2.1-10
- Drop tomcat5 subpackage.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 8 2010 Alexander Kurtakov <akurtako@redhat.com> 3.2.1-8
- Add commons-collections:commons-collections depmap.

* Mon Oct 4 2010 Alexander Kurtakov <akurtako@redhat.com> 3.2.1-7
- Fix pom name.
- Use newer maven plugins names.

* Tue Aug 31 2010 Carl Green <carlgreen at gmail.com> - 3.2.1-6
- Change package to own files in directories, not the directories

* Mon Aug 30 2010 Carl Green <carlgreen at gmail.com> - 3.2.1-5
- Remove source and patches no longer needed for Maven
- Fix non-standard groups and remove empty sections
- Fix file permissions

* Sat Aug 28 2010 Carl Green <carlgreen at gmail.com> - 3.2.1-4
- Renamed from jakarta-commons-collections
- Updated to use maven2
- Replaced saxon:group instruction with xsl:for-each-group in pom-maven2jpp-newdepmap.xsl
