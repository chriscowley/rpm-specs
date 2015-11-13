Name:           powerline
Version:        2.2
Release:        2%{?dist}

Summary:        The ultimate status-line/prompt utility
License:        MIT
Group:          Applications/System
Url:            https://github.com/powerline/powerline

BuildRequires:  python-setuptools
BuildRequires:  python-sphinx
BuildRequires:  fdupes
BuildRequires:  fontconfig
BuildRequires:  tmux
BuildRequires:  vim-minimal

Requires:       python
Requires:       fontconfig

Source0:        https://github.com/powerline/powerline/archive/%{version}.tar.gz
Source1:        vim-powerline.metainfo.xml

%description
Powerline is a status-line plugin for vim, and provides status-lines and prompts
for several other applications, including zsh, bash, tmux, IPython, Awesome and
Qtile.

%package docs
Summary: Powerline Documentation
Group: Documentation

%description docs
This package provides the powerline documentation.

%package -n vim-powerline
Summary: Powerline VIM plugin
Group: Application/Editors
BuildArch: noarch
Requires: vim
Requires: %{name} = %{version}-%{release}
Obsoletes: vim-plugin-powerline
Provides: vim-plugin-powerline

%description -n vim-powerline
Powerline is a status-line plugin for vim, and provides status-lines and
prompts.

%package -n tmux-powerline
Summary: Powerline for tmux
Group: Applications/System
BuildArch: noarch
Requires: tmux
Requires: %{name} = %{version}-%{release}

%description -n tmux-powerline
Powerline for tmux.

Add

    source /usr/share/tmux/powerline.conf

to your ~/.tmux.conf file.

%prep
%setup -q

%build
# nothing to build

%install
sed -i -e "/DEFAULT_SYSTEM_CONFIG_DIR/ s@None@'%{_sysconfdir}/xdg'@" powerline/config.py
sed -i -e "/TMUX_CONFIG_DIRECTORY/ s@BINDINGS_DIRECTORY@'/usr/share'@" powerline/config.py
CFLAGS="%{optflags}" \
python setup.py install --prefix=%{_prefix} --root=%{buildroot} --optimize=1

# build docs
pushd docs
#%__make html SPHINXBUILD=/usr/bin/sphinx-build PAPER=a4
#%__rm _build/html/.buildinfo
# A structure gets initialized while building the docs with os.environ.
# This works around an rpmlint error with the build dir being in a file.
#sed -i -e 's/abuild/user/g' _build/html/develop/extensions.html

#%__make man SPHINXBUILD=/usr/bin/sphinx-build
popd

# config
install -d -m0755 %{buildroot}%{_sysconfdir}/xdg/%{name}
cp -a powerline/config_files/* %{buildroot}%{_sysconfdir}/xdg/%{name}/

# fonts
install -d -m0755 %{buildroot}%{_sysconfdir}/fonts/conf.d
install -d -m0755 %{buildroot}%{_datadir}/fonts/truetype
install -d -m0755 %{buildroot}%{_datadir}/fontconfig/conf.avail

install -m0644 font/PowerlineSymbols.otf %{buildroot}%{_datadir}/fonts/truetype/PowerlineSymbols.otf
install -m0644 font/10-powerline-symbols.conf %{buildroot}%{_datadir}/fontconfig/conf.avail/10-powerline-symbols.conf

ln -s %{_datadir}/fontconfig/conf.avail/10-powerline-symbols.conf %{buildroot}%{_sysconfdir}/fonts/conf.d/10-powerline-symbols.conf

# manpages
#%__install -d -m0755 %{buildroot}%{_datadir}/man/man1
#for f in powerline-config.1 powerline-daemon.1 powerline-lint.1 powerline.1; do
#%__install -m0644 docs/_build/man/$f %{buildroot}%{_datadir}/man/man1/$f
#done

# awesome
install -d -m0755 %{buildroot}%{_datadir}/%{name}/awesome/
mv %{buildroot}%{python_sitelib}/powerline/bindings/awesome/powerline.lua %{buildroot}%{_datadir}/%{name}/awesome/
mv %{buildroot}%{python_sitelib}/powerline/bindings/awesome/powerline-awesome.py %{buildroot}%{_datadir}/%{name}/awesome/

# bash bindings
install -d -m0755 %{buildroot}%{_datadir}/%{name}/bash
mv %{buildroot}%{python_sitelib}/powerline/bindings/bash/powerline.sh %{buildroot}%{_datadir}/%{name}/bash/

# fish
install -d -m0755 %{buildroot}%{_datadir}/%{name}/fish
mv %{buildroot}%{python_sitelib}/powerline/bindings/fish/powerline-setup.fish %{buildroot}%{_datadir}/%{name}/fish

# i3
install -d -m0755 %{buildroot}%{_datadir}/%{name}/i3
mv %{buildroot}%{python_sitelib}/powerline/bindings/i3/powerline-i3.py %{buildroot}%{_datadir}/%{name}/i3

# ipython
install -d -m0755 %{buildroot}%{_datadir}/%{name}/ipython
mv %{buildroot}%{python_sitelib}/powerline/bindings/ipython/post_0_11.py %{buildroot}%{_datadir}/%{name}/ipython
mv %{buildroot}%{python_sitelib}/powerline/bindings/ipython/pre_0_11.py %{buildroot}%{_datadir}/%{name}/ipython

# qtile
install -d -m0755 %{buildroot}%{_datadir}/%{name}/qtile
mv %{buildroot}%{python_sitelib}/powerline/bindings/qtile/widget.py %{buildroot}%{_datadir}/%{name}/qtile

# shell bindings
install -d -m0755 %{buildroot}%{_datadir}/%{name}/shell
mv %{buildroot}%{python_sitelib}/powerline/bindings/shell/powerline.sh %{buildroot}%{_datadir}/%{name}/shell/

# tcsh
install -d -m0755 %{buildroot}%{_datadir}/%{name}/tcsh
mv %{buildroot}%{python_sitelib}/powerline/bindings/tcsh/powerline.tcsh %{buildroot}%{_datadir}/%{name}/tcsh

# tmux plugin
install -d -m0755 %{buildroot}%{_datadir}/tmux
mv %{buildroot}%{python_sitelib}/powerline/bindings/tmux/powerline*.conf %{buildroot}%{_datadir}/tmux/

# vim plugin
install -d -m0755 %{buildroot}%{_datadir}/vim/vimfiles/plugin/
mv %{buildroot}%{python_sitelib}/powerline/bindings/vim/plugin/powerline.vim %{buildroot}%{_datadir}/vim/vimfiles/plugin/powerline.vim
rm -rf %{buildroot}%{python_sitelib}/powerline/bindings/vim/plugin
install -d -m0755 %{buildroot}%{_datadir}/vim/vimfiles/autoload/powerline
mv %{buildroot}%{python_sitelib}/powerline/bindings/vim/autoload/powerline/debug.vim %{buildroot}%{_datadir}/vim/vimfiles/autoload/powerline/debug.vim
rm -rf %{buildroot}%{python_sitelib}/powerline/bindings/vim/autoload

# zsh
install -d -m0755 %{buildroot}%{_datadir}/%{name}/zsh
mv %{buildroot}%{python_sitelib}/powerline/bindings/zsh/__init__.py %{buildroot}%{_datadir}/%{name}/zsh
mv %{buildroot}%{python_sitelib}/powerline/bindings/zsh/powerline.zsh %{buildroot}%{_datadir}/%{name}/zsh

# vim-powerline appdata
mkdir -p %{buildroot}%{_datadir}/appdata
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/appdata

# cleanup
%__rm -rf %{buildroot}%{python_sitelib}/%{name}/config_files

%if 0%{?fedora}
%fdupes %{buildroot}%{python_sitelib}
%endif

%files
%doc LICENSE README.rst
%{_sysconfdir}/fonts/conf.d/10-powerline-symbols.conf
%config(noreplace) %{_sysconfdir}/xdg/%{name}
%{_bindir}/powerline
%{_bindir}/powerline-config
%{_bindir}/powerline-daemon
%{_bindir}/powerline-render
%{_bindir}/powerline-lint
%{_datadir}/fontconfig/conf.avail/10-powerline-symbols.conf
%dir %{_datadir}/fonts/truetype
%{_datadir}/fonts/truetype/PowerlineSymbols.otf
# %{_mandir}/man1/powerline.1*
# %{_mandir}/man1/powerline-config.1*
# %{_mandir}/man1/powerline-daemon.1*
# %{_mandir}/man1/powerline-lint.1*
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/awesome
%{_datadir}/%{name}/awesome/powerline.lua
%{_datadir}/%{name}/awesome/powerline-awesome.py*
%dir %{_datadir}/%{name}/bash
%{_datadir}/%{name}/bash/powerline.sh
%dir %{_datadir}/%{name}/fish
%{_datadir}/%{name}/fish/powerline-setup.fish
%dir %{_datadir}/%{name}/i3
%{_datadir}/%{name}/i3/powerline-i3.py*
%dir %{_datadir}/%{name}/ipython
%{_datadir}/%{name}/ipython/post_0_11.py*
%{_datadir}/%{name}/ipython/pre_0_11.py*
%dir %{_datadir}/%{name}/qtile
%{_datadir}/%{name}/qtile/widget.py*
%dir %{_datadir}/%{name}/shell
%{_datadir}/%{name}/shell/powerline.sh
%dir %{_datadir}/%{name}/tcsh
%{_datadir}/%{name}/tcsh/powerline.tcsh
%dir %{_datadir}/%{name}/zsh
%{_datadir}/%{name}/zsh/__init__.py*
%{_datadir}/%{name}/zsh/powerline.zsh
%{python_sitelib}/*

#%files docs
#%doc docs/_build/html

%files -n vim-powerline
%doc LICENSE README.rst
%dir %{_datadir}/vim/vimfiles
%dir %{_datadir}/vim/vimfiles/autoload
%dir %{_datadir}/vim/vimfiles/autoload/powerline
%{_datadir}/vim/vimfiles/autoload/powerline/debug.vim
%dir %{_datadir}/vim/vimfiles/plugin
%{_datadir}/vim/vimfiles/plugin/powerline.vim
%dir %{_datadir}/appdata
%{_datadir}/appdata/vim-powerline.metainfo.xml

%files -n tmux-powerline
%doc LICENSE README.rst
%dir %{_datadir}/tmux
%{_datadir}/tmux/powerline*.conf

%changelog
* Thu Sep 17 2015 Andreas Schneider <asn@redhat.com> - 2.2-2
- resolves: #1246510 - Add appdate metainfo file for Gnome
- resolves: #1260620 - Install vim plugin to correct directory
- resolves: #1260617 - Rename vim plugin to vim-powerline

* Wed Sep 02 2015 Andreas Schneider <asn@redhat.com> - 2.2-1
- Update to version 2.2
  o Added support for newest psutil version.
  o Added support for non-SSL IMAP4 connection.
  o Added support for clickable tab names in Vim.
  o Added support for truncating tmux segments.
  o Added support for new (i3ipc) module that interacts with i3.
  o Added support for i3 modes.
  o Fixed coloring of network_load segment.
  o Fixed dash bindings on OS X.
  o Fixed parsing numbers starting with 2 supplied by POWERLINE_*_OVERRIDES
    environment variables.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 19 2015 Andreas Schneider <asn@redhat.com> - 2.1.4-1
- Update to version 2.1.4
  o Added support for placing powerline on the left in qtile.
  o Added qtile-1.9 support.
  o Fixed tmux-2.0 support.
  o Made it easier to run tests outside of travis.
  o Added some missing highlight groups.
  o Made it omit writing empty above lines.
  o Fixed UnicodeEncodeError when running powerline-lint with
    non-ASCII characters in error messages.
  o Fixed code that replaces &statusline value: it now is able
    to replace non-ASCII &statuslines as well.


* Fri Feb 20 2015 Andreas Schneider <asn@redhat.com> - 2.1-1
- Update to version 2.1
  o Added BAR support.
  o Added support for pdb (Python debugger) prompt.
  o Added more highlight groups to solarized colorscheme.
  o Updated zpython bindings.
  o Fixed C version of the client on non-Linux platforms.
  o Fixed some errors in powerline-lint code.
  o Fixed Python-2.6 incompatibilities in setup.py.

* Tue Jan 20 2015 Andreas Schneider <asn@redhat.com> - 2.0-1
- Update to version 2.0
  o Added fbterm (framebuffer terminal emulator) support.
  o Added theme with unicode-7.0 symbols.
  o Added support for PyPy3.
  o Compiler is now called with CFLAGS from environment in setup.py if present.
  o Added support for pyuv-1.*.
  o Added a way to write error log to Vim global variable.
  o powerline script now supports overrides from $POWERLINE_CONFIG_OVERRIDES,
    $POWERLINE_THEME_OVERRIDES environment variables, so does powerline-config
     script.
  o powerline and powerline-config scripts now support taking paths from
    $POWERLINE_CONFIG_PATHS.
  o powerline-lint is now able to report dictionaries which were merged in to
    form marked dictionary and what were the previous values of overridden
    values.
  o Added support for Byron Rakitzis’ rc shell reimplementation.
  o Added support for querying battery status on cygwin platform.

* Wed Dec 10 2014 Andreas Schneider <asn@redhat.com> - 1.3.1-2
- Update cflags patch.

* Tue Dec 09 2014 Andreas Schneider <asn@redhat.com> - 1.3.1-1
- Update to version 1.3.1.
- resolves: #1171420 - Fix passing optflags to the C compiler.

* Thu Dec 04 2014 Andreas Schneider <asn@redhat.com> - 1.3-2
- Fix powerline-config.

* Wed Dec 03 2014 Andreas Schneider <asn@redhat.com> - 1.3-1
- Update to version 1.3.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.1-8.20140508git9e7c6c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 08 2014 Andreas Schneider <asn@redhat.com> - 0.0.1-7.20140508git9e7c6c
- Update to revision 0.0.1-7.20140508git9e7c6c

* Wed Mar 12 2014 Andreas Schneider <asn@redhat.com> - 0.0.1-6.20140226git70a94e
- Update to revision 0.0.1-6.20140226git70a94e

* Thu Nov 28 2013 Andreas Schneider <asn@redhat.com> - 0.0.1-6.20131123gitdb80fc
- Remove EPEL support.
- Removed BuildRoot.

* Wed Nov 27 2013 Andreas Schneider <asn@redhat.com> - 0.0.1-5.20131123gitdb80fc
- Remove fontpatcher.py.patch
- Moved BuildReqruies.
- Try to fix build on EPEL5.

* Wed Nov 27 2013 Andreas Schneider <asn@redhat.com> - 0.0.1.20131123gitdb80fc-4
- Added missing vim directories.
- Fixed BuildRoot.
- Use fdupes only on Fedora.
- Use name tag in Requires.

* Mon Nov 25 2013 Andreas Schneider <asn@redhat.com> - 0.0.1.20131123gitdb80fc-3
- Changed define to global
- Moved BuildArch

* Sun Nov 24 2013 Andreas Schneider <asn@redhat.com> - 0.0.1.20131123gitdb80fc-2
- Set checkout.
- Set source URL.
- Fix default configuration path.

* Sun Nov 24 2013 Andreas Schneider <asn@redhat.com> - 0.0.1.20131123gitdb80fc-1
- Initial package.
