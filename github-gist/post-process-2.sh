#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset
# set -o xtrace

PWD="$(pwd)"

die () {
	echo >&2 "$@"
	cd "${PWD}"
	exit 1
}

# Colors
GREEN='\033[0;32m'
NC='\033[0m' # No Color

__path="${1:-}"

# verify a path was provided
[ -n "$__path" ] || die "path is required"
# verify the path exists
[ -f "$__path" ] || die "path ($__path) is not a file"

__dir="$(dirname "${__path}")"
__file="$(basename "${__path}")"
__base="$(basename "${__path}" ".ts")"

# Try to find local version of ffmpeg, defaults to the path used in docker if not found
__ffmpeg="$(which ffmpeg || echo '/usr/local/bin/ffmpeg')"

# Change to the directory containing the recording
cd "${__dir}"

# Transcode to mp4
printf "[post-process.sh] %bTranscoding file..%b\n" "$GREEN" "$NC"
$__ffmpeg -i "${__file}" -vcodec h264 -acodec aac "${__base}.mp4" -report

# Remove the original recording file
slackSend "[${__base}] Moving originial file to postProcessBAK folder"
printf "[post-process.sh] %bRenaming originial file...%b\n" "$GREEN" "$NC"
# rm "${__file}"

# Return to the starting directory
cd "${PWD}"