"""Build and structurally audit the AWS Lambda deployment archive."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import sys
import tempfile
from typing import Iterable, Sequence
import zipfile

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REQUIREMENTS_FILE = PROJECT_ROOT / "requirements.txt"
RUNTIME_DIRECTORIES = ("src", "static")
FIXED_ZIP_TIMESTAMP = (2020, 1, 1, 0, 0, 0)
REGULAR_FILE_MODE = 0o100644

PIP_TARGET_OPTIONS = (
    "--platform",
    "manylinux2014_x86_64",
    "--implementation",
    "cp",
    "--python-version",
    "3.14",
    "--abi",
    "cp314",
    "--only-binary=:all:",
)

REQUIRED_APPLICATION_PATHS = (
    "src/__init__.py",
    "src/config.py",
    "src/database.py",
    "src/health_service.py",
    "src/lambda_handler.py",
    "src/logging_config.py",
    "src/main.py",
    "src/models.py",
    "src/services/__init__.py",
    "src/services/cocktail_service.py",
)
REQUIRED_STATIC_PATHS = (
    "static/favicon.svg",
    "static/main.css",
)
REQUIRED_DEPENDENCY_PATHS = {
    "annotated-doc": "annotated_doc/__init__.py",
    "annotated-types": "annotated_types/__init__.py",
    "anyio": "anyio/__init__.py",
    "boto3": "boto3/__init__.py",
    "botocore": "botocore/__init__.py",
    "click": "click/__init__.py",
    "dateutil": "dateutil/__init__.py",
    "dotenv": "dotenv/__init__.py",
    "fastapi": "fastapi/__init__.py",
    "h11": "h11/__init__.py",
    "idna": "idna/__init__.py",
    "jmespath": "jmespath/__init__.py",
    "mangum": "mangum/__init__.py",
    "pydantic": "pydantic/__init__.py",
    "pydantic-core": "pydantic_core/__init__.py",
    "s3transfer": "s3transfer/__init__.py",
    "six": "six.py",
    "starlette": "starlette/__init__.py",
    "typing-extensions": "typing_extensions.py",
    "typing-inspection": "typing_inspection/__init__.py",
    "urllib3": "urllib3/__init__.py",
    "uvicorn": "uvicorn/__init__.py",
}

ANY_DEPTH_FORBIDDEN_DIRECTORY_NAMES = {
    ".git",
    ".github",
    ".pytest_cache",
    ".venv",
    "__pycache__",
}
ROOT_ONLY_FORBIDDEN_DIRECTORY_NAMES = {
    "docs",
    "htmlcov",
    "scripts",
    "tests",
}
ANY_DEPTH_FORBIDDEN_FILE_NAMES = {
    ".coverage",
    "agents.md",
    "readme.md",
    "requirements-dev.txt",
}
DEVELOPMENT_PACKAGE_PREFIXES = (
    "_pytest",
    "black",
    "pytest",
    "ruff",
)


class PackageBuildError(RuntimeError):
    """Raised when the Lambda package cannot be built."""


class PackageAuditError(RuntimeError):
    """Raised when a Lambda archive fails structural auditing."""

    def __init__(self, failures: Sequence[str]) -> None:
        self.failures = tuple(failures)
        super().__init__("; ".join(self.failures))


@dataclass(frozen=True)
class AuditReport:
    archive: Path
    member_count: int
    compressed_size: int
    uncompressed_size: int
    application_paths: tuple[str, ...]
    dependency_packages: tuple[str, ...]
    static_assets: tuple[str, ...]


def pip_install_command(staging_directory: Path) -> list[str]:
    """Return the exact cross-platform pip installation command."""

    return [
        sys.executable,
        "-m",
        "pip",
        "install",
        "--requirement",
        str(REQUIREMENTS_FILE),
        "--target",
        str(staging_directory),
        "--no-compile",
        *PIP_TARGET_OPTIONS,
    ]


def install_runtime_dependencies(staging_directory: Path) -> None:
    """Install Linux CPython 3.14 wheels into the staging root."""

    try:
        subprocess.run(
            pip_install_command(staging_directory),
            cwd=PROJECT_ROOT,
            check=True,
        )
        shutil.rmtree(staging_directory / "bin", ignore_errors=True)
        normalize_linux_dependencies(staging_directory)
    except (OSError, subprocess.CalledProcessError) as exc:
        raise PackageBuildError(
            "Runtime dependency installation failed for CPython 3.14 "
            "manylinux2014 x86-64 wheels"
        ) from exc


def normalize_linux_dependencies(staging_directory: Path) -> None:
    """Remove packages selected only for the Windows build host."""

    shutil.rmtree(staging_directory / "colorama", ignore_errors=True)

    for metadata_directory in staging_directory.glob("colorama-*.dist-info"):
        if metadata_directory.is_dir():
            shutil.rmtree(metadata_directory)


def copy_runtime_files(staging_directory: Path) -> None:
    """Copy only application packages and static assets into staging."""

    for directory_name in RUNTIME_DIRECTORIES:
        source = PROJECT_ROOT / directory_name
        destination = staging_directory / directory_name
        shutil.copytree(
            source,
            destination,
            ignore=runtime_copy_ignore,
        )


def iter_archive_files(staging_directory: Path) -> list[Path]:
    """Return regular staging files in stable archive-path order."""

    files = []
    for path in staging_directory.rglob("*"):
        if path.is_symlink():
            raise PackageBuildError(f"Staging content contains a symbolic link: {path}")
        if path.is_file():
            files.append(path)

    return sorted(
        files,
        key=lambda path: path.relative_to(staging_directory).as_posix(),
    )


def write_archive(staging_directory: Path, archive: Path) -> None:
    """Write a stable, root-level Lambda ZIP from staging."""

    with zipfile.ZipFile(
        archive,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as package:
        for path in iter_archive_files(staging_directory):
            archive_path = path.relative_to(staging_directory).as_posix()
            member = zipfile.ZipInfo(archive_path, FIXED_ZIP_TIMESTAMP)
            member.compress_type = zipfile.ZIP_DEFLATED
            member.create_system = 3
            member.external_attr = REGULAR_FILE_MODE << 16
            package.writestr(member, path.read_bytes(), compresslevel=9)


def build_package(output: Path) -> Path:
    """Build a fresh Lambda package and atomically replace only output."""

    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary_archive: Path | None = None

    try:
        with tempfile.TemporaryDirectory(prefix="cocktail-ai-lambda-build-") as staging:
            staging_directory = Path(staging)
            install_runtime_dependencies(staging_directory)
            copy_runtime_files(staging_directory)

            with tempfile.NamedTemporaryFile(
                dir=output.parent,
                prefix=f".{output.name}.",
                suffix=".tmp",
                delete=False,
            ) as temporary_file:
                temporary_archive = Path(temporary_file.name)

            write_archive(staging_directory, temporary_archive)
            os.replace(temporary_archive, output)
            temporary_archive = None
    except PackageBuildError:
        raise
    except (OSError, zipfile.BadZipFile) as exc:
        raise PackageBuildError(f"Unable to build Lambda archive: {exc}") from exc
    finally:
        if temporary_archive is not None:
            temporary_archive.unlink(missing_ok=True)

    return output


def _is_symbolic_link(member: zipfile.ZipInfo) -> bool:
    mode = member.external_attr >> 16
    return stat.S_IFMT(mode) == stat.S_IFLNK


def _forbidden_path_reason(name: str, *, is_directory: bool = False) -> str | None:
    path = PurePosixPath(name)
    lowered_parts = tuple(part.lower() for part in path.parts)
    top_level = lowered_parts[0] if lowered_parts else ""
    directory_parts = lowered_parts if is_directory else lowered_parts[:-1]

    if any(part in ANY_DEPTH_FORBIDDEN_DIRECTORY_NAMES for part in directory_parts):
        return "development or repository directory"

    if top_level in ROOT_ONLY_FORBIDDEN_DIRECTORY_NAMES and (
        is_directory or len(lowered_parts) > 1
    ):
        return "development or repository directory"

    if (
        not is_directory
        and lowered_parts
        and lowered_parts[-1] in ANY_DEPTH_FORBIDDEN_FILE_NAMES
    ):
        return "development, repository or local environment file"

    if any(part == ".env" or part.startswith(".env.") for part in lowered_parts):
        return "development, repository or local environment file"

    if name.lower().endswith((".pyc", ".pyo")):
        return "Python cache file"

    if top_level.startswith(DEVELOPMENT_PACKAGE_PREFIXES):
        return "development-only package"

    return None


def runtime_copy_ignore(directory: str, names: list[str]) -> set[str]:
    """Apply archive content policy while copying application runtime files."""

    ignored = set()
    source_directory = Path(directory)

    for name in names:
        candidate = source_directory / name
        archive_path = candidate.relative_to(PROJECT_ROOT).as_posix()
        if _forbidden_path_reason(
            archive_path,
            is_directory=candidate.is_dir(),
        ):
            ignored.add(name)

    return ignored


def _validate_member(member: zipfile.ZipInfo) -> list[str]:
    failures = []
    name = member.filename

    if "\\" in name:
        failures.append(f"Backslash-based archive path: {name}")
        return failures

    path = PurePosixPath(name)
    if path.is_absolute() or (path.parts and ":" in path.parts[0]):
        failures.append(f"Absolute archive path: {name}")
    if ".." in path.parts:
        failures.append(f"Path traversal archive member: {name}")
    if _is_symbolic_link(member):
        failures.append(f"Symbolic-link archive member: {name}")

    forbidden_reason = _forbidden_path_reason(name, is_directory=member.is_dir())
    if forbidden_reason:
        failures.append(f"Forbidden {forbidden_reason}: {name}")

    return failures


def _missing_path_failures(names: set[str]) -> list[str]:
    failures = []

    for path in REQUIRED_APPLICATION_PATHS:
        if path not in names:
            failures.append(f"Missing required application path: {path}")

    for path in REQUIRED_STATIC_PATHS:
        if path not in names:
            failures.append(f"Missing required static asset: {path}")

    for package, path in REQUIRED_DEPENDENCY_PATHS.items():
        if path not in names:
            failures.append(f"Missing required runtime dependency {package}: {path}")

    return failures


def audit_package(archive: Path) -> AuditReport:
    """Audit a Lambda ZIP and return its structural report."""

    archive = archive.resolve()
    failures: list[str] = []

    try:
        compressed_size = archive.stat().st_size
        with zipfile.ZipFile(archive) as package:
            members = package.infolist()
            if not members:
                failures.append("Archive is empty")

            names = [member.filename for member in members]
            duplicate_names = sorted(
                name for name, count in Counter(names).items() if count > 1
            )
            failures.extend(
                f"Duplicate archive member: {name}" for name in duplicate_names
            )

            for member in members:
                failures.extend(_validate_member(member))

            name_set = set(names)
            failures.extend(_missing_path_failures(name_set))

            if "src/lambda_handler.py" not in name_set and any(
                "/src/lambda_handler.py" in name for name in names
            ):
                failures.append("Unexpected enclosing root directory")

            uncompressed_size = sum(member.file_size for member in members)
    except (OSError, zipfile.BadZipFile) as exc:
        raise PackageAuditError((f"Malformed or unreadable archive: {exc}",)) from exc

    if failures:
        raise PackageAuditError(tuple(dict.fromkeys(failures)))

    return AuditReport(
        archive=archive,
        member_count=len(members),
        compressed_size=compressed_size,
        uncompressed_size=uncompressed_size,
        application_paths=REQUIRED_APPLICATION_PATHS,
        dependency_packages=tuple(sorted(REQUIRED_DEPENDENCY_PATHS)),
        static_assets=REQUIRED_STATIC_PATHS,
    )


def print_audit_report(report: AuditReport) -> None:
    print(f"Archive: {report.archive}")
    print(f"Member count: {report.member_count}")
    print(f"Compressed size: {report.compressed_size} bytes")
    print(f"Total uncompressed size: {report.uncompressed_size} bytes")
    print("Handler path: src/lambda_handler.py")
    print(f"Required application paths found: {', '.join(report.application_paths)}")
    print(
        "Required dependency packages found: "
        f"{', '.join(report.dependency_packages)}"
    )
    print(f"Static assets found: {', '.join(report.static_assets)}")
    print("Audit: PASS")


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    build_parser = commands.add_parser("build", help="Build the Lambda ZIP")
    build_parser.add_argument("--output", type=Path, required=True)

    audit_parser = commands.add_parser("audit", help="Audit the Lambda ZIP")
    audit_parser.add_argument("--archive", type=Path, required=True)

    return parser


def main(argv: Iterable[str] | None = None) -> int:
    arguments = create_parser().parse_args(argv)

    try:
        if arguments.command == "build":
            output = build_package(arguments.output)
            print(f"Built Lambda archive: {output}")
            return 0

        report = audit_package(arguments.archive)
        print_audit_report(report)
        return 0
    except (PackageBuildError, PackageAuditError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
