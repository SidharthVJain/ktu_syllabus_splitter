import fitz
import re
import os
import argparse

def extract_course_code(text):
    match = re.search(r"Course Code\s+([A-Z0-9]+)", text)
    if match:
        return match.group(1)
    return None

def apply_watermark(doc):
    assets_dir = os.path.join(os.path.dirname(__file__), "watermark")
    logo_path = os.path.join(assets_dir, "logo.png")
    cover_path = os.path.join(assets_dir, "cover.pdf")
    
    if not os.path.exists(logo_path) or not os.path.exists(cover_path):
        return doc

    cover_doc = fitz.open(cover_path)
    new_doc = fitz.open()
    new_doc.insert_pdf(doc)
    new_doc.insert_pdf(cover_doc, from_page=0, to_page=0)
    
    logo_pix = fitz.Pixmap(logo_path)
    if logo_pix.n < 4:
        logo_pix = fitz.Pixmap(fitz.csRGB, logo_pix)
    if not logo_pix.alpha:
        logo_pix = fitz.Pixmap(logo_pix, 1)
        
    samples = bytearray(logo_pix.samples)
    for i in range(3, len(samples), 4):
        samples[i] = int(samples[i] * 0.15)
    logo_pix = fitz.Pixmap(logo_pix.colorspace, logo_pix.width, logo_pix.height, samples, logo_pix.alpha)
    
    footer_text = "Downloaded from KTUNOTES.LIVE"
    footer_link = "https://ktunotes.live"
    
    for i in range(len(new_doc) - 1):
        page = new_doc[i]
        rect = page.rect
        
        logo_aspect = logo_pix.width / logo_pix.height
        max_size = min(rect.width, rect.height) * 0.45
        
        if logo_aspect > 1:
            logo_w = max_size
            logo_h = max_size / logo_aspect
        else:
            logo_h = max_size
            logo_w = max_size * logo_aspect
            
        logo_x = (rect.width - logo_w) / 2
        logo_y = (rect.height - logo_h) / 2
        img_rect = fitz.Rect(logo_x, logo_y, logo_x + logo_w, logo_y + logo_h)
        
        page.insert_image(img_rect, pixmap=logo_pix, overlay=False)
        
        font_size = 12
        text_width = fitz.get_text_length(footer_text, fontname="helv", fontsize=font_size)
        text_x = (rect.width - text_width) / 2
        text_y = rect.height - 15
        
        page.insert_text((text_x, text_y), footer_text, fontsize=font_size, color=(0.3, 0.3, 0.3), fill_opacity=0.5)
        
        link_rect = fitz.Rect(text_x, text_y - font_size, text_x + text_width, text_y + 2)
        page.insert_link({"kind": fitz.LINK_URI, "uri": footer_link, "from": link_rect})
        
    cover_doc.close()
    return new_doc

def split_pdf(input_pdf, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(input_pdf)
    current_pages = []
    current_code = None

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        code = extract_course_code(text)

        if code:
            if current_code and current_pages:
                new_doc = fitz.open()
                for p in current_pages:
                    new_doc.insert_pdf(doc, from_page=p, to_page=p)
                
                watermarked_doc = apply_watermark(new_doc)
                output_path = os.path.join(output_dir, f"{current_code}.pdf")
                watermarked_doc.save(output_path)
                watermarked_doc.close()
                new_doc.close()
                current_pages = []

            current_code = code
        current_pages.append(page_num)

    if current_code and current_pages:
        new_doc = fitz.open()
        for p in current_pages:
            new_doc.insert_pdf(doc, from_page=p, to_page=p)
        
        watermarked_doc = apply_watermark(new_doc)
        output_path = os.path.join(output_dir, f"{current_code}.pdf")
        watermarked_doc.save(output_path)
        watermarked_doc.close()
        new_doc.close()

    print("Splitting and watermarking complete!")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_pdf")
    parser.add_argument("-o", "--output", default="courses")
    args = parser.parse_args()
    split_pdf(args.input_pdf, args.output)

if __name__ == "__main__":
    main()
