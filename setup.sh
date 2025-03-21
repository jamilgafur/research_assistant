apt update -y
apt upgrade -y
apt-get install curl -y
pip install -q kokoro>=0.9.2 soundfile
apt-get -qq -y install espeak-ng > /dev/null 2>&1
pip install 'markitdown[all]~=0.1.0a1'
pip install pydub
apt install ffmpeg
pip install nltk
pip install ushlex
curl -fsSL https://ollama.com/install.sh | sh