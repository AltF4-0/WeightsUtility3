#!/usr/bin/env python3
def generate_hsheet(h_ki_totals, h_cheps, h_loscams, h_maxi_total):

    import datetime
    import math
    from pathlib import Path

    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.page import PageMargins

    #temporary
    number_of_pages = 1

    # Date & Time
    today = datetime.datetime.now(datetime.timezone.utc).astimezone().strftime("%Y_%m_%d")

    # Save Path
    save_path = Path.home() / "Desktop" / f"WeightSheet_{today}.xlsx"

    rows_per_page = 49
    bottom_offset = 3

    # Spreadsheet column widths
    #                A   B   C   D   E   F   G
    column_widths = [12, 11 ,9 ,13 ,12 ,13 ,22]

    # Column header strings
    headers = ["ID", "Variety", "Order QTY", "Pallet QTY", "Roll Type", "Pallet Type", f"WEIGHTS {today}"]

    # Calculate number of 50s for h_ki_totals, then dividing amoungst the pallet types
    fifty_pallets = math.ceil(h_ki_totals / 50)
    h_50s = fifty_pallets - (h_cheps + h_loscams)

    # Maxi logic
    full_maxis, maxi_remainder = divmod(h_maxi_total, 20)

    # Load data frame with OpenPyXl
    wb = Workbook()
    ws = wb.active

    # H 50 Template
    h_50 = {
        'id': " ",
        'variety': "Kikuyu",         # Variety
        'order_qty': h_ki_totals,    # Order QTY
        'pallet_qty': 50,            # Pallet QTY
        'roll_type': "Small",        # Roll Type
        'pallet_type': "H"           # Pallet Type
    }

    # H 50 Chep Template
    chep_50 = {
        'id': " ",
        'variety': "Kikuyu",         # Variety
        'order_qty': h_ki_totals,    # Order QTY
        'pallet_qty': 50,            # Pallet QTY
        'roll_type': "Small",        # Roll Type
        'pallet_type': "Chep"        # Pallet Type
    }

    # H 50 Loscam Template
    loscam_50 = {
        'id': " ",
        'variety': "Kikuyu",         # Variety
        'order_qty': h_ki_totals,    # Order QTY
        'pallet_qty': 50,            # Pallet QTY
        'roll_type': "Small",        # Roll Type
        'pallet_type': "Loscam"      # Pallet Type
    }

    # H Maxi template
    maxi = {
        'id': " ",
        'variety': "Kikuyu",         # Variety
        'order_qty': h_maxi_total,   # Order QTY
        'pallet_qty': 20,            # Pallet QTY
        'roll_type': "MAXI",         # Roll Type
        'pallet_type': "MAXI"        # Pallet Type
    }

    # Build rows according to the logic
    rows = []
    rows += [maxi] * full_maxis

    # Finish maxi logic and append all blocks of rows
    if maxi_remainder > 0:
        part_maxi = maxi.copy()
        part_maxi['pallet_qty'] = maxi_remainder
        rows.append(part_maxi)

    rows += [h_50] * h_50s
    rows += [chep_50] * h_cheps
    rows += [loscam_50] * h_loscams

    for row in rows:
        ws.append(list(row.values()))

    # Append column widths and header strings
    for i, width in enumerate(column_widths, start=1):
        col_letter = get_column_letter(i)
        ws.column_dimensions[col_letter].width = width

    for i, header in enumerate(headers, start=1):
        ws.cell(row=1, column=i, value=header)

    # Set page margins
    ws.page_margins = PageMargins(
        left=0.5,
        right=0.5,
        top=0.8,
        bottom=0.5,
        header=0.5,
        footer=0.5,
    )

    # Apply formatting for cell borders, text alignment and cell colour fill
    for row in ws.iter_rows(
        min_row=1,
        max_row=((number_of_pages * rows_per_page) - 1),
        min_col=1,
        max_col=ws.max_column
    ):
        for cell in row:
            cell.border = Border(
                left=Side(style="thin"),
                right=Side(style="thin"),
                top=Side(style="thin"),
                bottom=Side(style="thin")
            )
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.fill = PatternFill(
                start_color="F2F2F2", end_color="F2F2F2", fill_type="solid"
            )
            if cell.value == "Sir Walter":
                cell.fill = PatternFill(
                    start_color="B5B5B5", end_color="B5B5B5", fill_type="solid"
                )
            # Column G ("WEIGHTS") is filled with an invisable character so LibreOffice prints the cell borders
            if cell.column == 7 and cell.value in (None, ""):
                cell.value = " "

    # Header row formatting
    for cell in ws[1]:
        cell.fill = PatternFill(
            start_color="222222", end_color="222222", fill_type="solid"
        )
        cell.font = Font(bold=True, color="FFFFFF")
    ws["G1"].value = f"WEIGHTS {today}"

    # Save workbook
    wb.save(save_path)
