Summary:	Conference module for Jabber
Summary(pl):	Modu³ konferencyjny systemu Jabber
Name:		jabber-mu-conference
Version:	0.3
Release:	1
License:	distributable
Group:		Applications/Communications
Source0:	http://download.jabber.org/dists/1.4/final/muconference-%{version}.tar.gz
Source1:	mu-conference.xml
Patch0:		%{name}-Makefile.patch
URL:		http://www.jabber.org/
BuildRequires:	jabber-devel
%requires_eq  	jabber
Requires:	jabber >= 1.4.2-4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the conferencing/groupchat service for the Jabber server.

%description -l pl
To jest modu³ konferencji/grupowych czatów dla serwera Jabber.

%prep
%setup -qn mu-conference
%patch0 -p1

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/jabberd,%{_sysconfdir}/jabberd,/var/log/jabber/muc}

install src/mu-conference.so $RPM_BUILD_ROOT%{_libdir}/jabberd
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/jabberd

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -r /var/lock/subsys/jabberd ]; then
	if [ -r /var/lock/subsys/jabber/mu-conference ]; then
        	/etc/rc.d/init.d/jabberd restart mu-conference >&2
	else
        	echo "Run \"/etc/rc.d/init.d/jabberd start mu-conference\" to start Jabber mu-conference service."
	fi
else
        echo "Run \"/etc/rc.d/init.d/jabberd start\" to start Jabber server."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -r /var/lock/subsys/jabber/mu-conference ]; then
		/etc/rc.d/init.d/jabberd stop mu-conference >&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc README FAQ ChangeLog TODO *.xml
%attr(755,root,root) %{_libdir}/jabberd/*
%attr(640,root,jabber) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/jabberd/*
%dir %attr(775,root,jabber) /var/log/jabber/muc
