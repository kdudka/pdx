# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 The PDX Project Authors

"""Podman helpers for running the Qdrant container used by pdx."""

import os
import subprocess

QDRANT_IMAGE = "docker.io/qdrant/qdrant"
QDRANT_CONTAINER_NAME = "pdx-qdrant"
QDRANT_PORT = "6333:6333"


def get_qdrant_storage_path() -> str:
    """Return the pdx data directory under XDG data home (e.g. ~/.local/share/pdx)."""
    xdg_data = os.environ.get(
        "XDG_DATA_HOME", os.path.join(os.path.expanduser("~"), ".local", "share")
    )
    return os.path.join(xdg_data, "pdx", "qdrant")


def start() -> str:
    """Start the Qdrant container. Returns a message to display. Raises on failure."""
    storage = get_qdrant_storage_path()
    os.makedirs(storage, exist_ok=True)
    storage_volume = f"{os.path.abspath(storage)}:/qdrant/storage:z"

    r = subprocess.run(
        ["podman", "inspect", "--type", "container", QDRANT_CONTAINER_NAME],
        capture_output=True,
    )
    if r.returncode == 0:
        subprocess.run(["podman", "start", QDRANT_CONTAINER_NAME], check=True)
        return f"Started existing container {QDRANT_CONTAINER_NAME}."
    subprocess.run(
        [
            "podman",
            "run",
            "-d",
            "--name",
            QDRANT_CONTAINER_NAME,
            "-p",
            QDRANT_PORT,
            "-v",
            storage_volume,
            QDRANT_IMAGE,
        ],
        check=True,
    )
    return f"Started new container {QDRANT_CONTAINER_NAME} (storage: {storage})."


def stop() -> tuple[bool, str]:
    """Stop the Qdrant container. Returns (success, message)."""
    r = subprocess.run(
        ["podman", "stop", QDRANT_CONTAINER_NAME],
        capture_output=True,
        text=True,
    )
    if r.returncode == 0:
        return True, f"Stopped {QDRANT_CONTAINER_NAME}."
    if "no container with name" in (r.stderr or "").lower():
        return False, f"Container {QDRANT_CONTAINER_NAME} is not running."
    return False, r.stderr or "Failed to stop container."


def logs(follow: bool = False) -> None:
    """Show logs of the Qdrant container. Raises on failure."""
    args = ["podman", "logs", QDRANT_CONTAINER_NAME]
    if follow:
        args.append("--follow")
    subprocess.run(args, check=True)
