
%define	jcr_version 0.1.2

Summary:	Conference module for Jabber
Summary(pl.UTF-8):   Moduł konferencyjny systemu Jabber
Name:		jabber-mu-conference
Version:	0.6.0
Release:	4
License:	distributable
Group:		Applications/Communications
Source0:	http://www.jabberstudio.org/files/mu-conference/mu-conference-%{version}.tar.gz
# Source0-md5:	e97433bf4a978329d639ce872bee3223
Source1:	http://jabber.terrapin.com/JCR/jcr-%{jcr_version}.tar.gz
# Source1-md5:	622a1bf538d5adc92a516c7ef4bfbf57
Source2:	jabber-muc.init
Source3:	jabber-muc.sysconfig
Patch0:		%{name}-Makefiles.patch
Patch1:		%{name}-config.patch
Patch2:		%{name}-drop_priv.patch
URL:		http://mu-conference.jabberstudio.org/
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
%setup -qn mu-conference-%{version} -a 1
mv jcr-%{jcr_version} jcr
%patch0 -p1
%patch1 -p1
%patch2 -p1
cp jcr/src/{main.c,jcomp.mk} src

%build
%{__make} -C jcr \
	CC="%{__cc}" \
	OFLAGS="%{rpmcflags}"

%{__make} -C src -f jcomp.mk \
	CC="%{__cc}" \
	OFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/jabber \
	$RPM_BUILD_ROOT{%{_sbindir},/etc/{rc.d/init.d,sysconfig}} \
	$RPM_BUILD_ROOT{/var/log/%{name}/chats,/var/lib/%{name}}

install src/mu-conference $RPM_BUILD_ROOT%{_sbindir}/jabber-muc
install muc-jcr.xml $RPM_BUILD_ROOT%{_sysconfdir}/jabber/mu-conference.xml
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/jabber-muc
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/jabber-muc

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
%doc AUTHORS ChangeLog FAQ README TODO *.xml
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,jabber) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/jabber/*
%attr(754,root,root) /etc/rc.d/init.d/jabber-muc
%dir %attr(771,root,jabber) /var/lib/jabber-mu-conference/
%dir %attr(775,root,jabber) /var/log/jabber-mu-conference/
%dir %attr(775,root,jabber) /var/log/jabber-mu-conference/chats
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/jabber-muc
