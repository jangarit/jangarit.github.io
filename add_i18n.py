import os
import re
import csv
import html

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILES_TO_PROCESS = [
    'index.html',
    'work.html',
    'about.html',
    os.path.join('projects', 'templateslug.html')
]

LANGBAR_SNIPPET = """                <div class="langbar">
                  <a href="#" class="nav-link lang w-nav-link" data-lang-select="es" onclick="setLang('es'); return false;">ES</a>
                  <div href="#" class="nav-bar-social-link lang"><img alt="" src="images/LangIcon.svg"></div>
                  <a href="#" class="nav-link lang w-nav-link" data-lang-select="en" onclick="setLang('en'); return false;">EN</a>
                </div>"""

# Load CSV Translations
CSV_FILE = os.path.join(BASE_DIR, 'Proyectos WEB Jangaritb - about.csv')
index_hero_es = ""
index_hero_en = ""
bio_text1_es = ""
bio_text1_en = ""
bio_text2_es = ""
bio_text2_en = ""
esc_es = ""
esc_en = ""
esc_bio1_es = ""
esc_bio1_en = ""
esc_bio2_es = ""
esc_bio2_en = ""

header_events_es = "Eventos y Exhibiciones"
header_events_en = "Events and Exhibits"
header_distinciones_es = "Distinciones"
header_distinciones_en = "Distinctions"
header_publicaciones_es = "Publicaciones"
header_publicaciones_en = "Publications"

def clean_csv_value(val):
    """Clean up residual CSV double-quote escaping and normalize."""
    val = val.strip()
    # Strip wrapping literal quotes left over from CSV
    if val.startswith('"') and val.endswith('"'):
        val = val[1:-1]
    # Replace residual doubled quotes from CSV escaping: "" -> "
    val = val.replace('""', '"')
    return val

if os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        row = next(reader)
        
    index_hero_es = clean_csv_value(row.get('IndexHero-es', ''))
    index_hero_en = clean_csv_value(row.get('IndexHero-en', ''))
    
    match_es = re.search(r'<h1[^>]*>(.*)</h1>', index_hero_es, flags=re.DOTALL)
    match_en = re.search(r'<h1[^>]*>(.*)</h1>', index_hero_en, flags=re.DOTALL)
    if match_es and match_en:
        esc_es = html.escape(match_es.group(1).strip())
        esc_en = html.escape(match_en.group(1).strip())
        
    esc_bio1_es = html.escape(row.get('BioText1-es', '').strip()).replace('\n', '<br>')
    esc_bio1_en = html.escape(row.get('BioText1-en', '').strip()).replace('\n', '<br>')
    esc_bio2_es = html.escape(row.get('BioText2-es', '').strip()).replace('\n', '<br>')
    esc_bio2_en = html.escape(row.get('BioText2-en', '').strip()).replace('\n', '<br>')

    # Parse Headers (They might have different names in the CSV row vs what we want to fallback to)
    val = row.get('Events and Exhibits-es')
    if val: header_events_es = html.escape(val.strip().split('\n')[0])
    val = row.get('Events and Exhibits-en')
    if val: header_events_en = html.escape(val.strip().split('\n')[0])
    
    val = row.get('Distinciones-es')
    if val: header_distinciones_es = html.escape(val.strip().split('\n')[0])
    val = row.get('Distinciones-en')
    if val: header_distinciones_en = html.escape(val.strip().split('\n')[0])
    
    val = row.get('Publicaciones-es')
    if val: header_publicaciones_es = html.escape(val.strip().split('\n')[0])
    val = row.get('Publicaciones-en')
    if val: header_publicaciones_en = html.escape(val.strip().split('\n')[0])

def process_html_file(filepath):
    print(f"Processing {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update langbar in the navbar
    content = re.sub(
        r'<div class="langbar">.*?<a [^>]*>[eE][nN]</a>\s*</div>',
        LANGBAR_SNIPPET,
        content,
        flags=re.DOTALL
    )
    
    if 'data-lang-select' not in content:
        content = re.sub(
            r'(<a href="[^"]*about\.html"[^>]*>.*?</a>\s*)(</nav>)',
            r'\1' + LANGBAR_SNIPPET + r'\n              \2',
            content,
            flags=re.DOTALL
        )

    # 2. Add script tag at the end of body
    script_src = "js/i18n.js"
    if 'projects' in filepath:
        script_src = "../js/i18n.js"
        content = content.replace('src="images/LangIcon.svg"', 'src="../images/LangIcon.svg"')
        
    script_tag = f'<script src="{script_src}"></script>\n</body>'
    if script_src not in content:
        content = content.replace('</body>', script_tag)

    # 3. Add data-lang-es / en attributes
    nav_replacements = {
        'Inicio': 'Home',
        'Proyectos': 'Projects',
        'Contacto': 'Contact',
        'Sobre mA-': 'About',
        'Sobre mí': 'About'
    }
    for es, en in nav_replacements.items():
        def replacer(match):
            attrs = match.group(1)
            if 'data-lang-es=' not in attrs:
                return f'{attrs} data-lang-es="{es}" data-lang-en="{en}">\g<3>'
            return match.group(0)
            
        content = re.sub(
            f'(<div class="nav-text[^>]*)(>)({es})',
            replacer,
            content
        )

    # Forms & Text
    def repl(pattern, replacement, text):
        regex_pattern = re.escape(pattern).replace(r'\ ', r'\s+')
        return re.sub(regex_pattern, replacement, text)

    content = repl(
        '<input class="input w-input" maxlength="256" name="entry.2005620554" data-name="entry.2005620554" placeholder="Tu nombre  " type="text" id="entry.2005620554" required="">',
        '<input class="input w-input" maxlength="256" name="entry.2005620554" data-name="entry.2005620554" placeholder="Tu nombre  " data-lang-es-placeholder="Tu nombre  " data-lang-en-placeholder="Your name" type="text" id="entry.2005620554" required="">',
        content
    )
    content = repl(
        '<input class="input w-input" maxlength="256" name="emailAddress" data-name="emailAddress" placeholder="Tu correo" type="email" id="emailAddress" required="">',
        '<input class="input w-input" maxlength="256" name="emailAddress" data-name="emailAddress" placeholder="Tu correo" data-lang-es-placeholder="Tu correo" data-lang-en-placeholder="Your email" type="email" id="emailAddress" required="">',
        content
    )
    content = repl(
        '<input class="input w-input" maxlength="256" name="entry.1022456070" data-name="entry.1022456070" placeholder="Tu telAcfono " type="tel" id="entry.1022456070">',
        '<input class="input w-input" maxlength="256" name="entry.1022456070" data-name="entry.1022456070" placeholder="Tu telAcfono " data-lang-es-placeholder="Tu telAcfono " data-lang-en-placeholder="Your phone" type="tel" id="entry.1022456070">',
        content
    )
    content = repl(
        '<input class="input w-input" maxlength="256" name="entry.1022456070" data-name="entry.1022456070" placeholder="Tu teléfono " type="tel" id="entry.1022456070">',
        '<input class="input w-input" maxlength="256" name="entry.1022456070" data-name="entry.1022456070" placeholder="Tu teléfono " data-lang-es-placeholder="Tu teléfono " data-lang-en-placeholder="Your phone" type="tel" id="entry.1022456070">',
        content
    )
    content = repl(
        '<textarea id="entry.839337160" name="entry.839337160" maxlength="5000" data-name="entry.839337160" placeholder="ACA3mo podemos ayudarte?" required="" class="input text-area w-input"></textarea>',
        '<textarea id="entry.839337160" name="entry.839337160" maxlength="5000" data-name="entry.839337160" placeholder="ACA3mo podemos ayudarte?" data-lang-es-placeholder="ACA3mo podemos ayudarte?" data-lang-en-placeholder="How can we help you?" required="" class="input text-area w-input"></textarea>',
        content
    )
    content = repl(
        '<textarea id="entry.839337160" name="entry.839337160" maxlength="5000" data-name="entry.839337160" placeholder="¿Cómo podemos ayudarte?" required="" class="input text-area w-input"></textarea>',
        '<textarea id="entry.839337160" name="entry.839337160" maxlength="5000" data-name="entry.839337160" placeholder="¿Cómo podemos ayudarte?" data-lang-es-placeholder="¿Cómo podemos ayudarte?" data-lang-en-placeholder="How can we help you?" required="" class="input text-area w-input"></textarea>',
        content
    )
    content = repl(
        '<input type="submit" data-wait="Please wait..." class="submit-button w-button" value="Enviar">',
        '<input type="submit" data-wait="Please wait..." class="submit-button w-button" value="Enviar" data-lang-es-value="Enviar" data-lang-en-value="Send">',
        content
    )
    content = repl(
        '<div class="medium-uppercase-m">Tu mensaje se ha enviado</div>',
        '<div class="medium-uppercase-m" data-lang-es="Tu mensaje se ha enviado" data-lang-en="Your message has been sent">Tu mensaje se ha enviado</div>',
        content
    )
    content = repl(
        '<p class="regular-s">Nos pondremos en contacto contigo lo antes posible.</p>',
        '<p class="regular-s" data-lang-es="Nos pondremos en contacto contigo lo antes posible." data-lang-en="We will contact you as soon as possible.">Nos pondremos en contacto contigo lo antes posible.</p>',
        content
    )
    content = repl(
        '<div class="regular-s">Oops, algo saliA3 mal. IntAcntalo de nuevo.</div>',
        '<div class="regular-s" data-lang-es="Oops, algo saliA3 mal. IntAcntalo de nuevo." data-lang-en="Oops, something went wrong. Try again.">Oops, algo saliA3 mal. IntAcntalo de nuevo.</div>',
        content
    )
    content = repl(
        '<div class="regular-s">Oops, algo salió mal. Inténtalo de nuevo.</div>',
        '<div class="regular-s" data-lang-es="Oops, algo salió mal. Inténtalo de nuevo." data-lang-en="Oops, something went wrong. Try again.">Oops, algo salió mal. Inténtalo de nuevo.</div>',
        content
    )
    content = repl(
        '<label for="entry.2005620554" class="medium-uppercase-xs-black input-label">Nombre</label>',
        '<label for="entry.2005620554" class="medium-uppercase-xs-black input-label" data-lang-es="Nombre" data-lang-en="Name">Nombre</label>',
        content
    )
    content = repl(
        '<label for="entry.1022456070" class="medium-uppercase-xs-black input-label">TelAcfono </label>',
        '<label for="entry.1022456070" class="medium-uppercase-xs-black input-label" data-lang-es="TelAcfono " data-lang-en="Phone ">TelAcfono </label>',
        content
    )
    content = repl(
        '<label for="entry.1022456070" class="medium-uppercase-xs-black input-label">Teléfono </label>',
        '<label for="entry.1022456070" class="medium-uppercase-xs-black input-label" data-lang-es="Teléfono " data-lang-en="Phone ">Teléfono </label>',
        content
    )
    content = repl(
        '<label for="entry.839337160" class="medium-uppercase-xs-black input-label">Mensaje</label>',
        '<label for="entry.839337160" class="medium-uppercase-xs-black input-label" data-lang-es="Mensaje" data-lang-en="Message">Mensaje</label>',
        content
    )
    content = repl(
        '<label for="emailAddress" class="medium-uppercase-xs-black input-label">Email</label>',
        '<label for="emailAddress" class="medium-uppercase-xs-black input-label" data-lang-es="Email" data-lang-en="Email">Email</label>',
        content
    )
    content = repl(
        '<h2 class="display-1 second _5rem">Contacto</h2>',
        '<h2 class="display-1 second _5rem" data-lang-es="Contacto" data-lang-en="Contact">Contacto</h2>',
        content
    )

    # 3b. Project page metadata labels (Cliente, Producción, Año, Software, Descripción)
    metadata_label_translations = {
        'cliente': ('Cliente', 'Client'),
        'Cliente': ('Cliente', 'Client'),
        'Producción': ('Producción', 'Production'),
        'Año': ('Año', 'Year'),
        'Software': ('Software', 'Software'),
        'Descripción': ('Descripción', 'Description'),
    }
    for label_text, (es, en) in metadata_label_translations.items():
        # Only add data-lang attrs if not already present on this element
        def repl_label(m):
            tag = m.group(1)
            if 'data-lang-es=' in tag:
                return m.group(0)  # Already has i18n, skip
            tag_no_close = tag.rstrip('>')
            return f'{tag_no_close} data-lang-es="{es}" data-lang-en="{en}">{label_text}</p>'
        content = re.sub(
            rf'(<p class="subhead-main for-footer-details"[^>]*>)\s*{re.escape(label_text)}\s*</p>',
            repl_label,
            content,
            flags=re.IGNORECASE
        )

    # 4. Specific index and about replacements
    if 'index.html' in filepath and esc_es and esc_en:
        def replace_h1(match):
            tag_open = match.group(1)
            inner = match.group(2)
            # Remove any existing data-lang attributes to ensure a fresh inject
            tag_open = re.sub(r'\s*data-lang-es="[^"]*"', '', tag_open)
            tag_open = re.sub(r'\s*data-lang-en="[^"]*"', '', tag_open)
            
            tag_open_no_close = tag_open[:-1]
            return f'{tag_open_no_close} data-lang-es="{esc_es}" data-lang-en="{esc_en}">{inner}</h1>'
            
        content = re.sub(r'(<h1 id="interText3"[^>]*>)(.*?)(</h1>)', replace_h1, content, flags=re.DOTALL)

    if 'about.html' in filepath and esc_bio1_es and esc_bio1_en:
        def repl_bio1(m):
            t = m.group(1)
            t = re.sub(r'\s*data-lang-es="[^"]*"', '', t)
            t = re.sub(r'\s*data-lang-en="[^"]*"', '', t)
            t_no_close = t[:-1]
            return f'{t_no_close} data-lang-es="{esc_bio1_es}" data-lang-en="{esc_bio1_en}">{m.group(2)}</p>'
            
        content = re.sub(r'(<p id="ProjectText1"[^>]*>)\s*(Diseñador con énfasis.*?)\s*(</p>)', repl_bio1, content, flags=re.DOTALL)
        
        def repl_bio2(m):
            t = m.group(1)
            t = re.sub(r'\s*data-lang-es="[^"]*"', '', t)
            t = re.sub(r'\s*data-lang-en="[^"]*"', '', t)
            t_no_close = t[:-1]
            return f'{t_no_close} data-lang-es="{esc_bio2_es}" data-lang-en="{esc_bio2_en}">{m.group(2)}</p>'
            
        content = re.sub(r'(<p id="ProjectText1"[^>]*>)\s*(Experiencia con fotogrametría.*?)\s*(</p>)', repl_bio2, content, flags=re.DOTALL)

        # Eventos, Distinciones, Publicaciones headers
        # We might have already wrapped them in a span, or they might be raw text inside h1.
        # Let's match the h1 and whatever is inside, and replace it with a fresh span containing the CSV values (if we have them).
        # We should parse the CSV for the headers: "Eventos y Exhibiciones", "Distinciones", "Publicaciones".
        # But wait, in the CSV these are:
        # "Events and Exhibits-es", "Events and Exhibits-en"
        # "Distinciones-es", "Distinciones-en"
        # "Publicaciones-es", "Publicaciones-en"
        
        def repl_header_eventos(m):
            return f'{m.group(1)}<span data-lang-es="{header_events_es}" data-lang-en="{header_events_en}">{header_events_es}</span>{m.group(2)}'
        content = re.sub(r'(<h1 class="subhead-main for-footer-title">)\s*(?:<span[^>]*>)?Eventos y Exhibiciones(?:</span>)?\s*(</h1>)', repl_header_eventos, content)
        
        def repl_header_distinciones(m):
            return f'{m.group(1)}<span data-lang-es="{header_distinciones_es}" data-lang-en="{header_distinciones_en}">{header_distinciones_es}</span>{m.group(2)}'
        content = re.sub(r'(<h1 class="subhead-main for-footer-title">)\s*(?:<span[^>]*>)?Distinciones(?:</span>)?\s*(</h1>)', repl_header_distinciones, content)
        
        def repl_header_publicaciones(m):
            return f'{m.group(1)}<span data-lang-es="{header_publicaciones_es}" data-lang-en="{header_publicaciones_en}">{header_publicaciones_es}</span>{m.group(2)}'
        content = re.sub(r'(<h1 class="subhead-main for-footer-title">)\s*(?:<span[^>]*>)?Publicaciones(?:</span>)?\s*(</h1>)', repl_header_publicaciones, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for f in FILES_TO_PROCESS:
    process_html_file(os.path.join(BASE_DIR, f))
