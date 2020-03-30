set -e
BASE_PATH=$(pwd)
rm -rf  workspace
mkdir workspace && cd workspace
git clone $REPOSITORY_URL $(pwd)
cd $CHALLENGE_NAME
docker build -t $CHALLENGE_NAME .
echo 'Running the test...'
docker run -v $BASE_PATH/challenges/$CHALLENGE_NAME/input.txt:/data/input.txt $CHALLENGE_NAME /data/input.txt  > result.txt
echo 'Test Done...'
diff --strip-trailing-cr -w result.txt $BASE_PATH/challenges/$CHALLENGE_NAME/expected.txt



