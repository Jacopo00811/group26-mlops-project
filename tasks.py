import os

from invoke import Context, task

WINDOWS = os.name == "nt"
PROJECT_NAME = "danish_to_english_llm"
PYTHON_VERSION = "3.11"


# Setup commands
@task
def create_environment(ctx: Context) -> None:
    """Create a new conda environment for project."""
    ctx.run(
        f"uv venv {PROJECT_NAME} python={PYTHON_VERSION}",
        echo=True,
        pty=not WINDOWS,
    )


@task
def requirements(ctx: Context) -> None:
    """Install project requirements."""
    ctx.run("pip install -r requirements.txt", echo=True, pty=not WINDOWS)
    ctx.run("pip install -e .", echo=True, pty=not WINDOWS)


@task(requirements)
def dev_requirements(ctx: Context) -> None:
    """Install development requirements."""
    ctx.run('pip install -e .["dev"]', echo=True, pty=not WINDOWS)


@task(requirements)
def api_requirements(ctx: Context) -> None:
    ctx.run("pip install -r requirements_frontend.txt", echo=True, pty=not WINDOWS)
    ctx.run("pip install -r requirements_backend.txt", echo=True, pty=not WINDOWS)


@task
def train(ctx: Context, config_path: str = "../../configs", config_name: str = "config.yaml") -> None:
    """Train model."""
    ctx.run(
        f"python src/{PROJECT_NAME}/train.py --config-path {config_path} --config-name {config_name}",
        echo=True,
        pty=not WINDOWS,
    )


@task
def test(ctx: Context) -> None:
    """Run tests."""
    ctx.run("coverage run -m pytest tests/unit_tests", echo=True, pty=not WINDOWS)
    ctx.run("coverage report -m", echo=True, pty=not WINDOWS)


@task
def docker_build(ctx: Context, progress: str = "plain") -> None:
    """Build docker images."""
    ctx.run(
        f"docker build -t train:latest . -f dockerfiles/train.dockerfile --progress={progress}",
        echo=True,
        pty=not WINDOWS,
    )
    ctx.run(
        f"docker build -t api:latest . -f dockerfiles/api.dockerfile --progress={progress}", echo=True, pty=not WINDOWS
    )
    ctx.run(
        f"docker build -t front_api:latest . -f dockerfiles/front_api.dockerfile --progress={progress}",
        echo=True,
        pty=not WINDOWS,
    )


# Documentation commands
@task(dev_requirements)
def build_docs(ctx: Context) -> None:
    """Build documentation."""
    ctx.run("mkdocs build --config-file mkdocs.yml --site-dir build", echo=True, pty=not WINDOWS)


@task(dev_requirements)
def serve_docs(ctx: Context) -> None:
    """Serve documentation."""
    ctx.run("mkdocs serve --config-file mkdocs.yml", echo=True, pty=not WINDOWS)
