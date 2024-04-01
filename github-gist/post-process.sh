#!/usr/bin/env bash

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

# Debbuging path variables
# printf "${GREEN}path:${NC} ${__path}\ndir: ${__dir}\nbase: ${__base}\n"

# Try to find local version of ffmpeg, defaults to the path used in docker if not found
__ffmpeg="$(which ffmpeg || echo '/usr/lib/jellyfin-ffmpeg/ffmpeg')"

# Change to the directory containing the recording
cd "${__dir}"

# Extract closed captions to external SRT file
printf "[post-process.sh] %bExtracting subtitles...%b\n" "$GREEN" "$NC"
$__ffmpeg -f lavfi -i movie="${__file}[out+subcc]" -map 0:1 "${__base}.srt"

# Transcode to mp4, crf parameter can be adjusted to change output quality
printf "[post-process.sh] %bTranscoding file..%b\n" "$GREEN" "$NC"
$__ffmpeg -i "${__file}" -vcodec libx264 -vf yadif=parity=auto -crf 20 -preset veryslow "${__base}.mp4"

# Remove the original recording file
printf "[post-process.sh] %bRemoving originial file...%b\n" "$GREEN" "$NC"
rm "${__file}"

# Return to the starting directory
cd "${PWD}"