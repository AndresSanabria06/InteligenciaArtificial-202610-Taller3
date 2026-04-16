"""
crimen_bono-el_topo.py - El Topo de la Cumbre Sombra Atlas

La Cumbre Sombra Atlas es una reunión de alto secreto realizado a las 3 AM en un búnker
subterráneo sin señal externa. Asistieron cuatro representantes: la Embajadora Vidal, el
General Montero, el Analista Bravo y la Directora Serrano. Durante la reunión, una célula
terrorista conocida como Fractura ejecutó un ataque de precisión que solo pudo coordinarse
con información interna: hora exacta, coordenadas del búnker y protocolo de turno de guardia.
La Embajadora Vidal tiene registro biométrico de entrada y salida ininterrumpido en la sala
de sesiones durante toda la noche. El General Montero estuvo de guardia exterior verificado
por cámara de seguridad independiente durante las tres horas críticas. El Analista Bravo
fue visto por dos testigos independientes saliendo al pasillo durante la ventana de ataque.
La Directora Serrano no tiene coartada verificada para la ventana de ataque. Se encontraron
en el maletín del Analista Bravo fragmentos de papel con coordenadas del búnker escritas a
mano. El teléfono satelital de la Directora Serrano registró una transmisión saliente cifrada
veinte minutos antes del ataque. El Analista Bravo tiene deudas con una organización
vinculada a Fractura según inteligencia financiera. La Directora Serrano tiene acceso al
protocolo de turno de guardia y al mapa de coordenadas del búnker. El Analista Bravo acusa
a la Directora Serrano. La Directora Serrano niega cualquier transmisión y acusa al Analista
Bravo. Un informante de Fractura mencionó por nombre al Analista Bravo y a la Directora
Serrano como contactos internos activos.

Como detective, he llegado a las siguientes conclusiones:
Quien tiene registro biométrico o de cámara ininterrumpido durante la ventana crítica queda
descartado como topo. Quien posee evidencia física comprometedora (coordenadas escritas o
transmisión cifrada) tiene evidencia en su contra. Quien tiene vínculos financieros con
Fractura tiene motivo probado. Quien tiene acceso a los tres elementos del ataque (hora,
coordenadas y protocolo) tiene capacidad operativa. Quien tiene evidencia en su contra,
motivo probado y sin coartada verificada es el topo. Cuando un sospechoso sin coartada
acusa a otro, esa acusación es táctica de distracción. Quien es mencionado por el informante
de Fractura y además es el topo confirma la infiltración. Si todos los mencionados por el
informante resultan topos, la célula tenía infiltración total en la cumbre.
"""

from src.crime_case import CrimeCase, QuerySpec
from src.predicate_logic import ExistsGoal, ForallGoal, KnowledgeBase, Predicate, Rule, Term


def crear_kb() -> KnowledgeBase:
    """Construye la KB según la narrativa del módulo."""
    kb = KnowledgeBase()

    # Constantes del caso
    embajadora_vidal   = Term("embajadora_vidal")
    general_montero    = Term("general_montero")
    analista_bravo     = Term("analista_bravo")
    directora_serrano  = Term("directora_serrano")
    maletin_bravo      = Term("maletin_bravo")
    telefono_serrano   = Term("telefono_serrano")

    # Hechos
    # Coartadas verificadas objetivamente
    kb.add_fact(Predicate("registro_biometrico_ininterrumpido", (embajadora_vidal,)))
    kb.add_fact(Predicate("camara_guardia_verificada",          (general_montero,)))

    # Sin coartada verificada
    kb.add_fact(Predicate("sin_coartada", (analista_bravo,)))
    kb.add_fact(Predicate("sin_coartada", (directora_serrano,)))

    # Evidencia física comprometedora
    kb.add_fact(Predicate("coordenadas_escritas_en",  (analista_bravo,  maletin_bravo)))
    kb.add_fact(Predicate("objeto_comprometedor",     (maletin_bravo,)))
    kb.add_fact(Predicate("transmision_cifrada_desde", (directora_serrano, telefono_serrano)))
    kb.add_fact(Predicate("objeto_comprometedor",     (telefono_serrano,)))

    # Motivo: vínculos financieros con Fractura
    kb.add_fact(Predicate("vinculo_financiero_fractura", (analista_bravo,)))

    # Capacidad operativa: acceso a los tres elementos del ataque
    kb.add_fact(Predicate("acceso_hora_secreta",       (directora_serrano,)))
    kb.add_fact(Predicate("acceso_coordenadas_bunker", (directora_serrano,)))
    kb.add_fact(Predicate("acceso_protocolo_guardia",  (directora_serrano,)))

    # Informante de Fractura menciona por nombre
    kb.add_fact(Predicate("mencionado_por_informante", (analista_bravo,)))
    kb.add_fact(Predicate("mencionado_por_informante", (directora_serrano,)))

    # Acusaciones cruzadas
    kb.add_fact(Predicate("acusa", (analista_bravo,    directora_serrano)))
    kb.add_fact(Predicate("acusa", (directora_serrano, analista_bravo)))

    # Reglas 
    # Registro biométrico ininterrumpido -> descartado
    kb.add_rule(Rule(
        head=Predicate("descartado", (Term("$X"),)),
        body=(Predicate("registro_biometrico_ininterrumpido", (Term("$X"),)),)
    ))

    # Cámara de guardia verificada -> descartado
    kb.add_rule(Rule(
        head=Predicate("descartado", (Term("$X"),)),
        body=(Predicate("camara_guardia_verificada", (Term("$X"),)),)
    ))

    # Coordenadas escritas en objeto comprometedor -> evidencia_fisica
    kb.add_rule(Rule(
        head=Predicate("evidencia_fisica", (Term("$X"),)),
        body=(
            Predicate("coordenadas_escritas_en", (Term("$X"), Term("$O"))),
            Predicate("objeto_comprometedor",    (Term("$O"),)),
        )
    ))

    # Transmisión cifrada desde objeto comprometedor -> evidencia_fisica
    kb.add_rule(Rule(
        head=Predicate("evidencia_fisica", (Term("$X"),)),
        body=(
            Predicate("transmision_cifrada_desde", (Term("$X"), Term("$O"))),
            Predicate("objeto_comprometedor",      (Term("$O"),)),
        )
    ))

    # Vínculo financiero con Fractura -> motivo_probado
    kb.add_rule(Rule(
        head=Predicate("motivo_probado", (Term("$X"),)),
        body=(Predicate("vinculo_financiero_fractura", (Term("$X"),)),)
    ))

    # Acceso a los tres elementos -> capacidad_operativa
    kb.add_rule(Rule(
        head=Predicate("capacidad_operativa", (Term("$X"),)),
        body=(
            Predicate("acceso_hora_secreta",       (Term("$X"),)),
            Predicate("acceso_coordenadas_bunker", (Term("$X"),)),
            Predicate("acceso_protocolo_guardia",  (Term("$X"),)),
        )
    ))

    # Evidencia física + motivo probado + sin coartada -> topo
    kb.add_rule(Rule(
        head=Predicate("topo", (Term("$X"),)),
        body=(
            Predicate("evidencia_fisica", (Term("$X"),)),
            Predicate("motivo_probado",   (Term("$X"),)),
            Predicate("sin_coartada",     (Term("$X"),)),
        )
    ))

    # Evidencia física + capacidad operativa + sin coartada -> topo
    kb.add_rule(Rule(
        head=Predicate("topo", (Term("$X"),)),
        body=(
            Predicate("evidencia_fisica",    (Term("$X"),)),
            Predicate("capacidad_operativa", (Term("$X"),)),
            Predicate("sin_coartada",        (Term("$X"),)),
        )
    ))

    # Sin coartada acusa a alguien -> acusacion_tactica
    kb.add_rule(Rule(
        head=Predicate("acusacion_tactica", (Term("$X"), Term("$Y"))),
        body=(
            Predicate("sin_coartada", (Term("$X"),)),
            Predicate("acusa",        (Term("$X"), Term("$Y"))),
        )
    ))

    # Mencionado por informante y además topo -> infiltracion_confirmada
    kb.add_rule(Rule(
        head=Predicate("infiltracion_confirmada", (Term("$X"),)),
        body=(
            Predicate("mencionado_por_informante", (Term("$X"),)),
            Predicate("topo",                      (Term("$X"),)),
        )
    ))

    return kb


CASE = CrimeCase(
    id="cumbre_sombra_atlas",
    title="El Topo de la Cumbre Sombra Atlas",
    suspects=(
        "embajadora_vidal",
        "general_montero",
        "analista_bravo",
        "directora_serrano",
    ),
    narrative=__doc__,
    description=(
        "Un ataque terrorista de precisión golpeó una cumbre ultrasecreta a las 3 AM. "
        "Solo alguien de adentro pudo filtrar la hora, las coordenadas y el protocolo de guardia. "
        "Dos sospechosos sin coartada se acusan mutuamente. Uno tiene coordenadas en su maletín "
        "y vínculos financieros con la célula; el otro tiene acceso total y una transmisión cifrada "
        "minutos antes del ataque. Encuentra al topo antes de que hable de nuevo."
    ),
    create_kb=crear_kb,
    queries=(
        QuerySpec(
            description="¿La Embajadora Vidal está descartada como topo?",
            goal=Predicate("descartado", (Term("embajadora_vidal"),)),
        ),
        QuerySpec(
            description="¿El Analista Bravo tiene evidencia física en su contra?",
            goal=Predicate("evidencia_fisica", (Term("analista_bravo"),)),
        ),
        QuerySpec(
            description="¿El Analista Bravo es el topo?",
            goal=Predicate("topo", (Term("analista_bravo"),)),
        ),
        QuerySpec(
            description="¿La acusación del Analista Bravo contra Serrano es táctica de distracción?",
            goal=Predicate("acusacion_tactica", (Term("analista_bravo"), Term("directora_serrano"))),
        ),
        QuerySpec(
            description="¿La infiltración del Analista Bravo queda confirmada por el informante?",
            goal=Predicate("infiltracion_confirmada", (Term("analista_bravo"),)),
        ),
        QuerySpec(
            description="¿Existe al menos un topo identificado en la cumbre?",
            goal=ExistsGoal("$T", Predicate("topo", (Term("$T"),))),
        ),
        QuerySpec(
            description="¿Todo mencionado por el informante resultó ser topo?",
            goal=ForallGoal(
                "$X",
                Predicate("mencionado_por_informante", (Term("$X"),)),
                Predicate("topo", (Term("$X"),)),
            ),
        ),
    ),
)