from pathlib import Path
import sys

import numpy as np
from PIL import Image
import rasterio
from rasterio.enums import Resampling
from rasterio.windows import Window


BASE = Path("dados/entrada/base_aprovada.png")
PASTA_GEBCO = Path("dados/temporario")
SAIDA = Path("saida")

SAIDA.mkdir(parents=True, exist_ok=True)


def localizar_arquivos_gebco():
    """
    Localiza automaticamente o GeoTIFF principal do GEBCO e o PNG hillshade
    depois que o ZIP da Release for descompactado.
    """

    tifs = [
        p for p in PASTA_GEBCO.rglob("*.tif")
        if "tid" not in p.name.lower()
        and "sub_ice" not in p.name.lower()
    ]

    hillshades = [
        p for p in PASTA_GEBCO.rglob("*.png")
        if "_hs" in p.name.lower()
        or "hillshade" in p.name.lower()
    ]

    if not tifs:
        raise FileNotFoundError(
            "Não encontrei o GeoTIFF principal do GEBCO em dados/temporario."
        )

    if not hillshades:
        raise FileNotFoundError(
            "Não encontrei o PNG de hillshade do GEBCO em dados/temporario."
        )

    return tifs[0], hillshades[0]


def combinar(base_rgb, hs_gray, elev):
    """
    Combina a aparência da imagem-base aprovada com:
      - profundidade real do GEBCO;
      - hillshade derivado do GEBCO.

    A influência batimétrica é aplicada principalmente sobre áreas abaixo
    do nível do mar.
    """

    base = base_rgb.astype(np.float32) / 255.0
    hs = hs_gray.astype(np.float32) / 255.0
    elev = elev.astype(np.float32)

    # Máscara oceânica suave ao redor do nível do mar.
    mask = 1.0 / (
        1.0
        + np.exp(
            np.clip(
                elev / 60.0,
                -20,
                20
            )
        )
    )

    # Normalização do hillshade.
    hsn = np.clip(
        (hs - 0.28) / (0.78 - 0.28),
        0,
        1
    )

    # Fator de iluminação.
    shade = 0.82 + 0.36 * hsn

    # Profundidade normalizada para aproximadamente 0–6000 m.
    depth = np.clip(
        (-elev) / 6000.0,
        0,
        1
    )

    # Tons de referência para águas rasas e profundas.
    shallow = (
        np.array(
            [61, 145, 166],
            dtype=np.float32
        )
        / 255.0
    )

    deep = (
        np.array(
            [8, 42, 92],
            dtype=np.float32
        )
        / 255.0
    )

    tint = (
        shallow[None, None, :] * (1 - depth[..., None])
        + deep[None, None, :] * depth[..., None]
    )

    # Mantém a imagem-base como componente dominante.
    ocean = base * 0.88 + tint * 0.12

    # Introduz o relevo sombreado.
    ocean = np.clip(
        ocean * shade[..., None],
        0,
        1
    )

    # Aplica a composição principalmente no oceano.
    alpha = (mask * 0.72)[..., None]

    resultado = (
        base * (1 - alpha)
        + ocean * alpha
    )

    return np.clip(
        resultado * 255,
        0,
        255
    ).astype(np.uint8)


def gerar_previa(base_path, gebco_path, hillshade_path):
    """
    Gera um JPG leve para inspeção visual.
    """

    base_preview = Image.open(base_path).convert("RGB")
    pw, ph = base_preview.size

    hill_preview = (
        Image.open(hillshade_path)
        .convert("L")
        .resize(
            (pw, ph),
            Image.Resampling.LANCZOS
        )
    )

    with rasterio.open(gebco_path) as src:
        elev_preview = src.read(
            1,
            out_shape=(ph, pw),
            resampling=Resampling.bilinear
        )

    preview_array = combinar(
        np.asarray(base_preview),
        np.asarray(hill_preview),
        elev_preview
    )

    caminho = SAIDA / "PREVIA_base_com_batimetria.jpg"

    Image.fromarray(preview_array).save(
        caminho,
        quality=95,
        subsampling=0
    )

    print(f"Prévia criada: {caminho}")


def gerar_geotiff(base_path, gebco_path, hillshade_path):
    """
    Gera o raster georreferenciado na grade completa do GEBCO.
    O processamento é feito em blocos para não carregar tudo na RAM.
    """

    with rasterio.open(gebco_path) as src:
        width = src.width
        height = src.height
        transform = src.transform
        crs = src.crs

    print(f"GEBCO: {width} x {height}")
    print(f"CRS: {crs}")

    # Redimensiona apenas a imagem visual para a grade do GEBCO.
    base_full = (
        Image.open(base_path)
        .convert("RGB")
        .resize(
            (width, height),
            Image.Resampling.LANCZOS
        )
    )

    hill_full = (
        Image.open(hillshade_path)
        .convert("L")
        .resize(
            (width, height),
            Image.Resampling.LANCZOS
        )
    )

    output = SAIDA / "base_aprovada_com_batimetria.tif"

    profile = {
        "driver": "GTiff",
        "width": width,
        "height": height,
        "count": 3,
        "dtype": "uint8",
        "crs": crs,
        "transform": transform,
        "compress": "DEFLATE",
        "predictor": 2,
        "tiled": True,
        "blockxsize": 512,
        "blockysize": 512,
        "interleave": "pixel",
    }

    with rasterio.open(gebco_path) as elev_src:
        with rasterio.open(output, "w", **profile) as dst:

            for row in range(0, height, 512):
                print(f"Processando linha {row} de {height}...")

                for col in range(0, width, 512):

                    h = min(512, height - row)
                    w = min(512, width - col)

                    window = Window(
                        col,
                        row,
                        w,
                        h
                    )

                    base_block = np.asarray(
                        base_full.crop(
                            (
                                col,
                                row,
                                col + w,
                                row + h
                            )
                        )
                    )

                    hs_block = np.asarray(
                        hill_full.crop(
                            (
                                col,
                                row,
                                col + w,
                                row + h
                            )
                        )
                    )

                    elev_block = elev_src.read(
                        1,
                        window=window
                    )

                    result = combinar(
                        base_block,
                        hs_block,
                        elev_block
                    )

                    dst.write(
                        result[:, :, 0],
                        1,
                        window=window
                    )

                    dst.write(
                        result[:, :, 1],
                        2,
                        window=window
                    )

                    dst.write(
                        result[:, :, 2],
                        3,
                        window=window
                    )

            # Pirâmides internas para melhorar a navegação.
            dst.build_overviews(
                [2, 4, 8, 16, 32],
                Resampling.average
            )

            dst.update_tags(
                ns="rio_overview",
                resampling="average"
            )

            dst.update_tags(
                DESCRIPTION="Base visual aprovada combinada com batimetria GEBCO 2026",
                SOURCE_BATHYMETRY="GEBCO 2026",
                NOTE=(
                    "A batimetria é derivada do GEBCO. "
                    "A imagem visual de fundo é uma composição cartográfica estilizada."
                )
            )

    print(f"GeoTIFF criado: {output}")


def main():

    if not BASE.exists():
        raise FileNotFoundError(
            f"Imagem-base não encontrada: {BASE}"
        )

    gebco_path, hillshade_path = localizar_arquivos_gebco()

    print(f"Imagem-base: {BASE}")
    print(f"GEBCO: {gebco_path}")
    print(f"Hillshade: {hillshade_path}")

    gerar_previa(
        BASE,
        gebco_path,
        hillshade_path
    )

    gerar_geotiff(
        BASE,
        gebco_path,
        hillshade_path
    )

    print("Processamento concluído com sucesso.")


if __name__ == "__main__":
    try:
        main()
    except Exception as erro:
        print(f"ERRO: {erro}", file=sys.stderr)
        raise
