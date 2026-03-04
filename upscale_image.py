#!/usr/bin/env python3
import argparse
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LIB_DIR = os.path.join(SCRIPT_DIR, "lib")
if os.path.exists(LIB_DIR):
    os.environ["LD_LIBRARY_PATH"] = f"{LIB_DIR}:{os.environ.get('LD_LIBRARY_PATH', '')}"

from PIL import Image
from realesrgan_ncnn_py import Realesrgan


def improve_image(input_path, output_path, scale=4, gpuid=0, tilesize=0, tta_mode=False):
    print(f"Procesando: {input_path}")
    print(f"  Scale: {scale}x")
    print(f"  GPU ID: {gpuid}")
    
    scale_map = {2: 1, 3: 2, 4: 0}
    model = scale_map.get(scale, 0)
    
    realesrgan = Realesrgan(
        gpuid=gpuid,
        model=model,
        tilesize=tilesize,
        tta_mode=tta_mode
    )
    
    with Image.open(input_path) as img:
        img_converted = img.convert("RGB")
        img_improved = realesrgan.process_pil(img_converted)
        img_improved.save(output_path, quality=95)
    
    print(f"Guardado: {output_path}")
    
    original_size = os.path.getsize(input_path)
    improved_size = os.path.getsize(output_path)
    print(f"  Tamano original: {original_size / 1024:.1f} KB")
    print(f"  Tamano mejorado: {improved_size / 1024:.1f} KB")


def main():
    parser = argparse.ArgumentParser(
        description="Mejora la definicion de imagenes usando IA (Real-ESRGAN)"
    )
    parser.add_argument("input", help="Imagen de entrada")
    parser.add_argument("-o", "--output", help="Imagen de salida (default: input_hd.ext)")
    parser.add_argument("-s", "--scale", type=int, default=2, choices=[2, 3, 4],
                        help="Factor de escala (default: 2)")
    parser.add_argument("-g", "--gpuid", type=int, default=0,
                        help="ID de GPU (default: 0, usa -1 para CPU)")
    parser.add_argument("-t", "--tilesize", type=int, default=0,
                        help="Tamano de tile para imagenes grandes (0=auto, default: 0)")
    parser.add_argument("--tta", action="store_true",
                        help="Usar test-time augmentation (mejor calidad, mas lento)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Error: No se encontro el archivo: {args.input}")
        return
    
    if args.output is None:
        base, ext = os.path.splitext(args.input)
        args.output = f"{base}_hd{ext}"
    
    improve_image(
        args.input,
        args.output,
        scale=args.scale,
        gpuid=args.gpuid,
        tilesize=args.tilesize,
        tta_mode=args.tta
    )


if __name__ == "__main__":
    main()
