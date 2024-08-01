from transformers import AutoModel,hf_hub_download
from huggingface_hub import list_repo_files
import os

hfModelRepoMap = {
    "/Stable-diffusion": "wsj1995/Checkpoint",
    # "/ScuNET": '',
    # "/SwinIR": "",
    # "/RealESRGAN": "",
    # "/DAT": "",
    # "/HAT": ""
}
def loadHuggingfaceModel(file_path):
    # repoPath = None
    for pathSuffix in hfModelRepoMap:
        if pathSuffix in file_path:
            # repoPath = f"wsj1995{file_path.split(pathSuffix)[-1]}"
            filename = file_path.split(pathSuffix)[-1]
            print({
                'repo_id':hfModelRepoMap[pathSuffix], 
                'filename':filename,   
                'cache_dir':file_path.replace(filename,'')
            })
            file_path = hf_hub_download(
                repo_id=hfModelRepoMap[pathSuffix], 
                filename=filename,   
                cache_dir=file_path.replace(filename,'')
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