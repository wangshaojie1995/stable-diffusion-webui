from transformers import AutoModel
from huggingface_hub import list_repo_files,hf_hub_download
import os

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
        return
    # repoPath = None
    for pathSuffix in hfModelRepoMap:
        if pathSuffix in file_path:
            # repoPath = f"wsj1995{file_path.split(pathSuffix)[-1]}"
            filename = file_path.split(pathSuffix)[-1][1:]
            cacheDir = file_path.replace(filename,'')
            print({
                'repo_id':hfModelRepoMap[pathSuffix], 
                'filename':filename,   
                'cache_dir':os.path.dirname(file_path),
                'cacheDir': cacheDir
            })
            file_path = hf_hub_download(
                repo_id=hfModelRepoMap[pathSuffix], 
                filename=filename,   
                cache_dir=os.path.dirname(file_path),
                token=os.environ.get("HF_TOKEN")
            )
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