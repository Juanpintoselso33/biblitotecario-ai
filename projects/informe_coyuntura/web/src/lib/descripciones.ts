// Descripción por indicador: qué es (1 frase) y qué aporta a la lectura del
// cinturón (su rol matusiano). Se muestra en el modal de detalle del indicador.
export interface Descripcion { que: string; aporta: string; }

export const DESCRIPCIONES: Record<string, Descripcion> = {
  // ── Macroeconomía (el motor económico) ──────────────────────────
  ipc_total: {
    que: "Variación mensual del nivel general de precios al consumidor (INDEC).",
    aporta: "Es el termómetro central de la estabilización: marca si el programa antiinflacionario avanza o se estanca.",
  },
  reservas_bcra: {
    que: "Reservas internacionales brutas del Banco Central, en millones de dólares.",
    aporta: "Miden el colchón externo: sin reservas, el tipo de cambio y el pago de deuda quedan expuestos.",
  },
  badlar: {
    que: "Tasa que pagan los bancos por depósitos mayoristas a 30 días o más.",
    aporta: "Refleja el costo del dinero y el sesgo de la política monetaria (más o menos restrictiva).",
  },
  emae_ia: {
    que: "Variación interanual del Estimador Mensual de Actividad Económica.",
    aporta: "Adelanta el pulso del PBI: si la economía crece o se contrae mes a mes.",
  },
  saldo_comercial_12m: {
    que: "Balance acumulado de exportaciones menos importaciones de los últimos 12 meses.",
    aporta: "Indica si el sector externo genera o drena los dólares que necesita el programa.",
  },
  recaudacion: {
    que: "Variación mensual de la recaudación tributaria nacional.",
    aporta: "Aproxima la salud fiscal y el nivel de actividad económica gravada.",
  },
  tcrm: {
    que: "Tipo de cambio real multilateral: competitividad cambiaria frente a los socios comerciales (base 2010=100).",
    aporta: "Señala si el peso está caro o barato, clave para exportar y acumular reservas.",
  },
  rem_ipc_12m: {
    que: "Inflación esperada a 12 meses según el Relevamiento de Expectativas de Mercado del BCRA.",
    aporta: "Captura la credibilidad del programa: las expectativas ancladas ayudan a bajar precios.",
  },
  prestamos_privados: {
    que: "Variación del crédito bancario otorgado al sector privado.",
    aporta: "Mide si el sistema financiero acompaña la actividad con financiamiento.",
  },
  base_monetaria: {
    que: "Variación de la base monetaria (billetes en circulación más reservas bancarias).",
    aporta: "Refleja la emisión y el ancla monetaria sobre la que descansa el plan.",
  },
  tc_mayorista: {
    que: "Variación del tipo de cambio oficial mayorista de referencia.",
    aporta: "Marca el ritmo de devaluación del ancla cambiaria del programa.",
  },

  // ── Política (el tablero de poder) ──────────────────────────────
  votometro_ventaja_lla: {
    que: "Diferencia de intención de voto ponderada entre LLA y el PJ (Votómetro CIGOB).",
    aporta: "Mide el capital electoral del oficialismo, base de su poder de negociación.",
  },
  ratio_dnu: {
    que: "Cantidad de Decretos de Necesidad y Urgencia sobre leyes sancionadas en el año.",
    aporta: "Un ratio alto indica un Ejecutivo que legisla por decreto ante un Congreso que no acompaña.",
  },
  movilizacion_cepa: {
    que: "Índice de conflictividad social y laboral relevado por el CEPA.",
    aporta: "Aproxima la tensión en la calle, un límite real al margen de maniobra del Gobierno.",
  },
  iaf_transferencias: {
    que: "Variación real interanual de las transferencias federales a las provincias.",
    aporta: "Mide la armonía —o el conflicto— fiscal con los gobernadores.",
  },
  eficacia_legislativa: {
    que: "Porcentaje de proyectos enviados por el Ejecutivo que el Congreso aprobó (ventana de 12 meses).",
    aporta: "Mide la capacidad real de convertir la agenda de gobierno en ley.",
  },
  cohesion_bloque: {
    que: "Porcentaje de diputados de LLA que votan alineados con la posición oficial del bloque.",
    aporta: "Indica la disciplina de la tropa propia, clave para sostener vetos y aprobar leyes.",
  },
  gobernadores_alineamiento: {
    que: "Porcentaje de gobernadores cuya posición pública es de alineamiento con la política nacional.",
    aporta: "Mide el apoyo territorial, decisivo en el Senado y en la gobernabilidad.",
  },
  veto_quorum: {
    que: "Porcentaje de sesiones de Diputados frustradas por falta de quórum.",
    aporta: "Señala la capacidad de la oposición de bloquear o forzar la agenda parlamentaria.",
  },
  comisiones_caidas: {
    que: "Porcentaje de proyectos con dictamen de comisión que nunca llegaron al recinto.",
    aporta: "Mide el embudo legislativo: cuánto queda trabado antes de poder votarse.",
  },

  // ── Vida cotidiana (el bolsillo y la calle) ─────────────────────
  brecha_salario_cbt: {
    que: "Cantidad de canastas básicas totales que cubre el salario formal promedio (RIPTE/CBT).",
    aporta: "Mide el poder adquisitivo real del ingreso, lo que la gente siente en el bolsillo.",
  },
  ipc_alimentos: {
    que: "Variación mensual de los precios de alimentos y bebidas (INDEC).",
    aporta: "Es la inflación más sensible socialmente: pega directo en la mesa de cada hogar.",
  },
  endeudamiento_familiar: {
    que: "Saldo del crédito de consumo de las familias (tarjeta más préstamos personales), en billones de pesos.",
    aporta: "Refleja si los hogares llegan a fin de mes apoyándose en deuda.",
  },
  peso_tarifas: {
    que: "Variación mensual de los precios regulados (luz, gas, agua, transporte).",
    aporta: "Mide el impacto de la quita de subsidios sobre el gasto fijo del hogar.",
  },
  consumo_carne: {
    que: "Consumo aparente de carne vacuna por habitante al año (CICCRA).",
    aporta: "Proxy histórico del bienestar alimentario y del poder de compra popular.",
  },
  informalidad: {
    que: "Porcentaje de asalariados sin descuento jubilatorio (empleo informal, INDEC EPH).",
    aporta: "Mide la precariedad laboral y la exclusión de la red de protección social.",
  },
  mortalidad_pymes: {
    que: "Variación de la actividad industrial manufacturera (IPI), usada como proxy.",
    aporta: "Aproxima la salud del entramado productivo y del empleo PyME.",
  },
  despacho_cemento: {
    que: "Índice de actividad de la construcción (ISAC, INDEC).",
    aporta: "Termómetro de la obra pública y privada, gran motor de empleo de baja calificación.",
  },
  pluriempleo: {
    que: "Porcentaje de subocupados que buscan trabajar más horas (INDEC EPH).",
    aporta: "Señala empleo insuficiente: gente ocupada a la que no le alcanza.",
  },
  inseguridad: {
    que: "Cantidad de hechos delictivos registrados por año (SNIC, Ministerio de Seguridad).",
    aporta: "Mide una de las principales preocupaciones cotidianas de la población.",
  },
  icc_utdt: {
    que: "Índice de Confianza del Consumidor (Universidad Torcuato Di Tella).",
    aporta: "Captura el humor económico de la gente, que anticipa consumo y voto.",
  },
  sentimiento_digital: {
    que: "Interés de búsqueda en Google sobre inflación, precios y términos afines.",
    aporta: "Proxy en tiempo real de la urgencia económica percibida por la sociedad.",
  },
  patentamiento_motos: {
    que: "Unidades de motos patentadas en el mes (CAFAM).",
    aporta: "Proxy de consumo durable de los sectores medios y bajos.",
  },

  // ── Gestión (la capacidad de ejecutar) ──────────────────────────
  cepo_mulc: {
    que: "Brecha entre el dólar financiero/libre y el oficial.",
    aporta: "Mide el grado de normalización cambiaria, uno de los ejes del programa económico.",
  },
  privatizaciones: {
    que: "Avance de la transferencia efectiva de empresas públicas al sector privado.",
    aporta: "Mide la ejecución de una reforma estructural emblema del Gobierno.",
  },
  concesiones_infraestructura: {
    que: "Avance de la concesión de corredores viales y obras de infraestructura.",
    aporta: "Indica si el Estado logra traspasar infraestructura al sector privado.",
  },
  reduccion_estado: {
    que: "Variación de la dotación de empleo del sector público.",
    aporta: "Mide el ajuste del tamaño del Estado, prioridad declarada del oficialismo.",
  },
  reestructuracion_organismos: {
    que: "Organismos públicos disueltos, fusionados o centralizados desde diciembre de 2023.",
    aporta: "Mide el avance concreto de la reforma del aparato estatal.",
  },
  rigi_inversiones: {
    que: "Avance de las inversiones aprobadas bajo el Régimen de Incentivo a Grandes Inversiones (RIGI).",
    aporta: "Señala la llegada de grandes inversiones, apuesta de crecimiento del plan.",
  },
  desregulacion_normativa: {
    que: "Normas derogadas o modificadas desde diciembre de 2023 (InfoLeg).",
    aporta: "Mide el ritmo de la desregulación económica impulsada por el Gobierno.",
  },
  apertura_comercial: {
    que: "Variación interanual de las importaciones totales, usada como proxy.",
    aporta: "Aproxima el grado de apertura de la economía al comercio exterior.",
  },
  asistencia_directa: {
    que: "Porcentaje de beneficios sociales pagados sin intermediación de organizaciones.",
    aporta: "Mide la reforma del esquema de asistencia social y el corte de intermediarios.",
  },
  fal_modernizacion_laboral: {
    que: "Avance de implementación de la modernización laboral (Fondo de Asistencia Laboral).",
    aporta: "Indica el progreso de la reforma del régimen de trabajo.",
  },
  libertad_opcion_salud: {
    que: "Opciones de cambio de obra social captadas por la Superintendencia de Servicios de Salud.",
    aporta: "Mide la desregulación del sistema de salud y la libre elección.",
  },
  protocolo_antipiquetes: {
    que: "Porcentaje de cortes de calle con carril libre garantizado.",
    aporta: "Mide la aplicación del protocolo de orden público en la vía pública.",
  },
};
