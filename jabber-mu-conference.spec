Summary:	Conference module for Jabber
Summary(pl):	Modu³ konferencyjny systemu Jabber
Name:		jabber-mu-conference
Version:	0.5.2
Release:	1
License:	distributable
Group:		Applications/Communications
Source0:	http://www.jabberstudio.org/files/mu-conference/mu-conference-%{version}.tar.gz
# Source0-md5:	c8167e4209278c22e96da20355e8cf49
Source1:	mu-conference.xml
Source2:	jabber-muc.init
Source3:	jabber-muc.sysconfig
Patch0:		%{name}-Makefile.patch
URL:		http://mu-conference.jabberstudio.org/
BuildRequires:	jabberd14-devel
%requires_eq	jabberd14
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the new multi-user conferencing service for the Jabber server. This is
the reference implementation of MUC protocol (JEP-0045).

%description -l pl
To jest nowy modu³ konferencji/grupowych czatów dla serwera Jabber. To jest
bazowa implementacja protoko³u MUC (JEP-0045).

%prep
%setup -qn mu-conference-%{version}
%patch0 -p1

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/jabberd14,%{_sysconfdir}/jabber} \
	$RPM_BUILD_ROOT{%{_sbindir},/etc/{rc.d/init.d,sysconfig}}

install src/mu-conference.so $RPM_BUILD_ROOT%{_libdir}/jabberd14
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/jabber
ln -s %{_sbindir}/jabberd14 $RPM_BUILD_ROOT%{_sbindir}/jabber-muc
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/jabber-muc
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/jabber-muc

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/jabber/secret ] ; then
	SECRET=`cat /etc/jabber/secret`
	if [ -n "$SECRET" ] ; then
        	echo "Updating component authentication secret in the config file..."
		perl -pi -e "s/>secret</>$SECRET</" /etc/jabber/mu-conference.xml
	fi
fi

/sbin/chkconfig --add jabber-muc
if [ -r /var/lock/subsys/jabber-muc ]; then
	/etc/rc.d/init.d/jabber-muc restart >&2
else
	echo "Run \"/etc/rc.d/init.d/jabber-muc start\" to start Jabber mu-conference service."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -r /var/lock/subsys/jabber-muc ]; then
		/etc/rc.d/init.d/jabber-muc stop >&2
	fi
	/sbin/chkconfig --del jabber-muc
fi

%files
%defattr(644,root,root,755)
%doc README FAQ ChangeLog TODO *.xml
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/jabberd14/*
%attr(640,root,jabber) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/jabber/*
%attr(754,root,root) /etc/rc.d/init.d/jabber-muc
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/jabber-muc
