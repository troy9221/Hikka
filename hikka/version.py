"""Represents current userbot version"""
# ©️ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# 🌐 https://github.com/troy9221/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

__version__ = (1, 6, 4)

import os

import git

STABLE_BRANCHES = frozenset({"master", "main"})


def detect_branch() -> str:
    """Return the current git branch, defaulting to ``main``."""
    try:
        repo = git.Repo(
            path=os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        )
        if not repo.head.is_detached:
            return repo.active_branch.name
        for name in ("main", "master"):
            if name in repo.heads:
                return name
    except Exception:
        pass
    return "main"


branch = detect_branch()
