#!/user/bin

scp 10.1.7.102:/data/resys/yuanjinwei/Anaconda2-4.2.0-Linux-x86_64.sh ~
sh ~/Anaconda2-4.2.0-Linux-x86_64.sh
CURRENT_FILE_DIR="$(cd "$(dirname "$0")";pwd)"
cd $CURRENT_FILE_DIR
source ./.commonrc
echo $(which python)
pip install scrapy
echo $(which scrapy)
source ./.commonrc

