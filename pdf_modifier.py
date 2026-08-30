def modify_pdf(path=None):

    import datetime
    import math
    from pathlib import Path

    import pdfplumber
    import pymupdf

    # Parameters
    QUANTITY_LABEL = "Quantity"
    PALLET_LABEL = "# of Pallets"
    JOB_LABEL = "JOB #"
    NEW_JOB_TEXT = "Weight (KG)"
    VARIETY_LABEL = "VARIETY"
    TRIGGER_TEXT = ["KI", "KP"]

    VALUE_BOX_OFFSET_Y = 4
    VALUE_BOX_HEIGHT = 50
    VALUE_BOX_WIDTH = 200

    PALLET_OFFSET_Y = 43
    PALLET_OFFSET_X = 25
    PALLET_FONT_SIZE = 56

    WEIGHT_FONT_SIZE = 16
    WEIGHT_OFFSET_X = 3
    WEIGHT_OFFSET_Y = 16

    # Paths
    today = datetime.datetime.now(datetime.timezone.utc).astimezone().strftime("%Y_%m_%d")
    output_path = Path.home() / "Desktop" / f"Stickers_{today}.pdf"

    #Checks for alternate input path from GUI script, if none is found then it defaults to the downloads folder
    if path:
            latest_pdf = Path(path)
            if not latest_pdf.is_file():
                raise FileNotFoundError(f"Provided file does not exist: {latest_pdf}")
    else:
        downloads = Path.home() / "Downloads"
        pdf_files = list(downloads.glob("*.pdf*"))
        if not pdf_files:
            raise FileNotFoundError("No .pdf files found in location!")
        latest_pdf = max(pdf_files, key=lambda f: f.stat().st_mtime)

    def find_label_instances(words, label):
        parts = label.split()
        matches = []
        for i in range(len(words) - len(parts) + 1):
            window = words[i:i + len(parts)]
            combined = " ".join(w["text"] for w in window)
            if combined.lower() == label.lower():
                matches.append(window)
        return matches

    def extract_value_below(page, label_words):
        x0 = min(w["x0"] for w in label_words)
        bottom = max(w["bottom"] for w in label_words)
        search_box = (
            x0,
            bottom + VALUE_BOX_OFFSET_Y,
            x0 + VALUE_BOX_WIDTH,
            bottom + VALUE_BOX_OFFSET_Y + VALUE_BOX_HEIGHT
        )
        cropped = page.crop(search_box)
        text = cropped.extract_text()
        return text.strip() if text else ""

    def parse_int(text):
        digits = "".join(c for c in text if c.isdigit())
        return int(digits) if digits else None

    # Filter pages and calculate pallet counts
    page_pallet_counts = []
    kept_pages_indices = []

    with pdfplumber.open(latest_pdf) as pdf:
        for page_index, page in enumerate(pdf.pages):
            words = page.extract_words(use_text_flow=True)

            # VARIETY label filter for non turf stickers
            variety_instances = find_label_instances(words, VARIETY_LABEL)
            delete_page = False

            for variety_window in variety_instances:
                label_bottom = max(w["bottom"] for w in variety_window)
                # Collect all words below the label
                words_below = [w["text"].strip() for w in words if w["top"] > label_bottom]

                # If none of the permitted TRIGGER_TEXT exist, mark for deletion
                if not any(v.lower() in [t.lower() for t in TRIGGER_TEXT] for v in words_below):
                    delete_page = True
                    break

            if delete_page:
                continue

            # Find QTY and append number of pallets
            qty_labels = find_label_instances(words, QUANTITY_LABEL)
            if not qty_labels:
                page_pallet_counts.append(1)
                kept_pages_indices.append(page_index)
                continue

            raw_value = extract_value_below(page, qty_labels[0])
            qty = parse_int(raw_value)
            pallets = math.ceil(qty / 50) if qty else 1
            page_pallet_counts.append(pallets)
            kept_pages_indices.append(page_index)

    # Duplicate pages with pallet counts and apply labels
    src_doc = pymupdf.open(latest_pdf)
    out_doc = pymupdf.open()

    for idx, pallet_count in zip(kept_pages_indices, page_pallet_counts):
        src_page = src_doc[idx]
        for _ in range(pallet_count):
            new_page = out_doc.new_page(
                width=src_page.rect.width, height=src_page.rect.height)
            new_page.show_pdf_page(new_page.rect, src_doc, idx)

            # Write pallet count
            pallet_instances = new_page.search_for(PALLET_LABEL)
            if pallet_instances:
                label_rect = pallet_instances[0]
                insert_point = pymupdf.Point(
                    label_rect.x0 + PALLET_OFFSET_X, label_rect.y1 + PALLET_OFFSET_Y)
                new_page.insert_text(
                    insert_point, str(pallet_count), fontname="helv",
                    fontsize=PALLET_FONT_SIZE, color=(0, 0, 0))

            # Replace "JOB #" with "Weight (KG)"
            job_instances = new_page.search_for(JOB_LABEL)
            if job_instances:
                for inst in job_instances:
                    new_page.add_redact_annot(inst, fill=(1, 1, 1))
                new_page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE)  # type: ignore[reportAttributeAccessIssue]

                for inst in job_instances:
                    insert_point = pymupdf.Point(
                        inst.x0 + WEIGHT_OFFSET_X, inst.y0 + WEIGHT_OFFSET_Y)
                    new_page.insert_text(
                        insert_point, NEW_JOB_TEXT, fontname="helv",
                        fontsize=WEIGHT_FONT_SIZE, color=(0, 0, 0))

    # Save output PDF
    out_doc.save(output_path)
    out_doc.close()
    src_doc.close()
