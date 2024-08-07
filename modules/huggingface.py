from huggingface_hub import list_repo_files,hf_hub_download
import os
import json
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
hfDownloadFolder = '/dev/shm'
listCacheKey = 'model-list'
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
    downloadedFilePath = file_path
    print(f'加载模型文件 {file_path}')
    for pathSuffix in hfModelRepoMap:
        if pathSuffix in file_path:
            if os.path.exists(file_path):
                print(f"文件 {file_path} 已存在，跳过下载")
            else:
                filename = file_path.split(pathSuffix)[-1][1:]
                pathData = pathlib.Path(file_path)
                saveFolder = f"{hfDownloadFolder}{pathSuffix}"
                current_size = get_directory_size(saveFolder)
                size_limit = 10737418240
                if current_size > size_limit:
                    clean_directory(saveFolder, size_limit)
                DownLoad(f"https://huggingface.co/{hfModelRepoMap[pathSuffix]}/resolve/main/{filename}", pathData.parent, pathData.name)
                print(f'模型文件下载完成 {file_path}')
                downloadedFilePath = True
            break
    return downloadedFilePath
    

def huggingfaceModelList(model_path, output,ext_filter, ext_blacklist):
    model_lists = os.environ.get('MODEL_LISTS')
    if model_lists:
        model_lists = json.loads(model_lists)
    else:
        model_lists = {}
    result = []
    for pathSuffix in model_lists:
        if model_path.endswith(pathSuffix):
            fileList = model_lists[pathSuffix]
            folder = f"{hfDownloadFolder}{pathSuffix}"
            for file in fileList:
                result.append(f"{folder}/{file}")
            break
    return result
# def huggingfaceModelList(model_path, output,ext_filter, ext_blacklist):
#     fileList = []
#     result = []
#     matchedPathSuffix = ''
#     existing_cache = cache(listCacheKey)
#     for pathSuffix in hfModelRepoMap:
#         if model_path.endswith(pathSuffix):
#             matchedPathSuffix = pathSuffix
#             cacheData = existing_cache.get(pathSuffix)
#             if cacheData:
#                 print('缓存读取 modelList')
#                 result = cacheData
#             else:
#                 fileList = list_repo_files(hfModelRepoMap[pathSuffix], repo_type="model")
#                 folder = f"{hfDownloadFolder}{matchedPathSuffix}"
#                 os.makedirs(folder, exist_ok=True)
#                 for file in fileList:
#                     full_path = f"{folder}/{file}"
#                     if ext_filter is not None:
#                         _, ext = os.path.splitext(file)
#                         if ext.lower() not in ext_filter:
#                             continue
#                     if ext_blacklist is not None and any(full_path.endswith(x) for x in ext_blacklist):
#                         continue
#                     if full_path not in output:
#                         result.append(full_path)
#                         # 直接返回http连接还是需要手动下载，sd不会自动下载
#                         # result.append(f"https://huggingface.co/{hfModelRepoMap[pathSuffix]}/resolve/main/{file}?download=true")
                
#                 existing_cache[pathSuffix] = result
#             break
#     return result



def get_directory_size(directory):
    """计算目录的总大小（字节）"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size

def get_files_by_creation_time(directory):
    """获取按创建时间排序的文件列表"""
    files = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            creation_time = os.path.getctime(filepath)
            files.append((filepath, creation_time))
    # 按创建时间排序（旧的在前）
    files.sort(key=lambda x: x[1])
    return files

def clean_directory(directory, size_limit):
    """清理目录，直到目录大小小于指定阈值"""
    while get_directory_size(directory) > size_limit:
        files = get_files_by_creation_time(directory)
        if not files:
            print("目录已空，无法继续删除文件。")
            break
        # 删除最早的文件
        oldest_file = files[0][0]
        try:
            os.remove(oldest_file)
            print(f"删除文件：{oldest_file}")
        except Exception as e:
            print(f"无法删除文件 {oldest_file}：{e}")