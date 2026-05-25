import os
import time
from multiprocessing import Pool, cpu_count
from PIL import Image


INPUT_DIR = "images"
OUTPUT_DIR = "processed"


def clear_folder(folder):
    if os.path.exists(folder):
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)

            if os.path.isfile(file_path):
                os.remove(file_path)


def create_test_images(count=10):
    os.makedirs(INPUT_DIR, exist_ok=True)

    # Удаляем старые изображения
    clear_folder(INPUT_DIR)

    for i in range(count):

        img = Image.new(
            "RGB",
            (1200, 900),
            color=(
                40 + i * 20,
                80 + i * 15,
                120 + i * 10
            )
        )

        img.save(os.path.join(INPUT_DIR, f"img_{i}.jpg"))


def process_image(filename):
    input_path = os.path.join(INPUT_DIR, filename)
    output_path = os.path.join(OUTPUT_DIR, f"out_{filename}")

    with Image.open(input_path) as img:

        # Поворот на 90° по часовой стрелке
        img = img.transpose(Image.Transpose.ROTATE_270)

        # Изменение размера
        img = img.resize((800, 600), Image.LANCZOS)

        # Оттенки серого
        img = img.convert("L")

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

    sequential_time = end - start

    print(f"Последовательная обработка: {sequential_time:.4f} секунд")

    return sequential_time


def process_parallel(files):
    start = time.perf_counter()

    with Pool(processes=cpu_count()) as pool:
        pool.map(process_image, files)

    end = time.perf_counter()

    parallel_time = end - start

    print(f"Параллельная обработка: {parallel_time:.4f} секунд")

    return parallel_time


def main():

    print("Программа обработки изображений")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    clear_folder(OUTPUT_DIR)

    create_test_images(count=10)

    files = get_jpg_files()
    sequential_time = process_sequential(files)
    parallel_time = process_parallel(files)
    speedup = sequential_time / parallel_time

    print(f"\nУскорение: {speedup:.2f}x")


if __name__ == "__main__":
    main()