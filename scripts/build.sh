set -e
BASE_PATH=$(pwd)
rm -rf  workspace
mkdir workspace && cd workspace
git clone $REPOSITORY_URL $(pwd)
cd $CHALLENGE_NAME
docker build -t $CHALLENGE_NAME .