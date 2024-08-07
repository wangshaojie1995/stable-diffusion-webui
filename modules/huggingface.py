import os
import json

hfDownloadFolder = '/dev/shm'
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