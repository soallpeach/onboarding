set -e
rm -rf  workspace
mkdir workspace && cd workspace
git clone $REPOSITRY_URL $(pwd)
cd $CHALLENGE_NAME
docker build -t $CHALLENGE_NAME .
docker run $CHALLENGE_NAME


