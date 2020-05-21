set -ex
cd code/$CHALLENGE_NAME
docker build -t $CHALLENGE_NAME .