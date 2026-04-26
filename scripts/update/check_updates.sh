#!/usr/bin/env bash
set -euo pipefail

REMOTE="${1:-origin}"
BRANCH="${2:-main}"
STATUS_FILE="update_status.json"

version="unknown"
if [ -f VERSION ]; then
  version="$(tr -d '\n' < VERSION)"
fi

current_branch="$(git branch --show-current 2>/dev/null || echo unknown)"
current_commit="$(git rev-parse --short HEAD 2>/dev/null || echo unknown)"
worktree_status="$(git status --short 2>/dev/null || true)"

if [ -n "$worktree_status" ]; then
  dirty="true"
else
  dirty="false"
fi

echo "Pantheon OS update check"
echo "Version: $version"
echo "Current branch: $current_branch"
echo "Current commit: $current_commit"
echo "Remote target: $REMOTE/$BRANCH"

git fetch "$REMOTE" "$BRANCH" >/tmp/pantheon_update_fetch.log 2>&1 || {
  cat /tmp/pantheon_update_fetch.log
  cat > "$STATUS_FILE" <<EOF
{
  "version": "$version",
  "branch": "$current_branch",
  "commit": "$current_commit",
  "remote": "$REMOTE/$BRANCH",
  "status": "error",
  "message": "git fetch failed"
}
EOF
  exit 1
}

remote_ref="$REMOTE/$BRANCH"
behind_count="$(git rev-list --count HEAD.."$remote_ref" 2>/dev/null || echo 0)"
ahead_count="$(git rev-list --count "$remote_ref"..HEAD 2>/dev/null || echo 0)"

if [ "$dirty" = "true" ]; then
  update_status="blocked_dirty_worktree"
elif [ "$behind_count" -gt 0 ]; then
  update_status="update_available"
else
  update_status="up_to_date"
fi

echo "Dirty worktree: $dirty"
echo "Behind remote: $behind_count"
echo "Ahead remote: $ahead_count"
echo "Status: $update_status"

pending_commits="$(git log --oneline HEAD.."$remote_ref" 2>/dev/null | sed 's/"/\\"/g' || true)"

cat > "$STATUS_FILE" <<EOF
{
  "version": "$version",
  "branch": "$current_branch",
  "commit": "$current_commit",
  "remote": "$remote_ref",
  "dirty_worktree": $dirty,
  "behind_count": $behind_count,
  "ahead_count": $ahead_count,
  "status": "$update_status",
  "pending_commits": $(printf '%s\n' "$pending_commits" | python3 -c 'import json,sys; print(json.dumps([line for line in sys.stdin.read().splitlines() if line]))')
}
EOF

echo "Update status written to $STATUS_FILE"
