set -x
df -h
docker image prune -a -f
df -h