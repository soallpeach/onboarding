set -x
df -h
rm -rf workspace
docker image prune -a -f
df -h