import csv
import os
import re
import shutil

# Directions
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PENDING_DIR = os.path.join(BASE_DIR, 'projects', 'Pending')
CSV_FILE = os.path.join(BASE_DIR, 'Proyectos WEB Jangaritb - PROYECTOS WEB.csv')
TEMPLATE_FILE = os.path.join(BASE_DIR, 'projects', 'templateslug.html')
INDEX_FILE = os.path.join(BASE_DIR, 'index.html')
PROJECTS_DIR = os.path.join(BASE_DIR, 'projects')

def find_csv_column(row, *candidates):
    """Find a CSV column by trying multiple name candidates.
    Useful when column names contain special characters (ó, ñ) that may
    differ depending on the encoding used to read the file."""
    for name in candidates:
        if name in row:
            return row[name]
    # Fallback: partial match on the key list
    for key in row:
        for name in candidates:
            # Strip accents / special chars and compare lowered substrings
            if name.lower().replace('ó', 'o').replace('ñ', 'n') in key.lower().replace('ó', 'o').replace('ñ', 'n'):
                return row[key]
    return ''

def clean_row_snippet(snippet):
    # The snippet in the CSV uses double double-quotes and some placeholders
    # Let's clean it up for insertion
    snippet = snippet.strip()
    if snippet.startswith('"') and snippet.endswith('"'):
        snippet = snippet[1:-1]
    snippet = snippet.replace('""', '"')
    
    # Fix common typos found in the CSV source data
    snippet = snippet.replace('alt=" "', 'alt=""')
    snippet = snippet.replace('alt=" class=', 'alt="" class=')
    snippet = snippet.replace('workxº-photo', 'work-photo')
    snippet = snippet.replace('thumb")', 'thumb"')
    snippet = snippet.replace('projecttitle', 'worktitle')
    
    return snippet

def generate_projects():
    print("--- Generating Web Projects ---")
    
    if not os.path.exists(CSV_FILE):
        print(f"Error: CSV file not found at {CSV_FILE}")
        return

    if not os.path.exists(TEMPLATE_FILE):
        print(f"Error: Template file not found at {TEMPLATE_FILE}")
        return

    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        template_content = f.read()

    projects_data = []

    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        # Using handle for potential CSV issues (like the snippet containing multiple lines or commas)
        reader = csv.DictReader(f)
        
        for row in reader:
            publish = row.get('Publish', '').upper() == 'TRUE'
            highlight = row.get('Highlight', '').upper() == 'TRUE'
            title = row.get('ProjectTitle-es', '')
            title_en = row.get('ProjectTitle-en', '') or title
            job = row.get('Job', '')
            text1 = row.get('projectText1-es', '')
            text1_en = row.get('projectText1-en', '') or text1
            text2 = row.get('projectText2-es', '')
            text2_en = row.get('projectText2-en', '') or text2
            slug = row.get('slug', '')
            simple_name = row.get('SimpleName', '')  # Image files use this name without number prefix

            
            # Folder handling - be more robust with path prefixes
            folder_val = row.get('Imagesfolder', '')
            # Strip ../ or / or .. prefixes
            folder_rel = re.sub(r'^(\.\./|\/|\.\.)', '', folder_val).rstrip('/')
            folder_path = os.path.join(BASE_DIR, folder_rel)
            
            # Destination: projects/slug.html
            href_rel = f"projects/{slug}.html"
            href_full = os.path.join(BASE_DIR, href_rel)
            
            # Old destination for cleanup - handle variations in CSV href column
            href_csv = row.get('href', '')
            # Clean up potential typos in CSV like ..projects/ instead of ../projects/
            href_csv_clean = re.sub(r'^(\.\./|\.\.|\/)', '', href_csv)
            old_href_rel = href_csv_clean
            old_href_full = os.path.join(BASE_DIR, old_href_rel)
            
            if old_href_full != href_full and os.path.exists(old_href_full):
                try:
                    os.remove(old_href_full)
                    # print(f"Cleaned up old page: {old_href_rel}")
                except Exception as e:
                    print(f"Error removing {old_href_full}: {e}")

            if not publish:
                os.makedirs(PENDING_DIR, exist_ok=True)
                
                if os.path.exists(href_full):
                    pending_html_path = os.path.join(PENDING_DIR, os.path.basename(href_full))
                    if os.path.exists(pending_html_path):
                        os.remove(pending_html_path)
                    shutil.move(href_full, pending_html_path)
                    print(f"Moved unpublished HTML to Pending: {os.path.basename(href_full)}")
                
                if folder_path and os.path.exists(folder_path):
                    pending_folder_path = os.path.join(PENDING_DIR, os.path.basename(folder_path))
                    if os.path.exists(pending_folder_path):
                        shutil.rmtree(pending_folder_path)
                    shutil.move(folder_path, pending_folder_path)
                    print(f"Moved unpublished folder to Pending: {os.path.basename(folder_path)}")
                
                continue

            thumbnail = row.get('thumbnail', '')
            images_str = row.get('Images', '')
            images = [img.strip() for img in images_str.split(',') if img.strip()]
            
            video_links = row.get('Video links', '')
            videos_str = row.get('Videos', '')
            videos = [vid.strip() for vid in videos_str.split(',') if vid.strip()]

            # Determine upfront whether this project has a usable "hero" video,
            # so we know whether image 1 should be reserved for the hero slot
            # (and skipped from the regular image grid) or used normally.
            video_links_list = [v.strip() for v in video_links.replace('\n', ',').split(',') if v.strip()] if video_links else []
            first_video_id = None
            if video_links_list:
                v_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', video_links_list[0])
                if v_match:
                    first_video_id = v_match.group(1)
            video_inserted = first_video_id is not None

            # No video - image 1 goes in the hero slot instead, so pull it out
            # of the regular image list to avoid showing it twice.
            hero_image_name = None
            if not video_inserted and images:
                hero_image_name = images[0]
                images = images[1:]
            
            client = row.get('Cliente/Client', '')
            year = find_csv_column(row, 'Año/Year', 'A\xf1o/Year')
            production = find_csv_column(row, 'Producción/Production', 'Producci\xf3n/Production')
            software = row.get('Software', '')
            
            row_snippet = row.get('row', '')

            # 1. Create Folder
            if publish and folder_rel:
                os.makedirs(folder_path, exist_ok=True)
                # print(f"Folder checked/created: {folder_rel}")

            # 2. Generate Project Page
            page_html = template_content
            
            # Replace Title in head and meta tags
            title_clean = title.replace('"', '&quot;')
            text1_clean = re.sub(r'<[^>]*>', '', text1)
            text1_clean = ' '.join(text1_clean.split()).replace('"', '&quot;')
            
            page_html = re.sub(r'<title>ProjectTitle</title>', f'<title>{title_clean}</title>', page_html)
            page_html = re.sub(r'<meta content="ProjectTitle" property="og:title">', f'<meta content="{title_clean}" property="og:title">', page_html)
            page_html = re.sub(r'<meta content="ProjectTitle" name="twitter:title">', f'<meta content="{title_clean}" name="twitter:title">', page_html)
            page_html = re.sub(r'<meta content="projectText1" name="description">', f'<meta content="{text1_clean}" name="description">', page_html)
            page_html = re.sub(r'<meta content="projectText1" property="og:description">', f'<meta content="{text1_clean}" property="og:description">', page_html)
            page_html = re.sub(r'<meta content="projectText1" name="twitter:description">', f'<meta content="{text1_clean}" name="twitter:description">', page_html)
            
            # Main ID replacements using regex to be more surgical
            title_clean_attr = title.replace('"', '&quot;')
            title_en_clean_attr = title_en.replace('"', '&quot;')
            # Title H1
            page_html = re.sub(r'(<h1 id="ProjectTitle"[^>]*>)(.*?)(</h1>)', rf'\1<span data-lang-es="{title_clean_attr}" data-lang-en="{title_en_clean_attr}">{title}</span>\3', page_html, flags=re.DOTALL)
            # Job H2
            page_html = re.sub(r'(<h2 id="Job"[^>]*>)(.*?)(</h2>)', r'\g<1>' + job + r'\g<3>', page_html, flags=re.DOTALL)
            # Text 1 and 2
            text1_clean_attr = text1.replace('"', '&quot;')
            text1_en_clean_attr = text1_en.replace('"', '&quot;')
            page_html = re.sub(r'(<p id="ProjectText1"[^>]*>)(.*?)(</p>)', rf'\1<span data-lang-es="{text1_clean_attr}" data-lang-en="{text1_en_clean_attr}">{text1}</span>\3', page_html, flags=re.DOTALL)
            
            text2_clean_attr = text2.replace('"', '&quot;')
            text2_en_clean_attr = text2_en.replace('"', '&quot;')
            page_html = re.sub(r'(<p id="ProjectText2"[^>]*>)(.*?)(</p>)', rf'\1<span data-lang-es="{text2_clean_attr}" data-lang-en="{text2_en_clean_attr}">{text2}</span>\3', page_html, flags=re.DOTALL)

            
            # Metadata in the sticky section
            # Cliente
            if client and client.strip():
                page_html = re.sub(r'(<div id="Cliente" class="line-flex"[^>]*>.*?<p class="subhead-main">)(.*?)(</p>.*?</div>)', r'\g<1>' + client + r'\g<3>', page_html, flags=re.DOTALL)
            else:
                page_html = re.sub(r'(<div id="Cliente" class="line-flex")', r'\1 style="display: none;"', page_html)

            # Producción (ID is Producci-n)
            if production and production.strip():
                page_html = re.sub(r'(<div id="Producci-n" class="line-flex"[^>]*>.*?<p class="subhead-main">)(.*?)(</p>.*?</div>)', r'\g<1>' + production + r'\g<3>', page_html, flags=re.DOTALL)
            else:
                page_html = re.sub(r'(<div id="Producci-n" class="line-flex")', r'\1 style="display: none;"', page_html)

            # Año (ID is A-o)
            if year and year.strip():
                page_html = re.sub(r'(<div id="A-o" class="line-flex"[^>]*>.*?<p class="subhead-main">)(.*?)(</p>.*?</div>)', r'\g<1>' + year + r'\g<3>', page_html, flags=re.DOTALL)
            else:
                page_html = re.sub(r'(<div id="A-o" class="line-flex")', r'\1 style="display: none;"', page_html)

            # Software
            if software and software.strip():
                # Replace newlines with <br> for multi-line software lists
                software_html = software.strip().replace('\n', '<br>')
                page_html = re.sub(r'(<div id="Software" class="line-flex"[^>]*>.*?<p class="subhead-main">)(.*?)(</p>.*?</div>)', r'\g<1>' + software_html + r'\g<3>', page_html, flags=re.DOTALL)
            else:
                page_html = re.sub(r'(<div id="Software" class="line-flex")', r'\1 style="display: none;"', page_html)

            # Replace Images
            # subfolder_name is the folder containing images relative to the project page
            # Usually folder_rel is 'projects/foldername', so we just need 'foldername'
            subfolder_name = os.path.basename(folder_rel)
            
            # 1. Handle ProjectImage1 and ProjectImage2 (Grid)
            # We remove srcset because the original images might have different aspect ratios/resolutions
            # and the browser might prefer the original srcset over the new src.
            if len(images) > 0:
                img_path = f"{subfolder_name}/{images[0]}"
                # Update src and remove srcset
                page_html = re.sub(rf'src="[^"]+"([^>]+id="ProjectImage1")', rf'src="{img_path}"\1', page_html)
                page_html = re.sub(rf'srcset="[^"]+"([^>]+id="ProjectImage1")', r'\1', page_html)
            else:
                # Remove the wrapper for ProjectImage1 if no image
                page_html = re.sub(r'<div class="photo-wrapper"><img[^>]+id="ProjectImage1"[^>]*></div>', '', page_html)

            if len(images) > 1:
                img_path = f"{subfolder_name}/{images[1]}"
                # Update src and remove srcset
                page_html = re.sub(rf'src="[^"]+"([^>]+id="ProjectImage2")', rf'src="{img_path}"\1', page_html)
                page_html = re.sub(rf'srcset="[^"]+"([^>]+id="ProjectImage2")', r'\1', page_html)
            else:
                # Remove the wrapper for ProjectImage2 if no image
                page_html = re.sub(r'<div class="photo-wrapper"><img[^>]+id="ProjectImage2"[^>]*></div>', '', page_html)

            # The template ships with two video slots baked in (one hero slot
            # before the images grid, one duplicate right before the 3rd
            # project image). These may be labeled Video-1/Video-2 or both
            # Video-1 depending on how the template was last edited, so match
            # on ANY "Video-N" id rather than assuming a specific number.
            # Rule: the 1st video (if any) stays in the hero slot at the top;
            # the duplicate slot is always dropped; any 2nd+ video is cloned
            # in starting right after the 3rd image (slot 4+).
            ANY_VIDEO_BLOCK_RE = re.compile(r'<div class="photo-wrapper">\s*<div id="Video-\d+".*?</div>\s*</div>', re.DOTALL)
            video_block_match = ANY_VIDEO_BLOCK_RE.search(page_html)
            pristine_video_block = video_block_match.group(0) if video_block_match else None

            if video_inserted:
                page_html = re.sub(r'https://www.youtube.com/embed/[A-Za-z0-9_-]+', f'https://www.youtube.com/embed/{first_video_id}', page_html)

            if not video_inserted:
                # No usable video - put image 1 (reserved above) in the hero
                # slot instead (any other stray video block found is dropped entirely).
                video_block_matches = list(ANY_VIDEO_BLOCK_RE.finditer(page_html))
                if video_block_matches:
                    hero_replacement = ""
                    if hero_image_name:
                        hero_img_path = f"{subfolder_name}/{hero_image_name}"
                        hero_replacement = f'<div class="photo-wrapper"><img alt="" src="{hero_img_path}" loading="eager" class="work-photo-first"></div>'
                    for stray_match in reversed(video_block_matches[1:]):
                        page_html = page_html[:stray_match.start()] + page_html[stray_match.end():]
                    first_match = video_block_matches[0]
                    page_html = page_html[:first_match.start()] + hero_replacement + page_html[first_match.end():]
            else:
                # Keep only the first (hero) video block; any other video block
                # baked into the template is always removed, regardless of its id.
                video_block_matches = list(ANY_VIDEO_BLOCK_RE.finditer(page_html))
                for stray_match in reversed(video_block_matches[1:]):
                    page_html = page_html[:stray_match.start()] + page_html[stray_match.end():]

            # Any 2nd+ video links get cloned from the pristine video block and
            # placed starting at slot 4 - i.e. right after the 3rd project image.
            # Only applies if the hero video was actually inserted successfully.
            additional_videos_html = ""
            if pristine_video_block and video_inserted and len(video_links_list) > 1:
                for idx, extra_video_url in enumerate(video_links_list[1:], start=2):
                    v_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', extra_video_url)
                    if not v_match:
                        continue
                    extra_video_id = v_match.group(1)
                    cloned_block = pristine_video_block
                    # Give each clone a unique id
                    cloned_block = re.sub(r'id="Video-\d+"', f'id="Video-{idx}"', cloned_block)
                    cloned_block = re.sub(r'https://www.youtube.com/embed/[A-Za-z0-9_-]+', f'https://www.youtube.com/embed/{extra_video_id}', cloned_block)
                    additional_videos_html += cloned_block + "\n"

            # 2. Handle ProjectImage3 onwards (Sequential)
            # Image filenames come from CSV and don't have number prefix
            extra_images_html = ""
            for i in range(2, len(images)):
                img_name = images[i]  # e.g., "ascii-sound-experience-3.jpg" (no number prefix)
                img_path = f"{subfolder_name}/{img_name}"  # e.g., "1-ascii-sound-experience/ascii-sound-experience-3.jpg"
                # Added empty srcset to be safe and clean class/loading
                extra_images_html += f'<div class="photo-wrapper"><img alt="" src="{img_path}" loading="eager" class="work-photo-first"></div>\n'
                if i == 2 and additional_videos_html:
                    # Slot 4 onward: drop in any extra videos right after the 3rd image
                    extra_images_html += additional_videos_html

            # Fallback: if there's no 3rd+ image to anchor to, still place the
            # extra videos where the ProjectImage3 placeholder used to be.
            if len(images) <= 2 and additional_videos_html:
                extra_images_html += additional_videos_html

            # Replace the placeholder ProjectImage3 with all subsequent images (and extra videos)
            if extra_images_html:
                page_html = re.sub(r'<div class="photo-wrapper"><img[^>]+id="ProjectImage3"[^>]*></div>', extra_images_html, page_html)
            else:
                # Remove the placeholder if no 3rd+ image
                page_html = re.sub(r'<div class="photo-wrapper"><img[^>]+id="ProjectImage3"[^>]*></div>', '', page_html)

            # Save Page
            if publish and href_full:
                with open(href_full, 'w', encoding='utf-8') as pf:
                    pf.write(page_html)
                print(f"Page generated: {href_rel}")

            if publish:
                projects_data.append({
                    'title': title,
                    'job': job,
                    'href': href_rel,
                    'thumb': f"{folder_rel}/{thumbnail}" if thumbnail else "",
                    'snippet': clean_row_snippet(row_snippet),
                    'title': title,
                    'title_en': title_en,
                    'highlight': highlight
                })

    # 3. Update index.html
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            index_content = f.read()

        # Add START and END markers if missing
        if '<!-- START PROJECTS -->' not in index_content:
            index_content = re.sub(
                r'(<div class="homeprojects">)',
                r'\1\n    <!-- START PROJECTS -->',
                index_content,
                count=1
            )
            
        if '<!-- END PROJECTS -->' not in index_content:
            # Check if section-2 exists
            if 'class="section-2"' in index_content:
                index_content = re.sub(
                    r'(<section [^>]*class="section-2"[^>]*>)',
                    r'<!-- END PROJECTS -->\n    \1',
                    index_content,
                    count=1
                )
            else:
                # Fallback to user's suggested location
                index_content = re.sub(
                    r'(<section class="section">\s*<div class="container-tactil">)',
                    r'<!-- END PROJECTS -->\n  \1',
                    index_content,
                    count=1
                )

        highlighted_projects = [p for p in projects_data if p['highlight']]
        all_rows_html = ""
        for i in range(0, len(highlighted_projects), 2):
            row_projects = highlighted_projects[i:i+2]
            row_html = '    <div class="card-row">\n'
            for proj in row_projects:
                snippet = proj['snippet']
                snippet = snippet.replace('href="#"', f'href="{proj["href"]}"')
                snippet = snippet.replace('src="../', 'src="')
                title_clean = proj['title'].replace('"', '&quot;')
                title_en_clean = proj['title_en'].replace('"', '&quot;')
                snippet = re.sub(r'(<div class="worktitle">)(.*?)(</div>)', rf'\1<span data-lang-es="{title_clean}" data-lang-en="{title_en_clean}">\2</span>\3', snippet, count=1)

                row_html += f'      <div data-w-id="01936ddb-bf34-bbc2-240c-e49d9f55507e" class="work-card-wrapper">\n'
                row_html += f'        <div class="divwork">\n'
                row_html += f'          {snippet}\n'
                row_html += f'        </div>\n'
                row_html += f'      </div>\n'
            row_html += '    </div>'
            all_rows_html += row_html + "\n"

        new_index = re.sub(
            r'<!-- START PROJECTS -->.*?<!-- END PROJECTS -->',
            f'<!-- START PROJECTS -->\n{all_rows_html}    <!-- END PROJECTS -->',
            index_content,
            flags=re.DOTALL
        )

        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            f.write(new_index)
        print("index.html updated.")

    # 4. Update work.html
    WORK_FILE = os.path.join(BASE_DIR, 'work.html')
    if os.path.exists(WORK_FILE):
        with open(WORK_FILE, 'r', encoding='utf-8') as f:
            work_content = f.read()
            
        # Add START and END markers if missing
        if '<!-- START PROJECTS -->' not in work_content:
            work_content = re.sub(
                r'(<div class="collection-list-wrapper.*?>\s*<div class="collection-list.*?>)',
                r'\1\n    <!-- START PROJECTS -->',
                work_content,
                count=1
            )
            
        if '<!-- END PROJECTS -->' not in work_content:
            work_content = re.sub(
                r'(</div>\s*</div>\s*<section class="section">)',
                r'<!-- END PROJECTS -->\n    \1',
                work_content,
                count=1
            )

        all_work_html = ""
        for i in range(0, len(projects_data), 2):
            row_projects = projects_data[i:i+2]
            row_html = '    <div class="card-row">\n'
            for proj in row_projects:
                snippet = proj['snippet']
                snippet = snippet.replace('href="#"', f'href="{proj["href"]}"')
                snippet = snippet.replace('src="../', 'src="')
                title_clean = proj['title'].replace('"', '&quot;')
                title_en_clean = proj['title_en'].replace('"', '&quot;')
                snippet = re.sub(r'(<div class="worktitle">)(.*?)(</div>)', rf'\1<span data-lang-es="{title_clean}" data-lang-en="{title_en_clean}">\2</span>\3', snippet, count=1)
                row_html += f'      <div data-w-id="01936ddb-bf34-bbc2-240c-e49d9f55507e" class="work-card-wrapper">\n'
                row_html += f'        <div class="divwork">\n'
                row_html += f'          {snippet}\n'
                row_html += f'        </div>\n'
                row_html += f'      </div>\n'
            row_html += '    </div>'
            all_work_html += row_html + "\n"

        new_work = re.sub(
            r'<!-- START PROJECTS -->.*?<!-- END PROJECTS -->',
            f'<!-- START PROJECTS -->\n{all_work_html}    <!-- END PROJECTS -->',
            work_content,
            flags=re.DOTALL
        )

        with open(WORK_FILE, 'w', encoding='utf-8') as f:
            f.write(new_work)
        print("work.html updated.")

if __name__ == "__main__":
    generate_projects()