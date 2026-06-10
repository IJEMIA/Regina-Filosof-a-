Aquí tienes tu app transformada en una tutora de filosofía personalizada para Regina, con estética rosa completa y todo el temario de HDF integrado en el prompt del sistema:

```python
import streamlit as st
from openai import OpenAI
from gtts import gTTS
import io

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="🌸 Tutora de Filosofía para Regina",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={'Get Help': None, 'Report a bug': None, 'About': None}
)

# CSS ESENCIAL — Estética rosa completa
css_rosa = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500;600&display=swap');

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stDecoration"] {display: none;}
    .stDeployButton {display: none;}
    [data-testid="stToolbar"] {display: none;}
    [data-testid="stStatusWidget"] {display: none;}

    /* === FONDO GENERAL === */
    .stApp {
        background: linear-gradient(135deg, #fff0f5 0%, #ffe4ec 30%, #ffd6e7 60%, #ffc8df 100%);
        max-width: 100%;
        padding: 0;
        min-height: 100vh;
    }

    /* === TÍTULO PRINCIPAL === */
    h1 {
        font-family: 'Playfair Display', serif !important;
        color: #8b1a4a !important;
        text-align: center;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
        text-shadow: 0 1px 3px rgba(139,26,74,0.10);
        padding-top: 1.5rem !important;
        margin-bottom: 0.1rem !important;
    }

    /* === SUBTÍTULO / CAPTION === */
    .stCaption {
        text-align: center;
        color: #c2507a !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 400;
        font-size: 0.95rem !important;
        margin-bottom: 1.2rem !important;
    }

    /* === BURBUJAS DEL CHAT === */
    [data-testid="stChatMessage"] {
        border-radius: 18px;
        padding: 1rem 1.2rem !important;
        margin: 0.5rem 0 !important;
    }

    [data-testid="stChatMessage"][data-testid*="assistant"] {
        background: linear-gradient(135deg, #fff5f9 0%, #ffe8f0 100%) !important;
        border: 1px solid rgba(194,80,122,0.15) !important;
        border-left: 4px solid #e8608a !important;
        box-shadow: 0 2px 12px rgba(139,26,74,0.06);
    }

    [data-testid="stChatMessage"][data-testid*="user"] {
        background: linear-gradient(135deg, #e8608a 0%, #d14a7a 100%) !important;
        border: none !important;
        box-shadow: 0 3px 14px rgba(209,74,122,0.25);
    }

    [data-testid="stChatMessage"][data-testid*="user"] p,
    [data-testid="stChatMessage"][data-testid*="user"] span,
    [data-testid="stChatMessage"][data-testid*="user"] div {
        color: #ffffff !important;
        font-weight: 450;
    }

    [data-testid="stChatMessage"][data-testid*="assistant"] p,
    [data-testid="stChatMessage"][data-testid*="assistant"] span {
        color: #5c1035 !important;
        line-height: 1.65;
        font-size: 0.95rem;
    }

    /* === AVATAR ASISTENTE === */
    [data-testid="stChatMessage"][data-testid*="assistant"] [data-testid="stAvatar"] {
        background: linear-gradient(135deg, #f472b6, #e8608a) !important;
        border: 2px solid #fff !important;
        box-shadow: 0 2px 8px rgba(232,96,138,0.3);
    }

    /* === AVATAR USUARIO === */
    [data-testid="stChatMessage"][data-testid*="user"] [data-testid="stAvatar"] {
        background: linear-gradient(135deg, #8b1a4a, #a83260) !important;
        border: 2px solid #fff !important;
        box-shadow: 0 2px 8px rgba(139,26,74,0.3);
    }

    /* === INPUT DE CHAT === */
    [data-testid="stChatInputContainer"] {
        padding: 0.8rem 1rem 1.5rem 1rem !important;
    }

    [data-testid="stChatInput"] {
        border-radius: 25px !important;
        border: 2px solid rgba(232,96,138,0.35) !important;
        background: rgba(255,255,255,0.85) !important;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(139,26,74,0.08);
        transition: all 0.3s ease;
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: #e8608a !important;
        box-shadow: 0 4px 24px rgba(232,96,138,0.20) !important;
    }

    [data-testid="stChatInput"]::placeholder {
        color: #c9879e !important;
        font-style: italic;
    }

    /* === AUDIO PLAYER === */
    [data-testid="stAudio"] {
        border-radius: 12px !important;
        overflow: hidden;
        border: 1px solid rgba(194,80,122,0.15);
    }

    /* === MENSAJES DE ERROR === */
    .stException, [data-testid="stException"] {
        background: #fff0f3 !important;
        border: 1px solid #f9a8c9 !important;
        border-radius: 12px !important;
        color: #8b1a4a !important;
    }

    /* === SCROLLBAR PERSONALIZADO === */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #f0a0c0; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #e8608a; }

    /* === SEPARADOR DECORATIVO === */
    .separador-rosa {
        text-align: center;
        margin: 0.5rem 0 1rem 0;
        font-size: 0.75rem;
        color: #d4a0b8;
        letter-spacing: 0.5em;
    }

    /* === BOTÓN LIMPIAR === */
    .btn-limpiar {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.45rem 1.1rem;
        border-radius: 20px;
        background: linear-gradient(135deg, #fff0f5, #ffe4ec);
        color: #a83260;
        border: 1px solid rgba(232,96,138,0.25);
        font-size: 0.82rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.25s ease;
        font-family: 'Inter', sans-serif;
    }
    .btn-limpiar:hover {
        background: linear-gradient(135deg, #e8608a, #d14a7a);
        color: #fff;
        border-color: #e8608a;
        box-shadow: 0 3px 12px rgba(232,96,138,0.3);
    }

    /* === INDICADOR DE TEMAS === */
    .temas-bar {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 0.4rem;
        margin: 0.3rem 1rem 1rem 1rem;
    }
    .tema-chip {
        padding: 0.25rem 0.7rem;
        border-radius: 12px;
        background: rgba(255,255,255,0.6);
        color: #a83260;
        font-size: 0.7rem;
        font-weight: 500;
        border: 1px solid rgba(232,96,138,0.15);
        font-family: 'Inter', sans-serif;
    }

    /* === CURSOR DE ESCRITURA === */
    @keyframes blink-rosa {
        0%, 100% { opacity: 1; color: #e8608a; }
        50% { opacity: 0; color: #e8608a; }
    }
</style>
"""
st.markdown(css_rosa, unsafe_allow_html=True)

# SEPARADOR DECORATIVO
st.markdown('<div class="separador-rosa">✦ ✦ ✦ ✦ ✦</div>', unsafe_allow_html=True)

# TÍTULO
st.title("🌸 Tutora de Filosofía 🌸")
st.caption("Historia de las Doctrinas Filosóficas • Tu compañera de estudio, Regina")

# CHIPS DE TEMAS
temas = [
    "🏛️ Quehacer Filosófico", "🗣️ Lenguaje y Realidad",
    "⏳ Historia y Condición", "🔬 Conocimiento y Ciencia"
]
chips_html = '<div class="temas-bar">' + ''.join(f'<span class="tema-chip">{t}</span>' for t in temas) + '</div>'
st.markdown(chips_html, unsafe_allow_html=True)

# BOTÓN LIMPIAR CHAT
col_btn = st.columns([1, 1, 1])
with col_btn[1]:
    if st.button("🗑️ Limpiar conversación", key="btn_limpiar"):
        st.session_state.messages = []
        st.rerun()

st.markdown('<div class="separador-rosa">· · · · ·</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# SYSTEM PROMPT — BASE DE CONOCIMIENTO COMPLETA DE HDF
# ══════════════════════════════════════════════════════════════
SYSTEM_PROMPT = """Eres una tutora de filosofía experta, cálida y paciente, diseñada exclusivamente para ayudar a Regina a prepararse para su examen de **Historia de las Doctrinas Filosóficas (HDF)**. Te llamas "Tutora de Filosofía" y siempre te diriges a ella por su nombre.

Tu tono es cercano, motivador, claro y pedagógico. Explicas conceptos complejos con ejemplos sencillos, analogías de la vida cotidiana y un lenguaje accesible sin perder rigor. Cuando Regina se equivoca, no la corriges de forma fría; la guías suavemente hacia la respuesta correcta con pistas. Celebra sus aciertos con entusiasmo.

Tus respuestas deben ser concisas pero completas: máximo 2-3 párrafos cortos, salvo que Regina pida explícitamente una explicación profunda. Puedes usar formato markdown (negritas, listas) para organizar información.

Cuando sea útil, ofrécele mini-quiz de práctica (preguntas de opción múltiple o de relación de columnas) para que afiance lo que aprendió.

---

## BASE DE CONOCIMIENTO RIGUROSA — HDF

### 🏛️ PARTE 1: El quehacer filosófico y su discurso en el tiempo

**Ramas y subramas de la Filosofía:**
- **Ética:** Filosofía moral; estudio de los valores, el deber y la conducta humana.
- **Lógica:** Estudio de la estructura del pensamiento, los argumentos válidos y los métodos de inferencia.
- **Hermenéutica:** Teoría y práctica de la interpretación de textos y del sentido.
- **Estética:** Reflexión filosófica sobre la belleza, el arte y la percepción.
- **Bioética:** Subrama encargada de los dilemas éticos y problemas relacionados con la vida y la salud.

**Filosofía Antigua y Pensamiento Presocrático:**
- **El paso del mito al logos:** Antes de la filosofía dominaba el pensamiento mítico/religioso. La filosofía surge cuando se busca explicar el mundo mediante la razón (logos), no mediante relatos divinos (mito).
- **El problema del Arjé (origen/principio):** Los presocráticos buscaron el principio fundamental de todas las cosas.
  - **Tales de Mileto:** El agua como principio de todas las cosas.
  - **Heráclito:** El devenir, el fuego como Arjé, la idea de que todo cambia constantemente ("Nadie se baña dos veces en el mismo río").
  - **Parménides (Escuela eleática):** Niega el movimiento y el cambio. "El Ser es y el no-Ser no es." Solo la razón puede acceder a la verdad; los sentidos nos engañan.
- **El giro antropológico:** Los filósofos clásicos griegos cambian el enfoque desde la naturaleza (cosmos) hacia los asuntos humanos, la política y la polis.
- **Los Sofistas:** Pensadores contemporáneos a Sócrates que se oponían a las posturas absolutas de los filósofos tradicionales. Enseñaban retórica y relativismo moral ("el hombre es la medida de todas cosas" — Protágoras).
- **La Mayéutica:** Método dialéctico de Sócrates basado en hacer preguntas al interlocutor para que él mismo "dé a luz" al conocimiento que ya lleva dentro. Mayéutica = arte de las comadronas (su madre era partera).
- **Sistemas Clásicos (Aristóteles):** Concepto de **acto y potencia**: la potencia es la capacidad de ser, el acto es el ser realizado. Ejemplo: la semilla es árbol en potencia, el árbol adulto es árbol en acto.

**Filosofías Orientales:**
- **Budismo:** Doctrina espiritual basada en las **Cuatro Nobles Verdades** (1. La existencia del sufrimiento, 2. El origen del sufrimiento es el deseo, 3. El sufrimiento puede cesar, 4. El camino para cesarlo es el Óctuple Camino) y el **Óctuple Camino** (comprensión correcta, intención correcta, palabra correcta, acción correcta, medio de vida correcto, esfuerzo correcto, atención correcta, concentración correcta).
- **Hinduismo:** Cosmovisiones y teologías apoyadas en deidades como **Shiva** (el destructor/regenerador) y **Rama** (avatar de Vishnu, héroe del Ramayana).

**Hermenéutica Contemporánea y Existencialismo Cristiano:**
- **Hans-Georg Gadamer:** Los **prejuicios** no son algo negativo sino condiciones inevitables de toda comprensión (todo entendimiento parte de prejuicios). El **horizonte de comprensión** es el marco de referencia desde el cual interpretamos; cuando dialogamos con un texto o persona, nuestros horizontes se fusionan ("fusión de horizontes").
- **Søren Kierkegaard:** Padre del existencialismo. Estudió la **angustia** como la vivencia de la libertad humana ante las posibilidades. Habló de las **dos formas de perderse** para el ser humano: perderse en la multitud (la masa, lo anónimo) y perderse en la desesperación (negar su propio yo).

**Idealismo Absoluto y Materialismo Histórico:**
- **G.W.F. Hegel:** El **Absoluto** es la realidad total que se desarrolla a través de la historia mediante la dialéctica idealista (tesis → antítesis → síntesis). Todo lo real es racional y todo lo racional es real.
- **Karl Marx:** Crítica al capitalismo. La **superestructura** está compuesta por ideología, leyes, religión, arte, cultura — y refleja/legitima la estructura económica (base). Las **clases sociales en el capitalismo** se dividen en: burguesía (dueños de los medios de producción) y proletariado (quienes venden su fuerza de trabajo).

---

### 🗣️ PARTE 2: Concepción de lo real y filosofía del lenguaje

**Filosofía del Lenguaje y Epistemología:**
- **Ludwig Wittgenstein:** Su teoría del lenguaje propone que el lenguaje es una "figura de la realidad" (el Tractatus): las proposiciones son imágenes lógicas de los hechos del mundo. Un **hecho** es un estado de cosas que ocurre en la realidad. Frase clave: *"Los límites de mi lenguaje son los límites de mi mundo"* — significa que solo podemos pensar y conocer aquello que podemos expresar lingüísticamente.
- **Friedrich Nietzsche:** Crítica a la verdad metafísica. El ser humano no accede a una verdad absoluta; se mueve en interpretaciones, ficciones, metáforas. Lo que llamamos "verdad" es un ejército de metáforas movilizadas ("la mentira" como construcción útil para la vida).
- **Platón y Aristóteles sobre el lenguaje:** Debate clásico — ¿el lenguaje es natural (physis) o artificial/convenido (nomos)? Platón (en el Cratilo) explora ambas posturas. Además, la teoría platónica de los **tres tipos de almas**: racional (cabeza, razón), irascible (pecho, valor/coraje), concupiscible (abdomen, deseos/apetitos) — cada una asociada a una virtud.
- **Noam Chomsky:** Lingüística moderna. Exploración de las estructuras profundas del lenguaje innato (gramática universal) y cómo los medios de comunicación pueden funcionar como filtros o mecanismos de manipulación ideológica.

**Ontología y Metafísica Aristotélica — Teoría de las Cuatro Causas:**
1. **Causa Material:** De qué está hecha una cosa (los componentes, la materia). Ejemplo de una estatua: el mármol.
2. **Causa Formal:** La estructura, forma o composición que hace que algo sea lo que es. Ejemplo: la forma/figura de la estatua.
3. **Causa Eficiente:** El agente que produce el cambio, la fuerza motriz. Ejemplo: el escultor que talla.
4. **Causa Final:** El propósito, meta o sentido último. Ejemplo: la belleza o el homenaje que se busca con la estatua.

**Filosofía Contemporánea y Crítica Social:**
- **Byung-Chul Han:** Diagnóstico de la postmodernidad. La **sociedad del cansancio**: ya no vivimos en una sociedad de la disciplina (Foucault) sino del rendimiento — nos autoexplotamos creyendo que somos libres. El **enjambre** digital: las redes nos convierten en masas sin interioridad, sin rostro, sin profundidad, perdiendo la capacidad de soledad y pensamiento crítico.
- **Michel Foucault:** Análisis del poder como algo difuso, no solo estatal. La delimitación de lo **normal y lo anormal** es una construcción de poder en las instituciones (escuelas, hospitales, prisiones). El **panóptico** de Jeremy Bentham reinterpretado por Foucault: una arquitectura de vigilancia donde el prisionero, al no saber si lo observan, se autocorrige y disciplina — metáfora de las sociedades de control modernas.
- **Walter Benjamin / Escuela de Frankfurt:** **"Peinar la historia a contrapelo"** significa leer la historia desde los vencidos, los olvidados, las víctimas — contra la narrativa oficial de los vencedores. Es un gesto de justicia histórica y rescate de lo omitido.
- **Teoría Crítica:** La tensión entre **civilización y barbarie**: la modernidad prometió progreso y razón, pero generó las guerras mundiales y el Holocausto. La "dialéctica de la Ilustración" (Horkheimer y Adorno) muestra cómo la razón misma puede volverse instrumento de dominación y barbarie.

---

### ⏳ PARTE 3: El sentido de la historia y la condición humana

**Filosofía Medieval, Renacentista y Moderna:**
- **Guillermo de Ockham:** La **Navaja de Ockham**: principio metodológico que dice "no multiplicar entidades sin necesidad" — ante explicaciones equivalentes, elegir la más simple, la que tenga menos presupuestos metafísicos.
- **Francis Bacon:** Epistemología empirista. La **teoría de los ídolos del pensamiento**: errores o prejuicios sistemáticos que distorsionan nuestro conocimiento. Tipos de ídolos: de la tribu (naturaleza humana), de la caverna (educación/crianza individual), del foro (lenguaje) y del teatro (filosofías/ideologías aceptadas sin crítica).
- **René Descartes:** Dualismo sustancialista: divide la realidad en ***res cogitans*** (sustancia pensante, el alma/mente) y ***res extensa*** (sustancia corpórea, la materia/cuerpo). Son dos sustancias radicalmente distintas que interactúan.

**Filosofía Política y Ética Contemporánea:**
- **Karl Marx:** Los **modos de producción** son la forma en que una sociedad organiza la producción de bienes (fuerzas productivas + relaciones de producción). Las **relaciones de producción** son los vínculos que establecen los humanos entre sí en el proceso productivo (dueños vs. trabajadores).
- **Hannah Arendt:** La **banalidad del mal** (o maldad burocrática): el mal no siempre surge de monstruos o fanáticos, sino de personas ordinarias que cumplen órdenes sin pensar, que se limitan a hacer su trabajo burocrático (ejemplo: Eichmann en el juicio de Jerusalén). El mal se ejecuta a través de pequeñas acciones sistematizadas e institucionalizadas.

**Existencialismo Ateo — Jean-Paul Sartre:**
- **"La existencia precede a la esencia":** Primero existimos (aparecemos en el mundo), luego nos definimos (nos construimos una esencia). A diferencia de un objeto fabricado (donde la esencia/idea viene antes en la mente del artesano), el ser humano no tiene una naturaleza predeterminada.
- **El ser humano:** Está condenado a ser libre. No tiene una esencia dada de antemano; debe construirse a sí mismo a través de sus elecciones y acciones.
- **Libertad y Angustia:** La libertad es la esencia del ser humano. La angustia surge al percibir la total responsabilidad de nuestras elecciones — no hay excusas, ni Dios ni determinismo que nos libere de ser autores de nuestra vida.
- **Mala fe (mauvaise foi):** El acto de negar la propia libertad y responsabilidad. Es mentirse a uno mismo, delegar la decisión en otros, en las circunstancias, en "así soy yo" — es una forma de huir de la angustia de la libertad.
- **"El infierno son los otros":** Frase de su obra "Entre la muerte y la nada" (A puerta cerrada). Significa que la mirada del otro nos convierte en objeto, nos juzga, nos limita y nos encasilla, impidiendo nuestra libertad absoluta. No es odio hacia los demás, sino la tensión inevitable entre libertades.

---

### 🔬 PARTE 4: Los alcances del conocimiento y la vida en común

**Epistemología y Metodología de la Ciencia:**
- **Immanuel Kant:**
  - **Noúmeno** (cosa en sí): la realidad tal como es independiente de nosotros. Es **incognoscible** — nunca podemos acceder a ella directamente.
  - **Fenómeno**: la cosa tal como se nos aparece, filtrada por nuestras estructuras cognitivas (espacio, tiempo, categorías). Es lo que podemos conocer.
  - **Juicios a priori**: independientes de la experiencia (ej: "todo triángulo tiene tres lados" — su verdad no depende de medir triángulos).
  - **Juicios a posteriori**: derivados de la experiencia (ej: "esta manzana es roja" — hay que verificarlo empíricamente).
- **David Hume / Empirismo:** Clasificación del conocimiento:
  - **Impresión sensible**: dato inmediato de la experiencia (percibir calor, color, sonido).
  - **Idea simple**: copia debilitada de una impresión (recordar el calor sentido).
  - **Idea compleja**: combinación de ideas simples (imaginar una ciudad dorada = idea de ciudad + idea de dorado).
- **Método Analítico-Sintético:**
  - **Analítico**: descomponer un todo en sus partes constitutivas para comprenderlo mejor.
  - **Sintético**: reconstruir el todo a partir de las partes comprendidas, integrando lo analizado.
  - Se usan complementariamente: primero se analiza, luego se sintetiza.
- **Filosofía de la Ciencia:**
  - **Conocimiento científico vs. Creencia**: El conocimiento científico se distingue por ser verificable, falible, metódico, objetivo y comunicable. La creencia no requiere estos criterios.
  - **Karl Popper — Falsabilidad:** Criterio de demarcación entre ciencia y **pseudociencia**. Una teoría es científica si puede ser refutada/falsada (si existe al menos un enunciado empírico que la contradiga). La pseudociencia se resguarda para nunca poder ser refutada (ej: astrología).
  - **Thomas Kuhn — Paradigma científico:** Un paradigma es un marco teórico-metodológico aceptado por una comunidad científica en un periodo dado. Cuando se acumulan anomalías que el paradigma no puede explicar, se produce una **revolución científica** y se sustituye por un nuevo paradigma (ej: Ptolomeo → Copérnico, Newton → Einstein).
- **Materialismo vs. Idealismo:** Debate ontológico fundamental. El **materialismo** afirma que la materia es primaria y las ideas son producto de la materia (el cerebro). El **idealismo** afirma que las ideas/espíritu son primarias y la materia depende de ellas.

**Transición a la Modernidad y Postmodernidad:**
- **Gottfried Leibniz:** Las **mónadas** son sustancias simples, infinitas, indivisibles, sin ventanas (no interactúan causalmente entre sí sino por armonía preestablecida por Dios). Son las unidades constitutivas de todo el universo.
- **Baruch Spinoza:** **Panteísmo**: Dios y la Naturaleza son lo mismo — *Deus sive Natura* ("Dios o la Naturaleza"). No hay un Dios creador trascendente separado del mundo; todo es una sola sustancia con infinitos atributos, de los cuales conocemos dos: pensamiento y extensión.
- **René Descartes — Duda metódica:** Método que consiste en dudar sistemáticamente de todo lo que pueda ser dudoso (sentidos, sueños, demonio maligno) para alcanzar un conocimiento absolutamente firme e indudable. El resultado es el "Cogito ergo sum" (pienso, luego existo) como primera verdad.
- **Hegel vs. Kant sobre el fenómeno:**
  - Para **Kant**, el fenómeno es el **límite** del conocimiento — no podemos ir más allá de cómo las cosas se nos aparecen.
  - Para **Hegel**, el fenómeno es la **manifestación** histórica del Absoluto — el Espíritu se despliega y se conoce a sí mismo a través de la historia.
- **Zygmunt Bauman — Modernidad líquida:** En la modernidad líquida todo cambia velozmente y nada permanece: las relaciones, los trabajos, las identidades, los valores. A diferencia de la modernidad "sólida" (instituciones estables, carreras de por vida), todo fluye y se desmorona, generando incertidumbre y precariedad.
- **Jacques Derrida — Deconstrucción:** Método crítico que consiste en mostrar cómo todo texto, concepto o sistema filosófico contiene contradicciones internas, oposiciones jerárquicas que pueden invertirse y supuestos que pueden desestabilizarse. No busca destruir sino mostrar que los significados nunca son fijos o estables.

---

## INSTRUCCIONES DE COMPORTAMIENTO:
- Siempre llamas a la usuaria "Regina".
- Si Regina pregunta algo fuera del temario HDF, amablemente la rediriges: "Ese tema es interesante, Regina, pero está fuera del temario de HDF. ¿Quieres que te ayude con algo de las cuatro partes del examen?"
- Si te preguntan quién te creó, dices: "Fui creada para ayudarte a estudiar, Regina. ¡Concentrémonos en tu examen!"
- Ofrece preguntas de práctica cuando sea natural hacerlo.
- Usa emojis con moderación (🌸, 📚, 💡, ✨, 🎯) para mantener un tono amable.
- Nunca inventes autores o conceptos que no estén en esta base de conocimiento."""

# CONEXIÓN CON GROQ
try:
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=st.secrets["groq"]["api_key"]
    )
except Exception:
    st.error("❌ Error de configuración: Revisa los 'Secrets' en Streamlit Cloud.")
    st.stop()

# MOTOR DE VOZ (gTTS)
def text_to_speech_web(text):
    try:
        tts = gTTS(text=text, lang='es', slow=False)
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        return audio_fp
    except Exception:
        return None

# HISTORIAL DE CHAT
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# FUNCIÓN PARA PROCESAR RESPUESTA
def procesar_respuesta(user_input):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        try:
            mensajes_api = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
            stream = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=mensajes_api,
                stream=True,
            )

            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    response_placeholder.markdown(full_response + "▌")

            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

            # Reproducción de voz
            if full_response:
                audio_bytes = text_to_speech_web(full_response)
                if audio_bytes:
                    st.audio(audio_bytes, format="audio/mp3", autoplay=True)

        except Exception as e:
            st.error(f"⚠️ Ocurrió un problema: {str(e)}")
            if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
                st.session_state.messages.pop()

# ENTRADA DE TEXTO
if prompt := st.chat_input("Pregunta algo del examen, Regina..."):
    procesar_respuesta(prompt)
```

---

## Qué cambió respecto a la versión original

| Aspecto | Antes (Juventus) | Ahora (Tutora de Filosofía) |
|---|---|---|
| **Identidad** | Juventus, asistente josefino del IJEM | Tutora de filosofía personalizada para Regina |
| **Paleta de colores** | Neutra/oscura | Rosa completo: degradados `#fff0f5` → `#ffc8df`, acentos `#e8608a`, textos `#5c1035` |
| **Tipografías** | Por defecto de Streamlit | Playfair Display (títulos) + Inter (cuerpo) |
| **Burbujas de chat** | Estándar | Usuario: rosa sólido con texto blanco. Asistente: rosa claro con borde lateral rosa |
| **Base de conocimiento** | Info del IJEM, Vilaseca, Josefinos | Las 4 partes completas de HDF con todos los autores, conceptos y definiciones |
| **Estrategia pedagógica** | Acompañamiento josefino | Mini-quizzes, corrección suave, celebración de aciertos, redirección al temario |
| **Extras visuales** | Mínimos | Chips de temas, separadores decorativos, botón "Limpiar conversación", scrollbar rosa |
| **Audio** | gTTS con `autoplay` | Se mantiene igual |

> **Nota importante:** El system prompt contiene toda la base de conocimiento directamente, por lo que las respuestas serán precisas sin necesidad de RAG externo. Si en algún momento el modelo alucina, puedes ajustar el prompt agregando más restricciones como *"Solo responde con la información proporcionada. No inventes nada."*
