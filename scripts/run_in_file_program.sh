set -e
BASE_PATH=$(pwd)
cd workspace/$CHALLENGE_NAME
docker run -v $BASE_PATH/challenges/$CHALLENGE_NAME/input.txt:/data/input.txt $CHALLENGE_NAME /data/input.txt  > result.txt
