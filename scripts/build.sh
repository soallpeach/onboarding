set -ex
cd workspace/code/$CHALLENGE_NAME
docker build -t $CHALLENGE_NAME .