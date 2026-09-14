# The proprietary portion of MakeMKV does not include debug symbols
%global debug_package %{nil}
# The EULA requires the program files to remain unchanged during packaging
%global __strip /bin/true

Name:           makemkv-bin
Version:        1.18.4
Release:        %autorelease
Summary:        A decryption and transcoding tool for DVD and Blu-ray discs

# MakeMKV EULA: https://pastebin.com/raw/PmWJ4CxA
# The blues.jar component is exempt from the EULA and licensed as GPL 2.0+
License:        Proprietary AND GPL-2.0-or-later
URL:            https://www.makemkv.com/
Source:         https://www.makemkv.com/download/makemkv-bin-%{version}.tar.gz

BuildRequires:  javapackages-local-openjdk25
BuildRequires:  javapackages-tools
BuildRequires:  make

Requires:       libmakemkv >= %{version}-1
Requires:       libdriveio >= %{version}-1
Requires:       makemkv-oss >= %{version}-1
Recommends:     libmmbd >= %{version}-1
Recommends:     makemkv-blues = %{version}-%{release}

ExclusiveArch:  aarch64 x86_64

%description
This package contains the proprietary binary used by MakeMKV that provides the
makemkvcon and sdftool.

%package -n makemkv-blues
Summary:        MakeMKV's BD-J emulation server (BLUES)
Requires:       jre
Requires:       makemkv >= %{version}-1
ExclusiveArch:  aarch64 x86_64

%description -n makemkv-blues
MakeMKV's BD-J emulation server (BLUES).

%package -n makemkv-blues-javadoc
Summary:        JavaDoc documentation for MakeMKV's Java component (BLUES)
# RPM Fusion mash doesn't work well with noarch sub-packages... to be revisited.
#BuildArch: noarch
ExclusiveArch:  aarch64 x86_64

%description -n makemkv-blues-javadoc
JavaDoc documentation for MakeMKV's Java component (BLUES).

%prep
%autosetup
mkdir tmp
touch tmp/eula_accepted
# Extract BLUES — the BD-J emulation server
unzip src/share/blues.jar SOURCE/* -d blues

%build
# Build BLUES JavaDoc
pushd blues/SOURCE
javadoc blues -d ../javadoc
popd

%install
%make_install
# Install BLUES JavaDocs
mkdir -p %{buildroot}%{_javadocdir}/makemkv-blues
cp -a blues/javadoc/* %{buildroot}%{_javadocdir}/makemkv-blues

%files
%license src/eula_en_linux.txt
%{_bindir}/makemkvcon
%{_bindir}/sdftool
%dir %{_datadir}/MakeMKV
%{_datadir}/MakeMKV/appdata.tar

%files -n makemkv-blues
# The blues.jar component is exempt from the EULA and licensed as GPL 2.0+
# The source code is included in the bundled JAR file.
%{_datadir}/MakeMKV/blues.jar
%{_datadir}/MakeMKV/blues.policy

%files -n makemkv-blues-javadoc
%{_javadocdir}/makemkv-blues

%changelog
%autochangelog
