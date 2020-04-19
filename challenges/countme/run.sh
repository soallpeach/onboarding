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

docker run -d --name "$CHALLENGE_NAME-container" -p "8080:80" $CHALLENGE_NAME

echo "GET http://localhost:8080" | vegeta  -cpus 1 attack -rate 100   -duration=2s  | vegeta report -type=json | jq '.' > metrics.json
cat metrics.json
echo "::::METRICS="$(cat metrics.json)

