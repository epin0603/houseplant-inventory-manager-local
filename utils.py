import os
import shutil

def save_image(file_path):
    assets_dir = os.path.join(os.getcwd(), 'assets', 'progressImages')
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
    new_path = os.path.join(assets_dir, os.path.basename(file_path))
    shutil.copy(file_path, new_path)
    return new_path