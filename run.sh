mkdir workspace && cd workspace

git clone $REPOSITRY_URL
cd $CHALLENGE_NAME
docker build -t $CHALLENGE_NAME .


