Version: 2.11
%define release 1
# get rpm version
%define rpm_ver %( rpm -q --queryformat='%{VERSION}' rpm | cut -f 1 -d.)
# test for an rpm version
%define test_ver() %(if test %1 == %2; then echo 1; else echo 0;fi )
# define binary flags
%define is_rpm3 %test_ver %rpm_ver 3

# The Summary: line should be expanded to about here -----^
Summary: A tool to build rpm file from rpm database
Summary(fr): Un outil pour construire un package depuis une base rpm
Name: rpmrebuild
License: GPL
Group: Development/Tools
BuildRoot: %{_topdir}/installroots/%{name}-%{version}-%{release}
Source: rpmrebuild-%{version}.tar.gz
# Following are optional fields
Url: http://rpmrebuild.sourceforge.net
Packager: Eric Gerbier <gerbier@users.sourceforge.net>
#Distribution: 
BuildArchitectures: noarch
Requires: bash
Requires: cpio
Requires: sed

%if %is_rpm3
# rpm v3
Requires: rpm < 4.0
Requires: fileutils
Requires: textutils
%define release_suffix %{release}rpm3

%else
# rpm v4 v5
Requires: /usr/bin/rpmbuild
Requires: coreutils
%define release_suffix  %{release} 
%endif

Release: %{release_suffix}

# compatibility with old digest format
%global _binary_filedigest_algorithm 1
%global _source_filedigest_algorithm 1

%description
rpmrebuild allow to build an rpm file from an installed rpm, or from
another rpm file, with or without changes (batch or interactive).
It can be extended by a plugin system.
A typical use is to easy repackage a software after some configuration's
change.

%description -l fr
rpmbuild permet de fabriquer un package rpm à partir d'un 
package installé ou d'un fichier rpm, avec ou sans modifications 
(interactives ou batch).
Un système de plugin permet d'étendre ses fonctionnalités.
Une utilisation typique est la fabrication d'un package suite à des modifications
de configuration.

%prep
%setup -c rpmrebuild

%build
make

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf "$RPM_BUILD_ROOT"
make DESTDIR="$RPM_BUILD_ROOT" install

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf "$RPM_BUILD_ROOT"

%files -f rpmrebuild.files

%changelog
* Wed Nov 22 2013 <gerbier@users.sourceforge.net> 2.11
- add install option

* Sun Aug 11 2013 <gerbier@users.sourceforge.net> 2.10-2
- bugfix from 2.10 on test install : test was inverted (applied on rpm files instead installed rpm)

* Tue Aug 01 2013 <valery_reznic@users.sourceforge.net> 2.10
- add tag DISTTAG (feature request)
- do not test install if work on rpm files
- applied patch from Olivier Bourdon for pretrans and postrans

* Sun Jan 13 2013 <valery_reznic@users.sourceforge.net> 2.9
- fix to work with rpm 4.10 (Fedora 18) - error: incorrect format: invalid field width

* Thu Jul 11 2012 <gerbier@users.sourceforge.net> 2.8
- can handle SUGGESTS/ENHANCES rpm tag
- add --cap-from-fs/cap-from-db options
- build rpmrebuild-version.tar.gz to allow rpmbuild -tb work

* Thu Jun 06 2012 <gerbier@users.sourceforge.net> 2.7
- patch from Andreas Kainz for package file checking
- add new unset_tag plugin
- add support for rpm version 5 (mandriva)
- fix -l / --list-plugin option
- add support of posix capability
- add new un_prelink plugin (suggest from Han Holl)
- add RPMREBUILD_OPTS environment variable
- fix problem with different architecture (build 32bit on 64bits)
- fix bad arch on gpg-pubkey packages

* Tue Jul 12 2011 <gerbier@users.sourceforge.net> 2.6
- fix bug when working on source packages, ghost files

* Fri Apr 15 2011 <gerbier@users.sourceforge.net> 2.5
- add -5/-l options in man pages
- Added support for obsolete version and flags (bugfix by Valery Reznic)
- shell compatibility (mkdir) for AIX : use -p option instead --parents
- new Mkdir_p function to check for mkdir result
- apply patch from ndyankov : support for broken symlinks
- specfile will allow build package for rpm version 4 or 3

* Fri Dec 11 2009 <gerbier@users.sourceforge.net> 2.4
- add -l / --list-plugin option

* Tue Nov 12 2009 <valery_reznic@users.sourceforge.net>
- add -5 / --md5-compat-digest option

* Wed Jan 09 2009 <gerbier@users.sourceforge.net> 2.3
- release version 2.3

* Tue Dec 16 2008 <valery_reznic@users.sourceforge.net>
- fix a problem: installation test failed when repackaged rpm file (with -p)

* Tue Dec 16 2008 <valery_reznic@users.sourceforge.net>
- fix for rpm 4.6 (fedora 10), that ignore BuildRoot in the spec file flag

* Wed Dec 05 2008 <gerbier@users.sourceforge.net> 
- do not use popt any more

* Wed Aug 06 2008 <gerbier@users.sourceforge.net> 2.2.3-1
- fix a problem with new rpm security on mandriva (defaultbuildroot)

* Mon Apr 28 2008 <gerbier@users.sourceforge.net> 2.2.2-1
- fix a bug when working on package file with path

* Wed Apr 2 2008 <gerbier@users.sourceforge.net> 2.2.1-1
- fix bug on uid/gid with --pug-from-fs option
- demo plugin : better error message
- do not remove /etc/popt : it does not belong our package
- add new set_tag plugin
- new demofiles plugin
- add utf-8 for french localisation

* Mon Oct 22 2007 <gerbier@users.sourceforge.net> 2.2.0-1
- add translation system (english and french) with new locale and man directory
- fix a bug with rpm localisation in PackageInstalled function ( rpm message are localized, so the grep filter does not work everywhere )
- fix bug : include file are also search in plugin directory
- fix help : do not show path any more (fedora bug 328641)
- add tests for --package option (if file exists, if it is an rpm)
- move package to Development/Tools group
- remove all calls to grep
- replace code in remove_from_popt.make.include by sed call (cf fedora specfile)
- update specfile description tag

* Mon Jun 18 2007 <gerbier@users.sourceforge.net> 2.1.1-1
- remove commented tags (PAYLOAD*, INSTALLTID, OPTFLAGS, PLATFORM, SIGSIZE) to solve bug for rpm 3.x
- add more info to bugreport (issues, warnings)
- add choice of email addresse for bug report
- send bug report to new rpmrebuild-bugreport list

* Tue May 15 2007 <gerbier@users.sourceforge.net> 2.1.0-1
- remove old deprecated tags ICON and SERIAL
- comment missing localisation file (lang)
- remove commnented tag XPM and GIF
- allow concurrent use : random working directory
- add new long option --debug
- check if rpm tags exists (CheckTags)
- add code to send bug report by mail (SendBugReport)

* Tue May 31 2005 <gerbier@users.sourceforge.net> 2.0.4-1
- force tmpdir to be empty (Christopher Faylor)
- fix bug with testinstall return
- fix bug with short options -r -n
- improved nodoc plugin

* Fri May 20 2005 <gerbier@users.sourceforge.net> 2.0.3-1
- add --notest-install option (Christopher Faylor)
- add --release option (Christopher Faylor)
- add nodoc plugin

* Wed Mar  2 2005 <gerbier@users.sourceforge.net> 2.0.2-1
- fix bug with BuildArch tag (rpmrebuild_popt)

* Tue Mar  1 2005 <valery_reznic@users.sourceforge.net> 2.0.2-1
- Change from /usr/local/bin to /usr/bin from /usr/local/man to /usr/share/man
- plugins moved to the plugins/ directory in the source tree
- plugins manpages renamed to the .in 

* Tue Feb 22 2005 <valery_reznic@users.sourceforge.net> 2.0.1-1
- fix for rpm-4.3.[12]

* Wed Dec 29 2004 <gerbier@users.sourceforge.net> 2.0.0-1
- add demo, uniq, file2pacDep plugins (exemples)
- add commented tags (PAYLOAD*, PATCH, SIZE, INSTALLTID, OPTFLAGS, PLATFORM, ARCHIVESIZE,SIGSIZE, SERIAL)

* Sun Nov 14 2004 <valery_reznic@users.sourceforge.net> 2.0.0-1
- rpmrebuild_parser.src - added '--help-plugins' option

* Wed Oct 26 2004 <valery_reznic@users.sourceforge.net> 2.0.0-1
- processing of /change/modify/edit was moved to the processng_func.src
- changes to support --change-spec-* ane --edit-* (in the processing_func, rpmrebuild_popt and rpmrebuild_parser)
- added '--include' option

* Wed Sep 28 2004 <valery_reznic@users.sourceforge.net> 2.0.0-1
- changed all env variables' names to be prefixed with RPMREBUILD_

* Tue Sep 27 2004 <valery_reznic@users.sourceforge.net> 2.0.0-1
- change different variables values from empty/non-empty to yes/no

* Tue Sep 20 2004 <valery_reznic@users.sourceforge.net> 2.0.0-1
- Added support for arbitrary execution order for change/edit/modify

* Sun Sep 19 2004 <valery_reznic@users.sourceforge.net> 2.0.0-1
- CommandLineParsing functionality moved to the new file rpmrebuild_parser.src

* Mon Aug 16 2004 <gerbier@users.sourceforge.net> 1.4.7-3
- change dependency from rpm-build package to rpmbuild file for suses distrib
- some fixes from rmlint

* Wed Aug 11 2004 <valery_reznic@users.sourceforge.net> 1.4.7-3
- fixed problem with repackaging rpm with ghost files

* Sun Jul 25 2004 <valery_reznic@users.sourceforge.net> 1.4.7-2
- fixed problem with manpages compression

* Mon Jul 12 2004 <valery_reznic@users.sourceforge.net> 1.4.7-1
- rpmrebuild.sh can be now run from local directory, without need to install package (add rpmrebuild_buildroot.sh file).

* Sun Jul 11 2004 <valery_reznic@users.sourceforge.net> 1.4.7-1
- Fix a bug: --comment-missing=yes was work only when --verify=no 
- --modify now work without --package too.
- fix a bug on sed for redhat 7.2 (rewrite SpecChange)
- change SpecFile to generate rpm according autorequire/autoprovide (avoid post sed)
- add rpmrebuild file (avoid symbolic link)

* Mon May 24 2004 <gerbier@users.sourceforge.net> 1.4.6-4
- fix a bug on --autoprovide/--autorequire

* Mon May 24 2004 <valery_reznic@users.sourceforge.net> 1.4.6-4
- eliminate 'expr' usage
- add RPMREBUILD_TMDDIR environment variable.  With default ~/.tmp/rpmrebuild It used instead of /tmp.

* Sun May 23 2004 <valery_reznic@users.sourceforge.net> 1.4.6-4
- fixed bug with parsing --long-option= 
- buildroot was changed not to use /tmp dir

* Wed May 19 2004 <valery_reznic@users.sourceforge.net> 1.4.6-3
- added long option abbreviation
- dir option changed to directory
- add all remaining dependencies (bash, sed, grep ...) to package

* Thu May 6 2004 <gerbier@users.sourceforge.net> 1.4.6-2
- split in 2 packages for rpm <4 and rpm >4 (add rpm-build dependency) 

* Mon Nov 24 2003 <gerbier@users.sourceforge.net> 1.4.6-1
- added -P/--autoprovide flag
- added -R/--autorequire flag

* Wed Nov 19 2003 <gerbier@users.sourceforge.net> 1.4.5-2
- change filter behavior to be more robust
- read -r on /etc/popt to keep backslash
- fix comment-missing option
- remove rpmlib dependencies from specfile
- remove gpg key from provide list
- fix wildcard problem in file list (guile) (Han Holl)

* Wed Jul  2 2003 <valery_reznic@users.sourceforge.net> 1.4.5-1
- switch from 'case' to usinf AskYesNo function
- added -y/--verify flag
- added -c/--comment-missing flag
- added missing -w/--warning to the Usage message

* Thu Jun 12 2003 <valery_reznic@users.sourceforge.net> 1.4.4-1
- added -m/--modify option - invoke script after rpm's file unpackaging
- added -a/--additional option - pass additional flags to rpmbuild
- added -D/--define option - set defines for rpmbuild
- after specfile editing (with -e option) is possible now abort rpm build 

* Mon Jun 09 2003 <valery_reznic@users.sourceforge.net> 1.4.3-1
- fixed problem with (none) in the FILELANG query
- rpmrebuild now working with rpm-4.2
- Makefile now can work with both  rpmbuild and rpm as package builder

* Mon Jun 02 2003 <valery_reznic@users.sourceforge.net> 1.4.2-1
- fixed problem with specspo (now I query package and not specspo information)

* Mon Feb 03 2003 <gerbier@users.sourceforge.net> 1.4.1-1
- add warning flag (-w/--warning) 

* Fri Jan 17 2003 <gerbier@users.sourceforge.net> 1.4.0-1
- public release of 1.3 dev branch

* Mon Dec 29 2002 <valery_reznic@users.sourceforge.net> 1.3-1
- add '-p' option. Now is possible rebuild not only installed rpm, but rpm file too. May be usefull with '-e' or '--filter' option

* Mon Dec 18 2002 <valery_reznic@users.sourceforge.net> 1.3-1
- more simple and robust filter

* Thu Dec 12 2002 <gerbier@users.sourceforge.net> 1.3.1
- add filter option for "pluggins"
- rewrite --resolv-dep as pluggin

* Mon Dec 10 2002 <valery_reznic@users.sourceforge.net> 1.3-0
- change long options name to be more consistant
- added support for %%lang

* Mon Dec 10 2002 <gerbier@users.sourceforge.net> 1.3.0
- add man page
- fix bug with % in changelog
- add -r|--resolv-dep option
- add french translation in specfile

* Sat Dec  3 2002 <valery_reznic@users.sourceforge.net> 1.3.0
- added long options

* Sat Dec  2 2002 <valery_reznic@users.sourceforge.net> 1.2-0
- now rpmrebuild can be run as 'rpm --rpmrebuild'

* Sat Nov 24 2002 <valery_reznic@users.sourceforge.net> 1.1-1
- filter "(none)" answer from rpm the scripts queries

* Sat Nov 23 2002 <gerbier@users.sourceforge.net> 1.1-0
- filter "(none)" answer from rpm queries

* Thu Oct 22 2002 <gerbier@users.sourceforge.net> 1.0-0
- replace vi by %%define
- add command lines options (-h : help, -v : verbose, -V: version)
- add lsm description
- move .popt to /usr/lib/rpmrebuild
- fix some .popt problems with rpm 4.1 (Han Holl)
- have a link from rpmrebuild.sh to rpmrebuild
- add option -b for batch processing
- add option -k to keep installed files perm
- fix a buggy test for non-installed packages (Han Holl)
- remove dirname and move code to /usr/lib/rpmrebuild
- use rpmbuild  if it exists (rpm 4.1)  (Han Holl)
- add -d option to change local dir
- add -e  option to edit spec file (Han Holl)
- add generation verify directive to the spec file
- add build testing and install testing
- fix a bug if release change
- specfile now temporary (Valery Reznic)
- added -s flag to generate spec file only (Valery Reznic)
- default dir for rpm now not current dir but naitive rpm dir (Valery Reznic)
- fix a bug for redhat 6.2 package name
- fix a bug for package providing

* Mon Oct  7 2002  <valery_reznic@users.sourceforge.net> 0.7.1
- split the script for a more modular way
- recode %file with all new tags (missingok, noreplace...)
- Valery Reznic join the project

* Mon Sep 30 2002  <gerbier@users.sourceforge.net> 0.7.0
- work on local dir (thanks Valery Reznic <valery_reznic@users.sourceforge.net>)

* Mon Sep 23 2002  <gerbier@users.sourceforge.net> 0.6.0
- add triggers (thanks to Han Holl <han.holl@prismant.nl>
- add many other spec tags (icon, exlude*, serial, provides, conflicts ...)

* Sun Sep 20 2002  <gerbier@users.sourceforge.net> 0.5.0
- try to have it work on any distribution
- the rpm package is now signed with my gpg key

* Mon Sep 17 2002  <gerbier@users.sourceforge.net> 0.4.2
- add architecture support (thanks to Han Holl <han.holl@prismant.nl>)
- add add require, obsolete tags
- force time format with LC_TIME to POSIX
- change shell name to match project name
- full english messages

* Mon Sep 17 2002  <gerbier@users.sourceforge.net> 0.4.1
- suppress useless exit
- shell cosmetic changes

* Sun Jul 14 2002  <gerbier@users.sourceforge.net>
- Initial spec file created by autospec ver. 0.6 with rpm 2.5 compatibility
- check changes (rpm -V)
- check for multiples rpm
- simplify pre post tag
- add type doc and config files
