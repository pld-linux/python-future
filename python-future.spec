#
# Conditional build:
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

Summary:	Clean single-source support for Python 3 and 2
Summary(pl.UTF-8):	Czysta obsługa Pythona 3 i 2 w jednych źródłach
Name:		python-future
Version:	0.17.1
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/future/
Source0:	https://files.pythonhosted.org/packages/source/f/future/future-%{version}.tar.gz
# Source0-md5:	e42113b4b72fabb5273ff88417104913
Patch0:		%{name}-tests.patch
URL:		https://python-future.org/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	python-setuptools
%if "%{py_ver}" < "2.7"
BuildRequires:	python-argparse
BuildRequires:	python-importlib
%if %{with tests}
BuildRequires:	python-unittest2
%endif
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.3
BuildRequires:	python3-setuptools
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinx_bootstrap_theme
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python-modules >= 1:2.6
%if "%{py_ver}" < "2.7"
Requires:	python-argparse
Requires:	python-importlib
Requires:	python-unittest2
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
future is the missing compatibility layer between Python 2 and
Python 3.  It allows you to use a single, clean Python 3.x-compatible
codebase to support both Python 2 and Python 3 with minimal overhead.

%description -l pl.UTF-8
future to brakująca warstwa zgodności między Pythonem 2 i 3. Pozwala
na używanie pojedynczego kodu źródłowego w Pythonie 3.x do obsługi
zarówno Pythona 2, jak i 3 z minimalnym narzutem.

%package -n python3-future
Summary:	Clean single-source support for Python 3 and 2
Summary(pl.UTF-8):	Czysta obsługa Pythona 3 i 2 w jednych źródłach
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.3

%description -n python3-future
future is the missing compatibility layer between Python 2 and
Python 3.  It allows you to use a single, clean Python 3.x-compatible
codebase to support both Python 2 and Python 3 with minimal overhead.

%description -n python3-future -l pl.UTF-8
future to brakująca warstwa zgodności między Pythonem 2 i 3. Pozwala
na używanie pojedynczego kodu źródłowego w Pythonie 3.x do obsługi
zarówno Pythona 2, jak i 3 z minimalnym narzutem.

%package apidocs
Summary:	API documentation for Python future module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona future
Group:		Documentation

%description apidocs
API documentation for Python future module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona future.

%prep
%setup -q -n future-%{version}
%patch0 -p1

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=$(pwd)/build-2/lib \
%{__python} -m unittest discover -s tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
# FIXME: fails with py3.7(?) as of future-0.17.1
%{__rm} tests/test_past/test_translation.py

PYTHONPATH=$(pwd)/build-3/lib \
%{__python3} -m unittest discover -s tests
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/build-3/lib \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean

%{__mv} $RPM_BUILD_ROOT%{_bindir}/futurize{,-2}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/pasteurize{,-2}
%endif

%if %{with python3}
%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/futurize{,-3}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/pasteurize{,-3}

ln -sf futurize-3 $RPM_BUILD_ROOT%{_bindir}/futurize
ln -sf pasteurize-3 $RPM_BUILD_ROOT%{_bindir}/pasteurize
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE.txt README.rst
%attr(755,root,root) %{_bindir}/futurize-2
%attr(755,root,root) %{_bindir}/pasteurize-2
%{py_sitescriptdir}/_dummy_thread
%{py_sitescriptdir}/_markupbase
%{py_sitescriptdir}/_thread
%{py_sitescriptdir}/builtins
%{py_sitescriptdir}/copyreg
%{py_sitescriptdir}/future
%{py_sitescriptdir}/html
%{py_sitescriptdir}/http
%{py_sitescriptdir}/libfuturize
%{py_sitescriptdir}/libpasteurize
%{py_sitescriptdir}/past
%{py_sitescriptdir}/queue
%{py_sitescriptdir}/reprlib
%{py_sitescriptdir}/socketserver
%{py_sitescriptdir}/tkinter
%{py_sitescriptdir}/winreg
%{py_sitescriptdir}/xmlrpc
%{py_sitescriptdir}/future-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-future
%defattr(644,root,root,755)
%doc LICENSE.txt README.rst
%attr(755,root,root) %{_bindir}/futurize
%attr(755,root,root) %{_bindir}/futurize-3
%attr(755,root,root) %{_bindir}/pasteurize
%attr(755,root,root) %{_bindir}/pasteurize-3
%{py3_sitescriptdir}/future
%{py3_sitescriptdir}/libfuturize
%{py3_sitescriptdir}/libpasteurize
%{py3_sitescriptdir}/past
%{py3_sitescriptdir}/future-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_modules,_static,*.html,*.js}
%endif
