import sys
sys.stdout.reconfigure(encoding='utf-8')

# Pesos de cada cinturón matusiano en el score agregado (deben sumar 1.0)
PESOS_CINTURONES = {
    "macro": 0.30,
    "politica": 0.30,
    "vida_cotidiana": 0.20,
    "gestion": 0.20,
}

# Umbrales de clasificación de estado por cinturón (score 0-10)
# score <= ESTABLE_MAX → "estable" | <= EN_TENSION_MAX → "en_tension" | > EN_TENSION_MAX → "tensionado"
UMBRALES = {
    "ESTABLE_MAX": 3,
    "EN_TENSION_MAX": 6,
}

# Mapping cinturón dominante → barbarismo activo (marco PES de Matus)
BARBARISMO_MAP = {
    "macro": "tecnocrático",
    "politica": "político",
    "gestion": "gerencial",
    "vida_cotidiana": "político",
}
