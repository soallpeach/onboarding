set -eu
BASE_PATH=$(pwd)

cd workspace/$CHALLENGE_NAME
rm -rf data/
mkdir data/
cp $BASE_PATH/challenges/$CHALLENGE_NAME/input.txt data/in.txt
docker run --rm -v "$PWD/data/:/data/" $CHALLENGE_NAME /data/in.txt /data/out.txt > result.txt
# Make sure old programs that use stdout and new programs using output file works.
if [[ ! -s result.txt && -s data/out.txt ]]; then
  mv data/out.txt result.txt;
fi
