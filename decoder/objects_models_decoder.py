import os
import tkinter as tk
from tkinter import filedialog
import argparse
import vedo
from struct import *


def main():
    parser = argparse.ArgumentParser(description='gilde-decoder')
    parser.add_argument('-i', '--input', help='input path')
    parser.add_argument('-o', '--output', help='output path')

    args = parser.parse_args()

    if not args.input:
        root = tk.Tk()
        root.withdraw()
        args.input = filedialog.askdirectory()
        root.destroy()
        args.input = args.input.replace('/', '\\')

    if not args.output:
        args.output = os.path.join(os.getcwd(), 'output')

    if not os.path.exists(args.input):
        print('input path does not exist')
        return

    if not os.path.exists(args.output):
        os.mkdir(args.output)

    objects_path = os.path.join(args.input, "Resources/Objects")
    input_path = os.path.join(objects_path, "Accessoires/Deko/kaefig.bgf")

    output_path = os.path.join(objects_path, "Accessoires/Deko/kaefig.obj")
    decode_object(input_path, output_path)

    show_object(output_path)


def decode_object(target_path, output_path):
    with open(target_path, "rb") as file:
        vectors = []
        faces = []
        file.seek(0x6B)
        for i in range(24):
            x = unpack("<f", file.read(4))[0]
            y = unpack("<f", file.read(4))[0]
            z = unpack("<f", file.read(4))[0]
            vector = (x, y, z)
            vectors += (vector,)

        file.seek(0x18D)

        for i in range(10):
            a = unpack("<i", file.read(4))[0] + 1
            b = unpack("<i", file.read(4))[0] + 1
            c = unpack("<i", file.read(4))[0] + 1
            face = (a, b, c)
            faces += (face,)
            file.read(1)
            file.read(12)
            file.read(12)
            file.read(12)
            file.read(16)

        with open(output_path, "w") as file:
            file.write("g test\n")

            for (x, y, z) in vectors:
                file.write("v ")
                file.write(str(x) + " ")
                file.write(str(y) + " ")
                file.write(str(z) + "\n")

            for (a, b, c) in faces:
                file.write("f ")
                file.write(str(a) + " ")
                file.write(str(b) + " ")
                file.write(str(c) + "\n")


def show_object(output_path):
    mesh = vedo.Mesh(output_path)

    mesh.show()


if __name__ == "__main__":
    main()
