from pathlib import Path
import stat
import subprocess
import zipfile

import pytest

from scripts import lambda_package

REQUIRED_MEMBERS = {
    **{path: b"application" for path in lambda_package.REQUIRED_APPLICATION_PATHS},
    **{path: b"static" for path in lambda_package.REQUIRED_STATIC_PATHS},
    **{
        path: b"dependency"
        for path in lambda_package.REQUIRED_DEPENDENCY_PATHS.values()
    },
}


def write_synthetic_archive(
    archive: Path,
    members: dict[str, bytes] | None = None,
) -> None:
    with zipfile.ZipFile(archive, "w") as package:
        for name, content in (members or REQUIRED_MEMBERS).items():
            package.writestr(name, content)


def test_audit_accepts_required_paths(tmp_path):
    archive = tmp_path / "lambda.zip"
    write_synthetic_archive(archive)

    report = lambda_package.audit_package(archive)

    assert report.archive == archive
    assert report.member_count == len(REQUIRED_MEMBERS)
    assert report.application_paths == lambda_package.REQUIRED_APPLICATION_PATHS
    assert report.static_assets == lambda_package.REQUIRED_STATIC_PATHS


def test_audit_rejects_missing_handler(tmp_path):
    archive = tmp_path / "lambda.zip"
    members = {
        name: content
        for name, content in REQUIRED_MEMBERS.items()
        if name != "src/lambda_handler.py"
    }
    write_synthetic_archive(archive, members)

    with pytest.raises(
        lambda_package.PackageAuditError,
        match="src/lambda_handler.py",
    ):
        lambda_package.audit_package(archive)


@pytest.mark.parametrize("static_asset", lambda_package.REQUIRED_STATIC_PATHS)
def test_audit_rejects_missing_static_assets(tmp_path, static_asset):
    archive = tmp_path / "lambda.zip"
    members = {
        name: content
        for name, content in REQUIRED_MEMBERS.items()
        if name != static_asset
    }
    write_synthetic_archive(archive, members)

    with pytest.raises(lambda_package.PackageAuditError, match=static_asset):
        lambda_package.audit_package(archive)


@pytest.mark.parametrize(
    "forbidden_path",
    [
        ".git/config",
        ".github/workflows/ci.yml",
        ".venv/pyvenv.cfg",
        "AGENTS.md",
        "README.md",
        "docs/setup.md",
        "requirements-dev.txt",
        "tests/test_main.py",
        "__pycache__/main.cpython-314.pyc",
        "pytest/__init__.py",
        "black/__init__.py",
        "ruff/__init__.py",
    ],
)
def test_audit_rejects_forbidden_content(tmp_path, forbidden_path):
    archive = tmp_path / "lambda.zip"
    write_synthetic_archive(
        archive,
        {**REQUIRED_MEMBERS, forbidden_path: b"forbidden"},
    )

    with pytest.raises(lambda_package.PackageAuditError, match="Forbidden"):
        lambda_package.audit_package(archive)


@pytest.mark.parametrize(
    "directory_name",
    [".git", ".github", ".venv", ".pytest_cache", "__pycache__"],
)
@pytest.mark.parametrize("parent", ["", "src", "static", "dependency/package"])
def test_audit_rejects_prohibited_directories_at_any_depth(
    tmp_path,
    directory_name,
    parent,
):
    archive = tmp_path / "lambda.zip"
    prohibited_path = "/".join(
        part for part in (parent, directory_name, "content") if part
    )
    write_synthetic_archive(
        archive,
        {**REQUIRED_MEMBERS, prohibited_path: b"forbidden"},
    )

    with pytest.raises(lambda_package.PackageAuditError, match="Forbidden"):
        lambda_package.audit_package(archive)


@pytest.mark.parametrize(
    "filename",
    [".coverage", "AGENTS.md", "README.md", "requirements-dev.txt"],
)
@pytest.mark.parametrize("parent", ["", "src", "dependency/package"])
def test_audit_rejects_prohibited_filenames_at_any_depth(
    tmp_path,
    filename,
    parent,
):
    archive = tmp_path / "lambda.zip"
    prohibited_path = "/".join(part for part in (parent, filename) if part)
    write_synthetic_archive(
        archive,
        {**REQUIRED_MEMBERS, prohibited_path: b"forbidden"},
    )

    with pytest.raises(lambda_package.PackageAuditError, match="Forbidden"):
        lambda_package.audit_package(archive)


@pytest.mark.parametrize("directory_name", ["tests", "docs", "scripts", "htmlcov"])
def test_audit_rejects_generic_development_directories_only_at_root(
    tmp_path,
    directory_name,
):
    root_archive = tmp_path / f"root-{directory_name}.zip"
    write_synthetic_archive(
        root_archive,
        {**REQUIRED_MEMBERS, f"{directory_name}/content": b"forbidden"},
    )
    nested_archive = tmp_path / f"nested-{directory_name}.zip"
    write_synthetic_archive(
        nested_archive,
        {
            **REQUIRED_MEMBERS,
            f"package/{directory_name}/content": b"allowed",
            "package-1.0.0.dist-info/METADATA": b"metadata",
        },
    )

    with pytest.raises(lambda_package.PackageAuditError, match="Forbidden"):
        lambda_package.audit_package(root_archive)

    lambda_package.audit_package(nested_archive)


@pytest.mark.parametrize(
    "allowed_path",
    [
        "src/README.rst",
        "src/MY_AGENTS.md",
        "config/requirements-development.txt",
        "src/coverage.py",
        "src/venv/content",
        "src/github/content",
    ],
)
def test_audit_allows_similar_repository_names(tmp_path, allowed_path):
    archive = tmp_path / "lambda.zip"
    write_synthetic_archive(
        archive,
        {**REQUIRED_MEMBERS, allowed_path: b"allowed"},
    )

    lambda_package.audit_package(archive)


@pytest.mark.parametrize(
    "environment_path",
    [
        ".env",
        ".env.example",
        ".env.local",
        ".env.production",
        "src/.env",
        "src/.env.local",
        "config/.env.production",
    ],
)
def test_audit_rejects_environment_file_variants(tmp_path, environment_path):
    archive = tmp_path / "lambda.zip"
    write_synthetic_archive(
        archive,
        {**REQUIRED_MEMBERS, environment_path: b"SECRET=test"},
    )

    with pytest.raises(lambda_package.PackageAuditError, match="environment file"):
        lambda_package.audit_package(archive)


@pytest.mark.parametrize(
    "allowed_path",
    [
        "environment.py",
        "env.py",
        "my.env",
        ".envrc",
        "config/environment.py",
    ],
)
def test_audit_allows_similar_non_environment_filenames(tmp_path, allowed_path):
    archive = tmp_path / "lambda.zip"
    write_synthetic_archive(
        archive,
        {**REQUIRED_MEMBERS, allowed_path: b"allowed"},
    )

    lambda_package.audit_package(archive)


def test_audit_rejects_path_traversal(tmp_path):
    archive = tmp_path / "lambda.zip"
    write_synthetic_archive(
        archive,
        {**REQUIRED_MEMBERS, "../outside.py": b"unsafe"},
    )

    with pytest.raises(lambda_package.PackageAuditError, match="Path traversal"):
        lambda_package.audit_package(archive)


def test_audit_rejects_absolute_paths(tmp_path):
    archive = tmp_path / "lambda.zip"
    write_synthetic_archive(
        archive,
        {**REQUIRED_MEMBERS, "/absolute.py": b"unsafe"},
    )

    with pytest.raises(lambda_package.PackageAuditError, match="Absolute"):
        lambda_package.audit_package(archive)


def test_audit_rejects_duplicate_members(tmp_path):
    archive = tmp_path / "lambda.zip"
    write_synthetic_archive(archive)
    with pytest.warns(UserWarning, match="Duplicate"):
        with zipfile.ZipFile(archive, "a") as package:
            package.writestr("src/lambda_handler.py", b"duplicate")

    with pytest.raises(lambda_package.PackageAuditError, match="Duplicate"):
        lambda_package.audit_package(archive)


def test_audit_rejects_symbolic_links(tmp_path):
    archive = tmp_path / "lambda.zip"
    write_synthetic_archive(archive)
    symbolic_link = zipfile.ZipInfo("src/link.py")
    symbolic_link.create_system = 3
    symbolic_link.external_attr = (stat.S_IFLNK | 0o777) << 16
    with zipfile.ZipFile(archive, "a") as package:
        package.writestr(symbolic_link, b"target.py")

    with pytest.raises(lambda_package.PackageAuditError, match="Symbolic-link"):
        lambda_package.audit_package(archive)


def test_audit_rejects_unexpected_enclosing_root(tmp_path):
    archive = tmp_path / "lambda.zip"
    write_synthetic_archive(
        archive,
        {f"bundle/{name}": content for name, content in REQUIRED_MEMBERS.items()},
    )

    with pytest.raises(
        lambda_package.PackageAuditError,
        match="Unexpected enclosing root",
    ):
        lambda_package.audit_package(archive)


def test_audit_rejects_empty_and_malformed_archives(tmp_path):
    empty_archive = tmp_path / "empty.zip"
    with zipfile.ZipFile(empty_archive, "w"):
        pass
    malformed_archive = tmp_path / "malformed.zip"
    malformed_archive.write_bytes(b"not a zip")

    with pytest.raises(lambda_package.PackageAuditError, match="Archive is empty"):
        lambda_package.audit_package(empty_archive)
    with pytest.raises(lambda_package.PackageAuditError, match="Malformed"):
        lambda_package.audit_package(malformed_archive)


def test_audit_rejects_backslash_paths(monkeypatch, tmp_path):
    archive = tmp_path / "lambda.zip"
    archive.write_bytes(b"synthetic archive")
    members = [zipfile.ZipInfo(name) for name in REQUIRED_MEMBERS]
    unsafe_member = zipfile.ZipInfo("safe-name.py")
    unsafe_member.filename = "src\\unsafe.py"
    members.append(unsafe_member)

    class SyntheticZipFile:
        def __init__(self, path):
            self.path = path

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def infolist(self):
            return members

    monkeypatch.setattr(lambda_package.zipfile, "ZipFile", SyntheticZipFile)

    with pytest.raises(lambda_package.PackageAuditError, match="Backslash"):
        lambda_package.audit_package(archive)


def test_archive_members_are_written_in_stable_sorted_order(tmp_path):
    staging = tmp_path / "staging"
    (staging / "zeta").mkdir(parents=True)
    (staging / "alpha").mkdir()
    (staging / "zeta" / "last.py").write_text("last")
    (staging / "alpha" / "first.py").write_text("first")
    archive = tmp_path / "lambda.zip"

    lambda_package.write_archive(staging, archive)

    with zipfile.ZipFile(archive) as package:
        assert package.namelist() == [
            "alpha/first.py",
            "zeta/last.py",
        ]


def fake_dependency_install(staging_directory: Path) -> None:
    for path in lambda_package.REQUIRED_DEPENDENCY_PATHS.values():
        dependency = staging_directory / path
        dependency.parent.mkdir(parents=True, exist_ok=True)
        dependency.write_text("dependency")


def test_linux_dependency_normalization_removes_only_colorama(tmp_path):
    colorama_package = tmp_path / "colorama"
    colorama_metadata = tmp_path / "colorama-0.4.6.dist-info"
    unrelated_package = tmp_path / "click"
    unrelated_metadata = tmp_path / "click-8.4.2.dist-info"

    for directory in (
        colorama_package,
        colorama_metadata,
        unrelated_package,
        unrelated_metadata,
    ):
        directory.mkdir()
        (directory / "content.txt").write_text("content")

    lambda_package.normalize_linux_dependencies(tmp_path)

    assert not colorama_package.exists()
    assert not colorama_metadata.exists()
    assert unrelated_package.exists()
    assert unrelated_metadata.exists()


def test_linux_dependency_normalization_succeeds_without_colorama(tmp_path):
    unrelated_package = tmp_path / "click"
    unrelated_package.mkdir()

    lambda_package.normalize_linux_dependencies(tmp_path)

    assert unrelated_package.exists()


def test_audit_does_not_require_colorama(tmp_path):
    archive = tmp_path / "lambda.zip"
    write_synthetic_archive(archive)

    report = lambda_package.audit_package(archive)

    assert "colorama" not in lambda_package.REQUIRED_DEPENDENCY_PATHS
    assert "colorama" not in report.dependency_packages


def test_build_creates_output_parent_and_replaces_only_target(
    monkeypatch,
    tmp_path,
):
    monkeypatch.setattr(
        lambda_package,
        "install_runtime_dependencies",
        fake_dependency_install,
    )
    output = tmp_path / "dist" / "lambda.zip"
    output.parent.mkdir()
    output.write_bytes(b"old archive")
    unrelated = output.parent / "keep.txt"
    unrelated.write_text("keep")

    result = lambda_package.build_package(output)

    assert result == output.resolve()
    assert zipfile.is_zipfile(output)
    assert unrelated.read_text() == "keep"


def test_build_failure_cleans_temporary_staging(monkeypatch, tmp_path):
    staging_directories = []
    real_temporary_directory = lambda_package.tempfile.TemporaryDirectory

    class RecordingTemporaryDirectory:
        def __init__(self, *args, **kwargs):
            self.temporary_directory = real_temporary_directory(
                *args,
                dir=tmp_path,
                **kwargs,
            )

        def __enter__(self):
            directory = self.temporary_directory.__enter__()
            staging_directories.append(Path(directory))
            return directory

        def __exit__(self, *args):
            return self.temporary_directory.__exit__(*args)

    def fail_install(staging_directory):
        raise lambda_package.PackageBuildError("test installation failure")

    monkeypatch.setattr(
        lambda_package.tempfile,
        "TemporaryDirectory",
        RecordingTemporaryDirectory,
    )
    monkeypatch.setattr(
        lambda_package,
        "install_runtime_dependencies",
        fail_install,
    )

    with pytest.raises(lambda_package.PackageBuildError):
        lambda_package.build_package(tmp_path / "dist" / "lambda.zip")

    assert staging_directories
    assert all(not directory.exists() for directory in staging_directories)


def test_pip_command_targets_linux_cp314_runtime_dependencies(tmp_path):
    command = lambda_package.pip_install_command(tmp_path)

    assert str(lambda_package.REQUIREMENTS_FILE) in command
    assert "requirements-dev.txt" not in command
    assert "--platform" in command
    assert "manylinux2014_x86_64" in command
    assert "--python-version" in command
    assert "3.14" in command
    assert "--abi" in command
    assert "cp314" in command
    assert "--only-binary=:all:" in command
    assert "--no-compile" in command


def test_copy_runtime_files_excludes_local_environment_files(monkeypatch, tmp_path):
    source_root = tmp_path / "project"
    (source_root / "src").mkdir(parents=True)
    (source_root / "static").mkdir()
    (source_root / "src" / "__init__.py").write_text("")
    (source_root / "src" / ".env").write_text("SECRET=test")
    (source_root / "src" / ".env.local").write_text("SECRET=local")
    (source_root / "src" / ".envrc").write_text("allowed")
    (source_root / "static" / "main.css").write_text(".card {}")
    monkeypatch.setattr(lambda_package, "PROJECT_ROOT", source_root)
    staging = tmp_path / "staging"
    staging.mkdir()

    lambda_package.copy_runtime_files(staging)

    assert (staging / "src" / "__init__.py").exists()
    assert not (staging / "src" / ".env").exists()
    assert not (staging / "src" / ".env.local").exists()
    assert (staging / "src" / ".envrc").exists()


def test_runtime_copy_filter_matches_any_depth_archive_policy(monkeypatch, tmp_path):
    source_root = tmp_path / "project"
    src = source_root / "src"
    static = source_root / "static"
    src.mkdir(parents=True)
    static.mkdir()
    (src / "__init__.py").write_text("")
    (static / "main.css").write_text(".card {}")

    for directory_name in lambda_package.ANY_DEPTH_FORBIDDEN_DIRECTORY_NAMES:
        prohibited_directory = src / "package" / directory_name
        prohibited_directory.mkdir(parents=True)
        (prohibited_directory / "content").write_text("forbidden")

    for filename in lambda_package.ANY_DEPTH_FORBIDDEN_FILE_NAMES:
        prohibited_file = src / "package" / filename
        prohibited_file.parent.mkdir(parents=True, exist_ok=True)
        prohibited_file.write_text("forbidden")

    nested_tests = src / "package" / "tests"
    nested_tests.mkdir()
    (nested_tests / "runtime_test_data.py").write_text("allowed")
    (src / "README.rst").write_text("allowed")

    monkeypatch.setattr(lambda_package, "PROJECT_ROOT", source_root)
    staging = tmp_path / "staging"
    staging.mkdir()

    lambda_package.copy_runtime_files(staging)

    for directory_name in lambda_package.ANY_DEPTH_FORBIDDEN_DIRECTORY_NAMES:
        assert not (staging / "src" / "package" / directory_name).exists()
    for filename in lambda_package.ANY_DEPTH_FORBIDDEN_FILE_NAMES:
        assert not (staging / "src" / "package" / filename).exists()
    assert (staging / "src" / "package" / "tests" / "runtime_test_data.py").exists()
    assert (staging / "src" / "README.rst").exists()


def test_install_failure_is_reported_as_package_build_error(monkeypatch, tmp_path):
    def fail_subprocess(*args, **kwargs):
        raise subprocess.CalledProcessError(1, ["pip"])

    monkeypatch.setattr(lambda_package.subprocess, "run", fail_subprocess)

    with pytest.raises(lambda_package.PackageBuildError):
        lambda_package.install_runtime_dependencies(tmp_path)


def test_audit_errors_return_non_zero_command_result(tmp_path, capsys):
    archive = tmp_path / "invalid.zip"
    write_synthetic_archive(archive, {"src/lambda_handler.py": b"incomplete"})

    result = lambda_package.main(["audit", "--archive", str(archive)])

    assert result == 1
    assert "ERROR:" in capsys.readouterr().err


def test_environment_file_audit_error_returns_non_zero(tmp_path, capsys):
    archive = tmp_path / "invalid-environment.zip"
    write_synthetic_archive(
        archive,
        {**REQUIRED_MEMBERS, "config/.env.production": b"SECRET=test"},
    )

    result = lambda_package.main(["audit", "--archive", str(archive)])

    assert result == 1
    assert ".env.production" in capsys.readouterr().err


def test_nested_repository_content_audit_error_returns_non_zero(tmp_path, capsys):
    archive = tmp_path / "nested-repository-content.zip"
    write_synthetic_archive(
        archive,
        {**REQUIRED_MEMBERS, "src/package/.git/config": b"forbidden"},
    )

    result = lambda_package.main(["audit", "--archive", str(archive)])

    assert result == 1
    assert "src/package/.git/config" in capsys.readouterr().err
