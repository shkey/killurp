# killurp [![The MIT License](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)](http://opensource.org/licenses/MIT)

这是一个工具集，将会不断更新各项功能，目的是干掉难用落后反人类的科成 urp

## 安装与配置

- 克隆本项目至本地

    ```bash
    git clone https://github.com/shkey/killurp.git
    ```

- 安装第三方库依赖

    ```bash
    cd killurp
    pip3 install -r requirements.txt
    ```

- 查看使用方法

    ``` bash
    $ python3 killurp.py -h
    usage: killurp.py [-h] [-a ACCOUNT] [-p PASSWORD] [-P PORT] [-z ZKZH]
                    [-n NAME] [-v]
                    {grade,judge,cet}

    一个小工具集，将会不断更新各项功能，目的是干掉难用落后反人类的科成 urp

    positional arguments:
    {grade,judge,cet}     选择你要使用的功能项 -> grade：成绩导出， judge：一键评教， cet：四六级查询

    optional arguments:
    -h, --help            show this help message and exit
    -v, --version         show program's version number and exit

    URP options:
    -a ACCOUNT, --account ACCOUNT
                            你的 URP 账号（也就是学号）
    -p PASSWORD, --password PASSWORD
                            你的 URP 账号的密码
    -P PORT, --port PORT  URP 教务系统开放端口（默认为 80 端口）

    CET options:
    -z ZKZH, --zkzh ZKZH  你的 CET 准考证号
    -n NAME, --name NAME  你的姓名

    有问题或者更好的建议？欢迎来 Github[https://github.com/shkey/killurp] 提 issue 和 PR
    ```

## 示例

- 成绩导出

    ``` bash
    $ python3 killurp.py grade -a ACCOUNT -p PASSWORD -P PORT
    登录成功
    成绩报表导出中...
    成绩报表导出完成，请注意查看
    ```

- 同理，要进行一键评教可按如下操作

    ```bash
    $ python3 killurp.py judge -a ACCOUNT -p PASSWORD -P PORT
    登录成功
    评教中，请稍等...
    XXX评教 评教完成
    XXX评教 评教完成
    XXX评教 评教完成
    程序自动评教完成，请注意自行检查是否真的评教完成～
    ```

- 四六级成绩查询

    ```bash
    $ python3 killurp.py cet -z 123456789012345 -n XX
    请输入验证码：XX
    查询中，请稍等...
    ```

- 最后，其实最简单的使用方法可以不用在功能类型后面加对应的参数，可选择对应功能后直接运行，程序会自动提示你进行相应参数的输入

    ```bash
    $ python3 killurp.py grade
    请输入你的账号：XXXXXXXXXX
    请输入你的密码：XXXXXX
    登录成功
    成绩报表导出中...
    成绩报表导出完成，请注意查看
    ```

## LICENSE

MIT [@shkey](https://github.com/shkey)
