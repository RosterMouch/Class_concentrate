### 如何部署Triton Inference Sever
关于如何部署[NVIDIA Triton Inference Sever](https://www.nvidia.cn/gpu-cloud/ngc-nvidia-triton/)，详情可参考[该文章](https://blog.csdn.net/Deaohst/article/details/128789824?spm=1001.2014.3001.5501)
![Triton-Stack](https://www.nvidia.cn/content/dam/en-zz/Solutions/cloud/triton/simplified-model-deployment-r2_mobile-300.svg)

#### 克隆当前仓库
```bash
git clone -b infercen-server https://github.com/RosterMouch/Class_concentrate.git
```

#### 切换至推理服务路径
```bash
cd inference-server
```
我们会得到如下的文件结构
```
.
├── README.md
├── bin
│   ├── runSever
│   └── stopServer
├── logs
│   ├── 2023-02-01-13:12:28.124181.log
│   ├── 2023-02-01-14:14:52.183175.log
│   ├── 2023-02-01-14:15:28.159916.log
│   ├── 2023-02-01-14:16:57.279093.log
│   ├── 2023-02-01-14:18:53.213792.log
│   ├── 2023-02-01-14:19:34.923177.log
│   ├── 2023-02-01-14:25:44.678500.log
│   ├── 2023-02-01-14:28:26.259226.log
│   ├── 2023-02-01-16:48:36.log
│   ├── 2023-02-01-18:11:31.log
│   ├── 2023-02-01-18:13:25.log
│   ├── 2023-02-01-18:18:57.log
│   └── 2023-02-01-18:23:19.log
├── model_repository
│   └── action_trt
│       ├── 1
│       │   └── model.plan
│       ├── config.pbtxt
│       └── labels.txt
└── src
    ├── makefile
    ├── pstream.h
    ├── runSever.cc
    └── stopServer.cc

6 directories, 23 files
```

#### 关于模型描述
通过观察观察文件树，你可以很清楚的观察到：Triton在启动时需要指定一个模型仓库，而每个模型仓库下对应的是包含了模型文件以及版本号，模型配置信息等一系列数据的文件夹。
参考本例中的模型结构，可自行添加可供Triton使用的模型。

#### 启动Triton Inference Sever
```bash
cd ./bin
./runSever 1
```
其中1代表Triton Inference Sever将启动在GPU模式下，反之为0则代表启动在CPU Only模式，该参数在启动时必须指定，否则无法启动Triton Sever，报错如下：
```bash
[ERROR] Expecting args length 2,but got : 1,determine shutdown the process.
```