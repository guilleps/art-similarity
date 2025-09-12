from textwrap import dedent
from typing import Tuple

SYSTEM_PROMPT = (
    "Eres un analista de visión que explica comparaciones de imágenes de forma breve, "
    "precisa y sin revelar cadena de pensamiento. Devuelve SIEMPRE JSON válido con el esquema pedido y una explicación corta."
)

PREFERENCE_ORDER = [
    "texture",
    "hsv_hue",
    "heat_color_map",
    "contrast",
    "hsv_saturation",
    "hsv_value",
]

USER_TEMPLATE = dedent(
    """
    Tarea: con base en los puntajes de similitud por transformación entre image_1 e image_2, elige la transformación que mejor preserva rasgos compartidos entre ambas imágenes (mayor robustez = mayor similarity).

    Datos:
    - comparison_id: {comparison_id}
    - similitud:
      - texture: {texture}
      - contrast: {contrast}
      - hsv_hue: {hsv_hue}
      - hsv_saturation: {hsv_saturation}
      - hsv_value: {hsv_value}
      - heat_color_map: {heat_color_map}

    URLs relevantes (por si el modelo soporta visión):
    - image_1 original: {img1}
    - image_2 original: {img2}
    - Pares por transformación (image_1 vs image_2):
      - texture: {tex1}, {tex2}
      - contrast: {con1}, {con2}
      - hsv_hue: {hue1}, {hue2}
      - hsv_saturation: {sat1}, {sat2}
      - hsv_value: {val1}, {val2}
      - heat_color_map: {heat1}, {heat2}

    Criterios:
    1) Ganador = mayor similarity; en empate, prioriza transformaciones más invariantes ({order}), salvo evidencia contraria.
    2) Asigna label por umbrales: >=0.93 "muy similar", >=0.88 "similar", de lo contrario "diferente".
    3) Devuelve JSON EXACTO según el esquema.
    4) Explicación máxima 120 palabras; no incluyas pasos de razonamiento.
    """
)


def build_user_prompt(payload: dict) -> str:
    sim = payload["similitud"]
    return USER_TEMPLATE.format(
        comparison_id=payload.get("comparison_id", "unknown"),
        texture=sim["texture"]["similarity"],
        contrast=sim["contrast"]["similarity"],
        hsv_hue=sim["hsv_hue"]["similarity"],
        hsv_saturation=sim["hsv_saturation"]["similarity"],
        hsv_value=sim["hsv_value"]["similarity"],
        heat_color_map=sim["heat_color_map"]["similarity"],
        img1=payload["image_1"]["original_image"],
        img2=payload["image_2"]["original_image"],
        tex1=sim["texture"]["files"][0],
        tex2=sim["texture"]["files"][1],
        con1=sim["contrast"]["files"][0],
        con2=sim["contrast"]["files"][1],
        hue1=sim["hsv_hue"]["files"][0],
        hue2=sim["hsv_hue"]["files"][1],
        sat1=sim["hsv_saturation"]["files"][0],
        sat2=sim["hsv_saturation"]["files"][1],
        val1=sim["hsv_value"]["files"][0],
        val2=sim["hsv_value"]["files"][1],
        heat1=sim["heat_color_map"]["files"][0],
        heat2=sim["heat_color_map"]["files"][1],
        order=", ".join(PREFERENCE_ORDER),
    )


def pick_winner(sim: dict) -> Tuple[str, float]:
    best = max(((k, v["similarity"]) for k, v in sim.items()), key=lambda t: t[1])
    return best
