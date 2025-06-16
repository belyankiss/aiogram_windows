FILE_CACHE = {}

def use_cache(file_path: str, file_id: str = None):
    if file_id:
        FILE_CACHE[file_path] = file_id
    return FILE_CACHE.get(file_path)