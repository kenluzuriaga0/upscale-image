# Upscale Image

Script en Python para mejorar la definición de imágenes usando el modelo **Real-ESRGAN** (Real Enhanced Super-Resolution GAN).

## Requisitos

- Python 3.8+
- GPU NVIDIA o AMD con soporte Vulkan
- Linux (el script está configurado para Linux)

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu_usuario/upscale_image.git
cd upscale_image

# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Uso Básico

```bash
# Mejorar una imagen con escala 2x (default)
./upscale.sh foto_borrosa.jpg

# Especificar imagen de salida
./upscale.sh entrada.jpg -o salida_mejorada.jpg

# Usar escala 4x (mejor calidad)
./upscale.sh foto.jpg -s 4

# Usar escala 3x
./upscale.sh foto.jpg -s 3

# Usar NVIDIA GPU (si tienes múltiples GPUs)
./upscale.sh foto.jpg -g 1

# Forzar CPU
./upscale.sh foto.jpg -g -1
```

## Opciones

| Opción | Descripción | Default |
|--------|-------------|---------|
| `-o, --output` | Archivo de salida | `input_hd.ext` |
| `-s, --scale` | Factor de escala (2, 3, 4) | 2 |
| `-g, --gpuid` | ID de GPU (-1 para CPU) | 0 |
| `-t, --tilesize` | Tamaño de tile (0=auto) | 0 |
| `--tta` | Test-time augmentation (mejor calidad) | off |

## Factor de Escala

El factor de escala determina cuánto se enlarge la imagen:

- **2x**: Imagen al 200% (doble tamaño) - **default**
- **3x**: Imagen al 300% (triple tamaño)  
- **4x**: Imagen al 400% (cuádruple tamaño)

Ejemplo: imagen 500x500 → 1000x1000 con scale 2x

## GPU

Tu sistema tiene detectadas:
- GPU 0: AMD Radeon 780M
- GPU 1: NVIDIA GeForce RTX 4050 Laptop GPU

**Para usar NVIDIA** (más rápida):
```bash
./upscale.sh foto.jpg -g 1
```

## Test-Time Augmentation (--tta)

Esta opción procesa la imagen múltiples veces desde diferentes ángulos y promedia los resultados. Mejora la calidad pero es 4-8x más lento.

```bash
./upscale.sh foto.jpg --tta
```

## Formatos Soportados

- JPEG (.jpg, .jpeg)
- PNG (.png)
- WebP (.webp)

## Ejemplo Completo

```bash
# Mejorar foto con NVIDIA, escala 4x, mejor calidad
./upscale.sh mis_fotos/vacaciones.jpg -o mis_fotos/vacaciones_hd.jpg -g 1 --tta
```

## Solución de Problemas

### "No se encontró el archivo"
Asegúrate de que la ruta de la imagen es correcta.

### Error de GPU
Si tienes problemas, prueba usar CPU:
```bash
./upscale.sh foto.jpg -g -1
```

### Error de librerías
Si ves errores sobre `libomp`, el script ya incluye un wrapper que configura las librerías automáticamente.

## Cómo Funciona

Real-ESRGAN es una red neuronal entrenada para:
1. Agrandar la imagen al factor especificado
2. "Inventar" nuevos píxeles basándose en patrones aprendidos
3. Mejorar detalles y texturas

A diferencia de métodos tradicionales (bicubic, lanczos), este modelo realmente "entiende" el contenido de la imagen y genera detalles realistas.

## Estructura del Proyecto

```
upscale_image/
├── upscale_image.py   # Script principal
├── upscale.sh         # Wrapper (configura librerías)
├── venv/              # Entorno virtual Python (no subir a git)
├── lib/               # Librerías necesarias
├── requirements.txt   # Dependencias Python
└── README.md          # Este archivo
```

## Licencia

El modelo Real-ESRGAN es de código abierto (licencia MIT).
