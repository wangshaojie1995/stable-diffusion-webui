from transformers import AutoModel
from huggingface_hub import list_repo_files,hf_hub_download
import os
import shutil

hfModelRepoMap = {
    "/Stable-diffusion": "wsj1995/Checkpoint",
    # "/ScuNET": '',
    # "/SwinIR": "",
    # "/RealESRGAN": "",
    # "/DAT": "",
    # "/HAT": ""
}
# TODO: api运行完成后删除下载的模型
def loadHuggingfaceModel(file_path):
    if os.path.exists(file_path):
        print(f"文件 {file_path} 已存在，跳过下载")
        return
    # repoPath = None
    for pathSuffix in hfModelRepoMap:
        if pathSuffix in file_path:
            # repoPath = f"wsj1995{file_path.split(pathSuffix)[-1]}"
            filename = file_path.split(pathSuffix)[-1][1:]
            print({
                'repo_id':hfModelRepoMap[pathSuffix], 
                'filename':filename,   
                'cache_dir':os.path.dirname(file_path),
            })
            downloadedFilePath = hf_hub_download(
                repo_id=hfModelRepoMap[pathSuffix], 
                filename=filename,   
                # cache_dir=os.path.dirname(file_path),
                token=os.environ.get("HF_TOKEN")
            )
            os.makedirs(os.path.dirname(file_path), exist_ok=True) 
            shutil.move(downloadedFilePath, file_path)
            print(f'模型文件下载完成 {downloadedFilePath} 并移动到 {file_path}')
            print(os.path.exists(file_path))
            print(os.path.exists(downloadedFilePath))
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