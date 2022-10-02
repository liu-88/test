--------------目录说明--------------------
# common目录用于存放通用的相关脚本文件
    -- config.py : 用于操作配置文件，对配置文件进行读取、删除、添加等操作,这里操作的
    文件是conf\test.ini
    -- logUtil.py: 用于日志操作，因为我们用的是Pytest自带的日志管理方式，这里的日志相关代码实际并
    未使用，只是在其中定义了一个单例的日志对象，以便在其它地方引用，原有代码已被注释，以作后续参考
    -- do_excel.py: 用于从excel.xlsx文件中读取和写入测试用例数据

# conf目录用于存放配置文件文本，主要是test.ini配置文件，是与测试用例数据相关的配置文件
    -- test.ini:用于配置测试数据，可通过config.py 对其进行增、删、改、查

# datas目录用于存放测试数据
    -- case.xlsx 存放测试用例数据的文件

# logs 目录用于存放日志文件

# pytest_at_venv python虚拟环境

# conftest.py pytest的固定文件，用于存放一些全局共享的代码，一般配合夹具使用

# requirements.txt 描述需要导入的第三方包可通过 pip install -r requirements.txt 命令
一次性导入