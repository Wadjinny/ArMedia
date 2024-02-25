import subprocess
from pathlib import Path


def add_subtitles_to_video(video_file:Path, srt_files:list[Path]):
    output_file = Path(str(video_file) + ".temp.mp4")
    command = [
        "ffmpeg",
        "-y",
        "-i",
        video_file,
    ]

    for i, srt_file in enumerate(srt_files):
        command.extend(["-i", srt_file])
    command.extend(
        [
            "-c:v",
            "copy",
            "-c:a",
            "copy",
            "-c:s",
            "mov_text",
            "-map",
            "0:v",
            "-map",
            "0:a",
        ]
    )
    for i, srt_file in enumerate(srt_files):
        command.extend(["-map", str(i + 1)])

    for i, srt_file in enumerate(srt_files):
        command.extend(
            ["-metadata:s:s:{}".format(i), "title={}".format(srt_file.stem)]
        )
    command.extend(
        [
            output_file,
        ]
    )
    try:
        subprocess.run(command, check=True)
        output_file.rename(video_file)
        return True
    except subprocess.CalledProcessError as e:
        print(e)
        output_file.unlink()
        return False
    
    
    
    


if __name__ == "__main__":
    folder = Path("YOU Season 4")
    video_path = folder / "YOU Season 4_EPEps 1 Joe Takes A Holiday.mp4"
    subtitle_files = list((folder/"captions").glob("*"))

    add_subtitles_to_video(video_path, subtitle_files)
