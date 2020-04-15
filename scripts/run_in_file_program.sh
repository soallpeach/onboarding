set -eux
BASE_PATH=$(pwd)
cd workspace/$CHALLENGE_NAME
mkdir data/
cp $BASE_PATH/challenges/$CHALLENGE_NAME/input.txt data/input.txt
COMMAND=$(docker inspect prime --format='{{.ContainerConfig.Entrypoint}}')
CMD=${COMMAND:1:$((${#COMMAND} - 2))} #remove first and last char (long version to work on both Linux and Mac)
docker run --rm -v "$PWD/data/:/data/" --entrypoint="" $CHALLENGE_NAME  sh -c "$CMD /data/input.txt > /data/result.txt"


