call conda create -n jobfree python=3.8
call conda create -n jobfreeSpider python=3.8

call conda activate jobfree
call pip install -r .\web-server\requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
call conda activate jobfreeSpider
call pip install -r .\spiderProject\requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
