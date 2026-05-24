import os
import time
from multiprocessing import Pool, cpu_count
from PIL import Image


INPUT_DIR = "images"
OUTPUT_DIR = "processed"
SIZE = (800, 600)


def create_test_images(count=20):
    os.makedirs(INPUT_DIR, exist_ok=True)

    for i in range(count):
        img = Image.new(
            "RGB",
            (1200, 900),
            color=(i * 30 % 255, i * 60 % 255, i * 90 % 255)
        )
        img.save(os.path.join(INPUT_DIR, f"img_{i}.jpg"))


def process_image(filename):
    input_path = os.path.join(INPUT_DIR, filename)
    output_path = os.path.join(OUTPUT_DIR, f"out_{filename}")

    with Image.open(input_path) as img:
        img = img.rotate(-90, expand=True)          # 90 градусов по часовой стрелке
        img = img.resize(SIZE, Image.LANCZOS)       # 800x600
        img = img.convert("L")                      # оттенки серого
        img.save(output_path)


def get_jpg_files():
    return [
        f for f in os.listdir(INPUT_DIR)
        if f.lower().endswith(".jpg")
    ]


def process_sequential(files):
    start = time.perf_counter()

    for file in files:
        process_image(file)

    end = time.perf_counter()
    print(f"Последовательная обработка: {end - start:.4f} секунд")


def process_parallel(files):
    start = time.perf_counter()

    with Pool(processes=cpu_count()) as pool:
        pool.map(process_image, files)

    end = time.perf_counter()
    print(f"Параллельная обработка: {end - start:.4f} секунд")


def main():
    create_test_images(count=20)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    files = get_jpg_files()

    process_sequential(files)
    process_parallel(files)


if __name__ == "__main__":
    main()