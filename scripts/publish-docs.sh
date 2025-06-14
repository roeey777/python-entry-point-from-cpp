#! /bin/bash

# ******************************************************************
# This script is intended for publishing the generated easily onto
# github pages (commit on gh-pages branch).
#
# Used the following formatter for formatting this code, like this:
# $ shfmt -i 4 -ci -sr --language-dialect bash <path to file>
#
# Validated using shellcheck as a static analyzer, like this:
# $ shellcheck --shell=bash <path to file>
#
# Both tools can be installed via conda, like this:
# $ conda install -c conda-forge go-shfmt    # for shfmt.
# $ conda install -c conda-forge shellcheck  # for shellcheck.
#
# ******************************************************************

CMAKE_BUILD_DIR="build/docs"
DOCS_BUILD_DIR="docs/build"
DEFAULT_BRANCH="master"
GIT_REMOTE_NAME="${1:-github}"
GITHUB_PAGES_BRANCH="gh-pages"
COMMIT_ID="$(git rev-parse "${DEFAULT_BRANCH}")"
COMMIT_MSG="Documentation for commit ${COMMIT_ID}"
CONDA_ENVIRONMENT_NAME="poc"

function copy_to_build_dir() {
    mkdir -p "${DOCS_BUILD_DIR}"
    cp -r build/docs/docs/docs/sphinx/* "${DOCS_BUILD_DIR}"
}

function activate_conda() {
    CONDA_BASE="$(conda info --base)"
    export CONDA_BASE
    # shellcheck disable=SC1091  # don't follow up on conda ...
    source "${CONDA_BASE}"/etc/profile.d/conda.sh
    conda activate "${CONDA_ENVIRONMENT_NAME}"
}

function build_docs() {
    activate_conda
    cmake -S . -B "${CMAKE_BUILD_DIR}" -Wdev -Werror=dev -DENABLE_DOCS=ON -DENABLE_TESTING=OFF
    cmake --build "${CMAKE_BUILD_DIR}" --target Sphinx
}

function clean_docs() {
    if [ -d "${DOCS_BUILD_DIR}" ]; then
        rm -r "${DOCS_BUILD_DIR}"
    elif [ -e "${DOCS_BUILD_DIR}" ]; then
        echo "${DOCS_BUILD_DIR} exists AND it's not a file! Please remove it manually."
        exit 1
    fi
}

function handle_worktree() {
    path_to_possible_worktree="$(realpath "${DOCS_BUILD_DIR}")"

    if git worktree list --porcelain | grep -q "^worktree ${path_to_possible_worktree}\$"; then
        echo "${DOCS_BUILD_DIR} is already a worktree, re-adding it."
        git worktree remove "${DOCS_BUILD_DIR}"
    else
        echo "${DOCS_BUILD_DIR} is not a worktree."
    fi

    git worktree add "${DOCS_BUILD_DIR}" "${GITHUB_PAGES_BRANCH}"
}

function publish_docs() {
    build_docs
    copy_to_build_dir

    # Use a ( sub-shell ) to avoid having to cd back. (shellcheck SC2103)
    (
        cd "${DOCS_BUILD_DIR}" || exit
        git add --all .
        git commit --allow-empty --signoff -m "${COMMIT_MSG}"
        git push "${GIT_REMOTE_NAME}" "${GITHUB_PAGES_BRANCH}"
    )
}

function usage() {
    echo "Usage: $0 [git remote name]"
    echo
    echo "If [git remote name] is provided, it will be used as the git remote when publishing the docs onto gh-pages."
    echo "If not provided, 'origin' will be used."
    echo
    echo "Options:"
    echo "  -h, --help    Show this help message and exit"
    exit 0
}

function main() {
    if [[ "$1" == "-h" || "$1" == "--help" ]]; then
        usage
    fi

    clean_docs
    handle_worktree
    publish_docs
}

main "$@"
