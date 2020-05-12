set -eu

DATE_COMMAND="date"

if [[ $(uname -s) == "Darwin" ]]; then
  DATE_COMMAND="gdate"
fi
BASE_PATH=$(pwd)
cd workspace/code/$CHALLENGE_NAME
mkdir data/
cp $BASE_PATH/challenges/$CHALLENGE_NAME/input.txt data/input.txt

set +e
docker container rm "$CHALLENGE_NAME-container" -f &> /dev/null
set -eu

COMMAND=$(docker inspect $CHALLENGE_NAME --format='{{.ContainerConfig.Entrypoint}}')
CMD=${COMMAND:1:$((${#COMMAND} - 2))} #remove first and last char (long version to work on both Linux and Mac)
docker run --name "$CHALLENGE_NAME-container" -v "$PWD/data/:/data/" --entrypoint="" $CHALLENGE_NAME  sh -c "$CMD /data/input.txt > /data/result.txt"

START_DATE=$(docker inspect --format='{{.State.StartedAt}}' "$CHALLENGE_NAME-container")
STOP_DATE=$(docker inspect --format='{{.State.FinishedAt}}' "$CHALLENGE_NAME-container")

START_TIMESTAMP=$($DATE_COMMAND --date=$START_DATE +'%s.%3N')
STOP_TIMESTAMP=$($DATE_COMMAND --date=$STOP_DATE +'%s.%3N')

docker container rm "$CHALLENGE_NAME-container" &> /dev/null

echo "::::DURATION="$(bc <<< "$STOP_TIMESTAMP - $START_TIMESTAMP")

