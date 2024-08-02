from transformers import AutoModel
from huggingface_hub import list_repo_files,hf_hub_download
import os
import shutil
import subprocess
import pathlib
import gc

hfModelRepoMap = {
    "/Stable-diffusion": "wsj1995/Checkpoint",
    # "/ScuNET": '',
    # "/SwinIR": "",
    # "/RealESRGAN": "",
    # "/DAT": "",
    # "/HAT": ""
}

def DownLoad(URI:str,DownloadPath:pathlib.Path,DownLoadFileName:str ) -> int:
    if (DownloadPath / DownLoadFileName).is_file(): return 0
    for z in range(10):
        i=subprocess.run([r"aria2c",r"-c",r"-x" ,r"16", r"-s",r"16", r"-k" ,r"1M" ,r"-m",r"0",r"--enable-mmap=false",r"--console-log-level=error",r"-d",str(DownloadPath),r"-o",DownLoadFileName,URI]);
        if(i.returncode == 0 ): 
            del i
            gc.collect()
            return 0
        else :
            del i
        raise Exception(str.format("download \'{0}\' failed",URI))


# TODO: api运行完成后删除下载的模型
def loadHuggingfaceModel(file_path):
    if os.path.exists(file_path):
        print(f"文件 {file_path} 已存在，跳过下载")
        return
    # repoPath = None
    for pathSuffix in hfModelRepoMap:
        if pathSuffix in file_path:
            
            filename = file_path.split(pathSuffix)[-1][1:]
            DownLoad(f"https://huggingface.co/{hfModelRepoMap[pathSuffix]}/{filename}",file_path)
            # repoPath = f"wsj1995{file_path.split(pathSuffix)[-1]}"
            # print({
            #     'repo_id':hfModelRepoMap[pathSuffix], 
            #     'filename':filename,   
            #     'cache_dir':os.path.dirname(file_path),
            # })
            # downloadedFilePath = hf_hub_download(
            #     repo_id=hfModelRepoMap[pathSuffix], 
            #     filename=filename,   
            #     # cache_dir=os.path.dirname(file_path),
            #     token=os.environ.get("HF_TOKEN")
            # )
            # os.makedirs(os.path.dirname(file_path), exist_ok=True) 
            # shutil.move(downloadedFilePath, file_path)
            print(f'模型文件下载完成 {file_path}')
            print(os.path.exists(file_path))
            # print(os.path.exists(downloadedFilePath))
            break
    # if repoPath is None:
    #     return repoPath 
    # model = AutoModel.from_pretrained(repoPath,use_auth_token=os.environ.get("HF_TOKEN"))

    # # 获取模型的状态字典
    # pl_sd = model.state_dict()

    # return pl_sd
    

def huggingfaceModelList(model_path):
    fileList = []
    for pathSuffix in hfModelRepoMap:
        if model_path.endswith(pathSuffix):
            fileList = list_repo_files(hfModelRepoMap[pathSuffix], repo_type="model")
            break
    result = []
    for file in fileList:
        result.append(model_path + '/' + file)
    return result