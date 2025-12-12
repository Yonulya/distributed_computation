sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.13 python3.13-venv -y
python3.13 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r ./master/worker/requirements.txt