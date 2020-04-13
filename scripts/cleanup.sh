set -x
df -h
rm -rf workspace
docker system prune -a
df -h