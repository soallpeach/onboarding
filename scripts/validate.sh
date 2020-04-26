set -e
BASE_PATH=$(pwd)
cd workspace/code/$CHALLENGE_NAME/data
diff --strip-trailing-cr -w result.txt $BASE_PATH/challenges/$CHALLENGE_NAME/expected.txt



