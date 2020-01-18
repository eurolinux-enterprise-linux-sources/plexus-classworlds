Name:           plexus-classworlds
Version:        2.4.2
Release:        7%{?dist}
Summary:        Plexus Classworlds Classloader Framework
License:        ASL 2.0 and Plexus
URL:            http://plexus.codehaus.org/
BuildArch:      noarch

Source0:        https://github.com/sonatype/%{name}/archive/%{name}-%{version}.tar.gz
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt

BuildRequires:  maven-local
BuildRequires:  plexus-pom
BuildRequires:  maven-dependency-plugin

Obsoletes:      classworlds < %{version}-%{release}
Provides:       classworlds = %{version}-%{release}

%description
Classworlds is a framework for container developers
who require complex manipulation of Java's ClassLoaders.
Java's native ClassLoader mechanisms and classes can cause
much headache and confusion for certain types of
application developers. Projects which involve dynamic
loading of components or otherwise represent a 'container'
can benefit from the classloading control provided by
classworlds.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n %{name}-%{name}-%{version}
%mvn_file  : plexus/classworlds
%mvn_alias : classworlds:classworlds

for j in $(find . -name "*.jar" | grep -v /test-data/ | grep -v /test-jars/); do
  rm $j
done

# fix ant groupId
sed -i 's:<groupId>ant</groupId>:<groupId>org.apache.ant</groupId>:' pom.xml

# Generate OSGI info
%pom_xpath_inject "pom:project" "<packaging>bundle</packaging>"
%pom_xpath_inject "pom:build/pom:plugins" "
        <plugin>
          <groupId>org.apache.felix</groupId>
          <artifactId>maven-bundle-plugin</artifactId>
          <extensions>true</extensions>
          <configuration>
            <instructions>
              <_nouses>true</_nouses>
              <Export-Package>org.codehaus.classworlds.*;org.codehaus.plexus.classworlds.*</Export-Package>
            </instructions>
          </configuration>
        </plugin>"

cp %{SOURCE1} .

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%dir %{_javadir}/plexus
%doc LICENSE.txt LICENSE-2.0.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt LICENSE-2.0.txt

%changelog
* Fri Jul 26 2013 Michal Srb <msrb@redhat.com> - 2.4.2-7
- Fix Provides and Obsoletes

* Fri Jul 12 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.4.2-6
- Build with XMvn
- Update to current packaging guidelines
- Provide and obsolete classworlds

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.4.2-5
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Thu Apr 11 2013 Mat Booth <fedora@matbooth.co.uk> - 2.4.2-4
- Remove superfluous BRs, fixes rhbz #915616

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.4.2-2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Jan 22 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.4.2-1
- Update to latest bugfix release 2.4.2 (#895445)

* Wed Nov 21 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.4-11
- Install required ASL 2.0 license text

* Wed Nov 21 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.4-10
- Revert change from 2.4-9

* Tue Nov 20 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.4-9
- Provide and obsolete classworlds

* Mon Nov 19 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.4-8
- Fix source URL to be stable

* Tue Aug  7 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.4-7
- Export only proper OSGI packages
- Do not generate "uses" OSGI clauses

* Mon Aug 06 2012 Gerard Ryan <galileo@fedoraproject.org> - 2.4-6
- Generate OSGI info using maven-plugin-bundle

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr  5 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.4-4
- Update to maven 3
- Remove rpm bug workaround

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.4-1
- Update to latest upstream version
- Drop ant build parts
- Versionless jars & javadocs
- Enable tests again

* Tue Dec 21 2010 Alexander Kurtakov <akurtako@redhat.com> 2.2.3-2
- Fix FTBFS.

* Tue Jul 13 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.3-1
- Version bump
- Fix few small packaging guidelines violations

* Thu Aug 20 2009 Andrew Overholt <overholt@redhat.com> 0:1.2-0.a9.8
- Bump release.

* Wed Aug 19 2009 Andrew Overholt <overholt@redhat.com> 0:1.2-0.a9.7
- Document sources and patches

* Wed Aug 19 2009 Andrew Overholt <overholt@redhat.com> 0:1.2-0.a9.6
- Update tarball-building instructions
- Remove gcj support
- Remove unnecessary post requirements

* Thu May 14 2009 Fernando Nasser <fnasser@redhat.com> 0:1.2-0.a9.6
- Fix license specification

* Tue Apr 28 2009 Yong Yang <yyang@redhat.com> 0:1.2-0.a9.5
- Add BRs maven2-plugin-surfire*, maven-doxia*
- Rebuild with maven2-2.0.8 built in non-bootstrap mode

* Mon Mar 16 2009 Yong Yang <yyang@redhat.com> 0:1.2-0.a9.4
- rebuild with new maven2 2.0.8 built in bootstrap mode

* Tue Jan 13 2009 Yong Yang <yyang@redhat.com> 0:1.2-0.a9.3jpp.1
- re-build with maven

* Tue Jan 06 2009 Yong Yang <yyang@redhat.com> 0:1.2-0.a9.2jpp.1
- Imported into devel from dbhole's maven 2.0.8 packages

* Wed Jan 30 2008 Deepak Bhole <dbhole@redhat.com> 0:1.2-0.a9.1jpp.1
- Initial build -- merged from JPackage
