%{?scl:%scl_package apache-commons-collections}
%{!?scl:%global pkg_name %{name}}

# For java auto requires/provides generation
%{?scl:%thermostat_find_provides_and_requires}

%global base_name       collections
%global short_name      commons-%{base_name}

Name:           %{?scl_prefix}apache-%{short_name}
Version:        3.2.1
Release:        24%{?dist}
Summary:        Provides new interfaces, implementations and utilities for Java Collections
License:        ASL 2.0
Group:          Development/Libraries
URL:            http://commons.apache.org/%{base_name}/
Source0:        http://www.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz

Patch0:         jakarta-%{short_name}-javadoc-nonet.patch
Patch4:         commons-collections-3.2-build_xml.patch

BuildArch:      noarch

BuildRequires: java-devel
BuildRequires: jpackage-utils
BuildRequires: maven-local
BuildRequires: maven-antrun-plugin
BuildRequires: maven-assembly-plugin
BuildRequires: maven-compiler-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-install-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-doxia-sitetools
BuildRequires: maven-plugin-bundle
BuildRequires: maven-surefire-plugin
BuildRequires: maven-surefire-provider-junit
BuildRequires: ant
BuildRequires: apache-commons-parent >= 26-7

%{?scl:Requires: %scl_runtime}

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
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}

%description testframework
%{summary}.

%package javadoc
Summary:        Javadoc for %{pkg_name}
Group:          Documentation

%description javadoc
%{summary}.

%package testframework-javadoc
Summary:        Javadoc for %{pkg_name}-testframework
Group:          Documentation

%description testframework-javadoc
%{summary}.

%prep
%{?scl:scl enable %{scl} - << "EOF"}
%setup -q -n %{short_name}-%{version}-src
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;

%patch0 -p1
%patch4 -b .sav

# Fix file eof
%{__sed} -i 's/\r//' LICENSE.txt
%{__sed} -i 's/\r//' PROPOSAL.html
%{__sed} -i 's/\r//' RELEASE-NOTES.html
%{__sed} -i 's/\r//' README.txt
%{__sed} -i 's/\r//' NOTICE.txt

%mvn_file : %{pkg_name} %{short_name}
%mvn_alias : "org.apache.commons:%{short_name}"
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - << "EOF"}
%mvn_build

ant tf.javadoc
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - << "EOF"}
%mvn_install

# this JAR doesn't have POM file
install -Dm 644 target/%{short_name}-testframework-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{pkg_name}-testframework.jar
ln -s %{_javadir}/%{pkg_name}-testframework.jar $RPM_BUILD_ROOT%{_javadir}/%{short_name}-testframework.jar

# testframework-javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{pkg_name}-testframework
cp -pr build/docs/testframework/* $RPM_BUILD_ROOT%{_javadocdir}/%{pkg_name}-testframework
%{?scl:EOF}

%files -f .mfiles
%doc PROPOSAL.html README.txt LICENSE.txt RELEASE-NOTES.html NOTICE.txt

%files testframework
%{_javadir}/%{pkg_name}-testframework.jar
%{_javadir}/%{short_name}-testframework.jar

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt

%files testframework-javadoc
%{_javadocdir}/%{pkg_name}-testframework
%doc LICENSE.txt NOTICE.txt

%changelog
* Mon Jan 20 2014 Omair Majid <omajid@redhat.com> - 3.2.1-24
- Rebuild in order to fix osgi()-style provides.
- Resolves: RHBZ#1054813

* Wed Nov 27 2013 Severin Gehwolf <sgehwolf@redhat.com> - 3.2.1-23
- Properly enable SCL

* Fri Nov 15 2013 Severin Gehwolf <sgehwolf@redhat.com> - 3.2.1-22
- Remove unwanted Obsoletes/Provides.
- Add auto requires/provides generation macro.

* Mon Nov 11 2013 Jiri Vanek <jvanek@redhat.com> - 3.2.1-21
- SCL-ize package.

* Fri Sep 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.1-20
- Add BuildRequires on apache-commons-parent >= 26-7

* Mon Aug 26 2013 Michal Srb <msrb@redhat.com> - 3.2.1-19
- Migrate away from mvn-rpmbuild (Resolves: #997509)

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.1-18
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

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

* Tue Aug 30 2010 Carl Green <carlgreen at gmail.com> - 3.2.1-6
- Change package to own files in directories, not the directories

* Mon Aug 30 2010 Carl Green <carlgreen at gmail.com> - 3.2.1-5
- Remove source and patches no longer needed for Maven
- Fix non-standard groups and remove empty sections
- Fix file permissions

* Sat Aug 28 2010 Carl Green <carlgreen at gmail.com> - 3.2.1-4
- Renamed from jakarta-commons-collections
- Updated to use maven2
- Replaced saxon:group instruction with xsl:for-each-group in pom-maven2jpp-newdepmap.xsl
