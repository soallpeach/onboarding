set -ex
cd workspace
git clone --quiet  $REPOSITORY_URL $(pwd)/code
cd code/$CHALLENGE_NAME
git log -1 --pretty="tformat:%H,%s"