chcp 65001

@echo off


echo "如果出现Fully automatic, cached. Proceed and download? [Yes]/No 提示，请输入yes并按回车键"
echo 进行过程中，按Ctrl+C取消
choice /M 请认真阅读以上文字，输入Y回车继续

Cd /d %~dp0

call gsrenv\Scripts\activate.bat

pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip config set install.trusted-host mirrors.aliyun.com

pip install nuitka
pip install -r requirements.txt

call nuitka ^
--mingw64 ^
--standalone ^
--windows-disable-console ^
--output-dir=out ^
--show-progress ^
--windows-icon-from-ico=logo.ico ^
--windows-company-name=玄云海网络工作室 ^
--windows-product-name=GSR ^
--windows-file-version=2.0.0 ^
--windows-product-version=2.0.0 ^
--windows-file-description=GSR，是一个本地文件自动同步到Git仓库的Python程序。 ^
 main.py ^

yes

choice /M 完成，按任意键退出
exit