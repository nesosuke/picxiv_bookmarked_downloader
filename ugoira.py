import glob
import os
import shutil
import json
from PIL import Image


def fetch_ugoira_frames(api, id, metadata, save_dir):
    meta_ugoira = api.ugoira_metadata(id)
    if meta_ugoira.error:
        return None

    ugoira_dir = save_dir+'/'+str(id)+'_ugoira'
    if not os.path.exists(ugoira_dir):
        os.mkdir(ugoira_dir)

    frames_url = meta_ugoira.ugoira_metadata.zip_urls.medium
    frames_meta = meta_ugoira.ugoira_metadata.frames
    delay = meta_ugoira.ugoira_metadata.frames[0].delay
    api.download(frames_url, path=ugoira_dir)

    # Extract zip
    zip_path = glob.glob(ugoira_dir+'/*.zip')[0]
    shutil.unpack_archive(zip_path, ugoira_dir)

    # combibe frames
    gif = []
    for i, frame in enumerate(frames_meta):
        gif.append(Image.open(ugoira_dir+'/'+str(frame.file)))

    filename = metadata.user.account+'_' + str(id) + '.gif'
    gif[0].save(save_dir+'/'+filename, save_all=True,
                append_images=gif[1:], duration=delay, loop=0)

    # Delete ugoira dir
    shutil.rmtree(ugoira_dir)
