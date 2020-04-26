set -ex
cd workspace
git clone $REPOSITORY_URL $(pwd)/code
cd code/$CHALLENGE_NAME
docker build -t $CHALLENGE_NAME .