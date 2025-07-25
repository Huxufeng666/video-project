import cv2
import numpy as np
import random
import asyncio
import platform
from moviepy.editor import VideoFileClip

async def convert_to_ascii_frame(frame, char_set=" 01#@+-", char_size=10):
    # 转换为灰度图
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape
    result = np.ones((height, width, 3), dtype=np.uint8) * 0  # 黑色背景

    # 根据亮度选择字符
    for y in range(0, height, char_size):
        for x in range(0, width, char_size):
            pixel_value = gray[y, x]
            char = char_set[int(pixel_value / 255 * (len(char_set) - 1))]  # 根据亮度映射字符
            cv2.putText(result, char, (x, y + char_size), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

    return result

async def process_video(input_path, output_path):
    try:
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            print("无法打开视频文件")
            return

        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter('temp_output2.mp4', fourcc, fps, (frame_width, frame_height))

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            ascii_frame = await convert_to_ascii_frame(frame)
            out.write(ascii_frame)

        cap.release()
        out.release()

        video = VideoFileClip(input_path)
        temp_video = VideoFileClip('temp_output.mp4')
        final_video = temp_video.set_audio(video.audio)
        final_video.write_videofile(output_path, codec="libx264", logger=None)
        print(f"视频已成功保存到 {output_path}")
    except Exception as e:
        print(f"发生错误: {e}")

async def main():
    input_path = "25932923127-1-192.mp4"
    output_path = "./" 
    await process_video(input_path, output_path)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())