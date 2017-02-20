%define __server_dir   /opt/NewsGate
%define __work_dir    /u01/NewsGate/var

Name:    newsgate-config-##TYPE##
Version: 1.4.0.0
Release: ssv1%{?dist}
Summary: Newsgate server configuration for ##TYPE##
License: LGPL
Group: System Environment/Daemons
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-buildroot
Source0: %name-%version.tar.gz
BuildRequires: make OpenSBE 
Requires: newsgate = %version net-snmp-subagent-shell >=  2.1.2.0 syslog-ng
##ABT_ANCHOR1##

%description 
Newsgate server configuration for ##TYPE## 

%prep
%setup -n %name-%version/Template

%build
cp -a ../##TYPE##/* ./
osbe
./configure --enable-no-questions
%__make

%install
%__rm -rf %buildroot
make install destdir=%buildroot prefix=/ proddir=%__server_dir 
find %buildroot%__server_dir/etc -name '*.sh' -exec chmod 755 '{}' ';'
find %buildroot%__server_dir/etc/NewsGate/cert -type f |  sed -e "s#%{buildroot}##g" > cert.files
mkdir -p %buildroot%__work_dir
pushd %buildroot%__server_dir
%__ln_s %__work_dir/ ./
popd

%files -f cert.files
%defattr(-, root, newsgate)
%__server_dir/etc/*.sh
%__server_dir/etc/NewsGate/*.sh
%__server_dir/etc/NewsGate/*.cnf
%__server_dir/etc/NewsGate/*.xml
%dir %__server_dir/etc/NewsGate/Frontend
%__server_dir/etc/NewsGate/Frontend/*
%dir %__server_dir/etc/NewsGate/tests
%__server_dir/etc/NewsGate/tests/*
%dir %__server_dir/etc/NewsGate/SearchMailer/
%__server_dir/etc/NewsGate/SearchMailer/*
%__server_dir/etc/NewsGate/www*
/etc/cron.d/*
/etc/snmp/subagent-shell/*
/etc/security/limits.d/*
/etc/syslog-ng/conf.d/*
%defattr(-, newsgate, newsgate)
%dir %__work_dir
%__server_dir/var

%post
/sbin/service subagent-shell restart

%clean
%__rm -rf %{buildroot}

%changelog
