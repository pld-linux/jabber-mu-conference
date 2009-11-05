Summary:	Conference module for Jabber
Summary(pl.UTF-8):	Moduł konferencyjny systemu Jabber
Name:		jabber-mu-conference
Version:	0.8
Release:	1
License:	distributable
Group:		Applications/Communications
Source0:	http://download.gna.org/mu-conference/mu-conference_%{version}.tar.gz
# Source0-md5:	3e11ae52499a65a577d4c697194fc1ce
Source1:	jabber-muc.init
Source2:	jabber-muc.sysconfig
Patch0:		%{name}-Makefiles.patch
Patch1:		%{name}-config.patch
Patch2:		%{name}-drop_priv.patch
URL:		https://gna.org/projects/mu-conference/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post):	sed >= 4.0
Requires(post):	textutils
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the new multi-user conferencing service for the Jabber server.
This is the reference implementation of MUC protocol (JEP-0045).

%description -l pl.UTF-8
To jest nowy moduł konferencji/grupowych czatów dla serwera Jabber. To
jest wzorcowa implementacja protokołu MUC (JEP-0045).

%prep
%setup -qn mu-conference_%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__make} -C src \
	CC="%{__cc}" \
	OFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/jabber \
	$RPM_BUILD_ROOT{%{_sbindir},/etc/{rc.d/init.d,sysconfig}} \
	$RPM_BUILD_ROOT{/var/log/%{name}/chats,/var/lib/%{name}}

install src/mu-conference $RPM_BUILD_ROOT%{_sbindir}/jabber-muc
install muc-default.xml $RPM_BUILD_ROOT%{_sysconfdir}/jabber/mu-conference.xml
install style.css $RPM_BUILD_ROOT%{_sysconfdir}/jabber/mu-conference-style.css
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/jabber-muc
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/jabber-muc

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f %{_sysconfdir}/jabber/secret ] ; then
	SECRET=`cat %{_sysconfdir}/jabber/secret`
	if [ -n "$SECRET" ] ; then
		echo "Updating component authentication secret in the config file..."
		%{__sed} -i -e "s/>secret</>$SECRET</" %{_sysconfdir}/jabber/mu-conference.xml
	fi
fi

/sbin/chkconfig --add jabber-muc
%service jabber-muc restart "Jabber mu-conference service"

%preun
if [ "$1" = "0" ]; then
	%service jabber-muc stop
	/sbin/chkconfig --del jabber-muc
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog FAQ README TODO *.xml *.sql
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,jabber) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/jabber/*
%attr(754,root,root) /etc/rc.d/init.d/jabber-muc
%dir %attr(771,root,jabber) /var/lib/jabber-mu-conference/
%dir %attr(775,root,jabber) /var/log/jabber-mu-conference/
%dir %attr(775,root,jabber) /var/log/jabber-mu-conference/chats
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/jabber-muc
