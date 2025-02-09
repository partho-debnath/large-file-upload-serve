import requests
import os
import math


def upload_file():
    url = "http://127.0.0.1:8000/file-upload/"
    file_path = "/home/partho/Downloads/icc/Lucifer S01/Lucifer S01E01.mkv"
    file_id = "1"
    # 1MB = 1025KB; 1KB = 1024Bytes;  (1024 * 1024)Bytes == 1MB
    chunk_size = 1024 * 1024
    total_chunks = math.ceil(os.path.getsize(file_path) / chunk_size)
    print("total_chunks = ", total_chunks)
    with open(file_path, "rb") as file:
        for chunk_index in range(total_chunks):
            data = {
                "file_id": file_id,
                "chunk_index": chunk_index,
                "total_chunk": total_chunks,
                "file_name": os.path.basename(file.name),
            }
            response = requests.post(
                url=url,
                data=data,
                files={
                    "file": (
                        os.path.basename(file_path),
                        file.read(chunk_size),
                    ),
                },
            )
            print(response.json())


if __name__ == "__main__":
    upload_file()
