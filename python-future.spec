# TODO:
# - package tools
#
# Conditional build:
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Clean single-source support for Python 3 and 2
Name:		python-future
Version:	0.16.0
Release:	1
License:	MIT
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/00/2b/8d082ddfed935f3608cc61140df6dcbf0edea1bc3ab52fb6c29ae3e81e85/future-%{version}.tar.gz
# Source0-md5:	3e8e88a2bda48d54b1da7634d04760d7
URL:		https://python-future.org/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.3
BuildRequires:	python3-setuptools
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
future is the missing compatibility layer between Python 2 and
Python 3.  It allows you to use a single, clean Python 3.x-compatible
codebase to support both Python 2 and Python 3 with minimal overhead.

%package -n python3-future
Summary:	Clean single-source support for Python 3 and 2
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.3

%description -n python3-future
future is the missing compatibility layer between Python 2 and
Python 3.  It allows you to use a single, clean Python 3.x-compatible
codebase to support both Python 2 and Python 3 with minimal overhead.

%prep
%setup -q -n future-%{version}

%build
%if %{with python2}
%py_build
%endif

%if %{with python3}
%py3_build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst
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
%doc README.rst
%{py3_sitescriptdir}/future
%{py3_sitescriptdir}/libfuturize
%{py3_sitescriptdir}/libpasteurize
%{py3_sitescriptdir}/past
%{py3_sitescriptdir}/future-%{version}-py*.egg-info
%endif
