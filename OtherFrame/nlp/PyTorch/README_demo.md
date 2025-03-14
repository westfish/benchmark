# NGC PyTorch 性能复现
## 本readme仅为示例,相关内容请勿更新到此, NLP_demo也仅为示例
## 目录 

├── PrepareEnv.sh   # 竞品PyTorch运行环境搭建  
├── README.md       # 运行文档  
├── models          # 提供竞品PyTorch框架的修改后的模型,官方模型请直接在脚本中拉取,统一方向的模型commit应一致,如不一致请单独在模型运行脚本中写明运行的commit  
├── run_PyTorch.sh  # 全量竞品PyTorch框架模型运行脚本  
└── scripts         # 提供各个模型复现性能的脚本  
## 环境介绍
### 1.物理机环境
- 单机（单卡、8卡）
  - 系统：CentOS release 7.5 (Final)
  - GPU：Tesla V100-SXM2-32GB * 8
  - CPU：Intel(R) Xeon(R) Gold 6271C CPU @ 2.60GHz * 80
  - Driver Version: 460.27.04
  - 内存：629 GB
  - CUDA、cudnn Version: cuda10.1-cudnn7 、 cuda11.2-cudnn8-gcc82
- 多机（32卡） TODO
### 2.Docker 镜像,如:

NGC PyTorch 的代码仓库提供了自动构建 Docker 镜像的 [Dockerfile](https://github.com/NVIDIA/DeepLearningExamples/blob/master/PyTorch/Translation/Transformer/Dockerfile)，

- **镜像版本**: `nvcr.io/nvidia/pytorch:20.06-py3`   # 竞品镜像,每个方向的请一致
- **PyTorch 版本**: `1.6.0a0+9907a3e`  # 竞品版本：最新稳定版本，如需特定版本请备注说明原因  
- **CUDA 版本**: `11.2`
- **cuDnn 版本**: `8.0.1`

## 测试步骤
```bash
bash run_PyTorch.sh;     # 创建容器,在该标准环境中测试模型   
```
脚本内容,如:
```bash
#!/usr/bin/env bash
# 拉镜像
ImageName=  ;
docker pull ${ImageName}
# 启动镜像后测试单个模型
run_cmd="bash PrepareEnv.sh;
        cd /workspace/models/NLP/nlp_modelName/;
        cp /workspace/scripts/NLP/nlp_modelName/preData.sh ./;
        cp /workspace/scripts/NLP/nlp_modelName/run_benchmark.sh ./;
        cp /workspace/scripts/NLP/nlp_modelName/analysis_log.py ./;
        CUDA_VISIBLE_DEVICES=0 bash run_benchmark.sh sp 32 fp32 500;
        CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 bash run_benchmark.sh sp 64 fp16 500;
        "
# 启动镜像
nvidia-docker run --name test_torch -it  \
    --net=host \
    --shm-size=1g \
    -v $PWD:/workspace \
    ${ImageName}  /bin/bash -c "${run_cmd}"

```
## 单个模型脚本目录

└── nlp_modelName              # 模型名  
    ├── README.md              # 运行文档  
    ├── analysis_log.py        # log解析脚本,每个框架尽量统一,可参考[paddle的analysis.py](https://github.com/mmglove/benchmark/blob/jp_0907/scripts/analysis.py)  
    ├── logs                   # 训练log,注:log中不得包含机器ip等敏感信息  
    │   ├── index              # log解析后待入库数据json文件   
    │   │   ├── nlp_modelName_sp_bs32_fp32_1_speed  # 单卡数据  
    │   │   └── nlp_modelName_mp_bs32_fp32_8_speed  # 8卡数据  
    │   └── train_log          # 原始训练log  
    ├── preData.sh             # 数据处理  
    └── run_benchmark.sh       # 运行脚本（包含性能、收敛性）  

## 输出

每个模型case需返回log解析后待入库数据json文件

```bash
{
"log_file": "/logs/2021.0906.211134.post107/train_log/ResNet101_bs32_1_1_sp", \    # log 目录,创建规范见PrepareEnv.sh 
"model_name": "clas_MobileNetv1_bs32_fp32", \    # 模型case名,创建规范:repoName_模型名_bs${bs_item}_${fp_item} 如:clas_MobileNetv1_bs32_fp32
"mission_name": "图像分类", \     # 模型case所属任务名称，具体可参考scripts/config.ini      
"direction_id": 0, \            # 模型case所属方向id,0:CV|1:NLP|2:Rec 具体可参考benchmark/scripts/config.ini    
"run_mode": "sp", \             # 单卡:sp|多卡:mp
"index": 1, \                   # 速度验证默认为1
"gpu_num": 1, \                 # 1|8
"FINAL_RESULT": 197.514, \      # 速度计算后的平均值,需要skip掉不稳定的前几步值
"JOB_FAIL_FLAG": 0, \           # 该模型case运行0:成功|1:失败
"UNIT": "images/s" \            # 速度指标的单位 
}

```



