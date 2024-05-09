import requests
import json
import subprocess
import os

output_folder = "Output"
# True = keep audio/video files separate and False = keep only the merged file
keep_raw_files = False


def downloadFile(link, file_name):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
    }
    try:
        resp = requests.get(link, headers=headers).content
    except:
        print("Failed to open {}".format(link))
        return
    with open(os.path.join(output_folder, file_name), 'wb') as f:
        f.write(resp)


def downloadVideo(link):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Dnt': '1',
        'Dpr': '1.3125',
        'Priority': 'u=0, i',
        'Sec-Ch-Prefers-Color-Scheme': 'dark',
        'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'Sec-Ch-Ua-Full-Version-List': '"Chromium";v="124.0.6367.156", "Google Chrome";v="124.0.6367.156", "Not-A.Brand";v="99.0.0.0"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Model': '""',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Ch-Ua-Platform-Version': '"15.0.0"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Viewport-Width': '1463'
    }
    try:
        resp = requests.get(link, headers=headers).text
    except:
        print("Failed to open {}".format(link))
        return
    splits = link.split('/')
    video_id = ''
    for ids in splits:
        if ids.isdigit():
            video_id = ids
    target_video_audio_id = resp.split('"id":"{}"'.format(video_id))[1].split(
        '"dash_prefetch_experimental":[')[1].split(']')[0].strip()
    list_str = "[{}]".format(target_video_audio_id)
    sources = json.loads(list_str)
    video_link = resp.split('"representation_id":"{}"'.format(sources[0]))[
        1].split('"base_url":"')[1].split('"')[0]
    video_link = video_link.replace('\\', '')
    print(video_link)
    audio_link = resp.split('"representation_id":"{}"'.format(sources[1]))[
        1].split('"base_url":"')[1].split('"')[0]
    audio_link = audio_link.replace('\\', '')
    print(audio_link)
    print("Downloading video...")
    downloadFile(video_link, 'video.mp4')
    print("Downloading audio...")
    downloadFile(audio_link, 'audio.mp4')
    print("Merging files...")
    video_path = os.path.join(output_folder, 'video.mp4')
    audio_path = os.path.join(output_folder, 'audio.mp4')
    combined_file_path = os.path.join(output_folder, 'merged_final.mp4')
    cmd = 'ffmpeg -hide_banner -loglevel error -i "{}" -i "{}" -c copy "{}"'.format(
        video_path, audio_path, combined_file_path)
    subprocess.call(cmd, shell=True)
    os.remove(os.path.join(output_folder, 'video.mp4'))
    os.remove(os.path.join(output_folder, 'audio.mp4'))
    os.rename(os.path.join(output_folder, 'merged_final.mp4'),
              os.path.join(output_folder, '{}.mp4'.format(video_id)))


if __name__ == "__main__":
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    downloadVideo(input("Enter the video URL: "))
    print("Done! Please check in the {} folder".format(output_folder))
