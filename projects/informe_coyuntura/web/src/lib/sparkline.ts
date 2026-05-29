// Genera coordenadas para sparklines y charts SVG a partir de una serie de valores.
export interface PuntoSerie { fecha: string; valor: number; }

export interface SparkPaths {
  linea: string;   // "M x,y L x,y ..."
  area: string;    // path cerrado para el relleno
  ultimo: { x: number; y: number } | null;
  vacio: boolean;
}

// w/h en unidades de viewBox; pad vertical para que la línea no toque los bordes.
export function sparkline(serie: PuntoSerie[], w = 60, h = 22, pad = 3): SparkPaths {
  const vals = serie.map(p => p.valor);
  if (vals.length < 2) return { linea: "", area: "", ultimo: null, vacio: true };
  const min = Math.min(...vals), max = Math.max(...vals);
  const span = max - min || 1;
  const stepX = w / (vals.length - 1);
  const pts = vals.map((v, i) => ({
    x: +(i * stepX).toFixed(2),
    y: +(h - pad - ((v - min) / span) * (h - 2 * pad)).toFixed(2),
  }));
  const linea = pts.map((p, i) => `${i === 0 ? "M" : "L"}${p.x},${p.y}`).join(" ");
  const area = `${linea} L${pts[pts.length - 1].x},${h} L${pts[0].x},${h} Z`;
  return { linea, area, ultimo: pts[pts.length - 1], vacio: false };
}

// Variante para el gráfico grande / minis (mismo cálculo, distinto tamaño).
export function chartPath(serie: PuntoSerie[], w: number, h: number, pad = 6): SparkPaths {
  return sparkline(serie, w, h, pad);
}
