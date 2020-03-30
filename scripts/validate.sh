set -e
BASE_PATH=$(pwd)
cd workspace/$CHALLENGE_NAME
diff --strip-trailing-cr -w result.txt $BASE_PATH/challenges/$CHALLENGE_NAME/expected.txt



