import os, os.path
import shutil




def copy_files_recursive(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path, exist_ok=True)

    entries = os.listdir(source_dir_path)
    _copy_entry_list(entries, source_dir_path, dest_dir_path)


def _copy_entry_list(entries, source_dir_path, dest_dir_path):
    if not entries:
        return

    head = entries[0]
    tail = entries[1:]

    src_path = os.path.join(source_dir_path, head)
    dst_path = os.path.join(dest_dir_path, head)

    if os.path.isfile(src_path):
        shutil.copy(src_path, dst_path)
    else:
        copy_files_recursive(src_path, dst_path)

    _copy_entry_list(tail, source_dir_path, dest_dir_path)
    
        
    

