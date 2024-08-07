from huggingface_hub import list_repo_files,hf_hub_download
import os
import shutil
import subprocess
import pathlib
import gc

hfModelRepoMap = {
    "/Stable-diffusion": "wsj1995/stable-diffusion-models",
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
    downloaded = False
    print(f'加载模型文件 {file_path}')
    for pathSuffix in hfModelRepoMap:
        if pathSuffix in file_path:
            if os.path.exists(file_path):
                print(f"文件 {file_path} 已存在，跳过下载")
                downloaded = True
            else:
                filename = file_path.split(pathSuffix)[-1][1:]
                pathData = pathlib.Path(file_path)
                DownLoad(f"https://huggingface.co/{hfModelRepoMap[pathSuffix]}/resolve/main/{filename}", pathData.parent, pathData.name)
                print(f'模型文件下载完成 {file_path}')
                downloaded = True
            break
    return downloaded
    

def huggingfaceModelList(model_path):
    fileList = []
    for pathSuffix in hfModelRepoMap:
        if model_path.endswith(pathSuffix):
            fileList = list_repo_files(hfModelRepoMap[pathSuffix], repo_type="model")
            break
    result = []
    for file in fileList:
        result.append(model_path + '/' + file)
    
    print(f'加载模型列表 {model_path}')
    return result