import os
import math
from xml.etree.ElementTree import Element, SubElement, ElementTree

# Base domain
BASE_DOMAIN = 'https://tha.hitools.space'
# Max URLs per sitemap file
MAX_URLS_PER_SITEMAP = 500
# Output folder for sitemaps
SITEMAP_FOLDER = 'sitemaps'


def get_all_html_paths(root_dir):
    html_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.html'):
                full_path = os.path.relpath(os.path.join(dirpath, filename), root_dir)
                html_files.append(full_path.replace(os.sep, '/'))  # for URL-friendly path
    return html_files


def generate_sitemap(urls, file_index):
    urlset = Element('urlset', {
        'xmlns': "http://www.sitemaps.org/schemas/sitemap/0.9"
    })

    for url in urls:
        url_tag = SubElement(urlset, 'url')
        loc = SubElement(url_tag, 'loc')
        loc.text = f"{BASE_DOMAIN}/{url}"

    filename = f"sitemap{file_index}.xml"
    filepath = os.path.join(SITEMAP_FOLDER, filename)
    ElementTree(urlset).write(filepath, encoding='utf-8', xml_declaration=True)
    return filename


def generate_sitemap_index(sitemap_filenames):
    sitemapindex = Element('sitemapindex', {
        'xmlns': "http://www.sitemaps.org/schemas/sitemap/0.9"
    })

    for filename in sitemap_filenames:
        sitemap = SubElement(sitemapindex, 'sitemap')
        loc = SubElement(sitemap, 'loc')
        loc.text = f"{BASE_DOMAIN}/{SITEMAP_FOLDER}/{filename}"

    index_path = os.path.join(SITEMAP_FOLDER, 'sitemap_index.xml')
    ElementTree(sitemapindex).write(index_path, encoding='utf-8', xml_declaration=True)


def main():
    root_dir = os.getcwd()
    os.makedirs(SITEMAP_FOLDER, exist_ok=True)

    html_paths = get_all_html_paths(root_dir)
    if not html_paths:
        print("No HTML files found.")
        return

    num_sitemaps = math.ceil(len(html_paths) / MAX_URLS_PER_SITEMAP)
    sitemap_files = []

    for i in range(num_sitemaps):
        chunk = html_paths[i * MAX_URLS_PER_SITEMAP: (i + 1) * MAX_URLS_PER_SITEMAP]
        filename = generate_sitemap(chunk, i + 1)
        sitemap_files.append(filename)

    generate_sitemap_index(sitemap_files)

    print(f"Generated {len(sitemap_files)} sitemap(s) and sitemap_index.xml in '{SITEMAP_FOLDER}/'")


if __name__ == '__main__':
    main()
