url=""
fn=".mp4"

curl --continue-at - \
    --progress-bar \
    --output $fn $url

