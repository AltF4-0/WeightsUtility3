#!/usr/bin/env python3
def generate_hsheet(wb, h_ki_totals, h_ki_parts_total, h_ki_parts_h_pallets, h_ki_parts_chep_pallets, h_ki_parts_loscam_pallets, h_cheps, h_loscams, h_maxi_total, today):

    import math
    from pathlib import Path

    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.page import PageMargins

    # Save Path
    save_path = Path.home() / "Desktop" / f"WeightSheet_{today}.xlsx"

    rows_per_page = 49
    bottom_offset = 3

    # Spreadsheet column widths and row height
    #                A   B   C   D   E   F   G
    column_widths = [12, 11 ,11 ,12 ,12 ,12 ,23]
    row_height = 15

    # Calculate number of 50s for h_ki_totals, then dividing amoungst the pallet types
    fifty_pallets = math.ceil((h_ki_totals - h_ki_parts_total) / 50)
    h_50s = (fifty_pallets - (h_cheps + h_loscams))

    # Maxi logic
    total_tubes = math.ceil(h_maxi_total / 20)
    full_maxis, maxi_remainder = divmod(h_maxi_total, 20)

    # Load workbook with OpenPyXl
    ws = wb.active

    # Page setup
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.orientation = "portrait"
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth = 0
    ws.page_setup.fitToHeight = 0

    # == Template dicts ==

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

    # Pallet totals block template
    h_sw_pallets = 1
    h_sw_cheps = 1
    h_sw_loscams = 1
    # temp vars ^
    totals_block = [
        {'id': "TOTALS", 'variety': "H", 'order_qty': "CHEP", 'pallet_qty': "LOSCAM", 'roll_type': "TUBES"},
        {'id': "Kikuyu", 'variety': (h_50s + h_ki_parts_h_pallets), 'order_qty': (h_cheps + h_ki_parts_chep_pallets), 'pallet_qty': (h_loscams + h_ki_parts_loscam_pallets), 'roll_type': total_tubes},
        {'id': "Sir Walter", 'variety': h_sw_pallets, 'order_qty': h_sw_cheps, 'pallet_qty': h_sw_loscams}
        ]
    # ====================

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

    # Append column widths
    for i, width in enumerate(column_widths, start=1):
        col_letter = get_column_letter(i)
        ws.column_dimensions[col_letter].width = width

    # ====== Insert totals block ======
    # Calculate total number of pages needed
    number_of_pages = math.ceil((ws.max_row + bottom_offset) / rows_per_page)

    # Calculate the first row that the total block is inserted in
    start_row = (((number_of_pages * rows_per_page) - bottom_offset) + 1)

    # Inserts blank rows, pushing any data there downwards so it is not overwritten
    ws.insert_rows(start_row, amount=3)

    # Insert totals block
    for offset, row in enumerate(totals_block):
        for col, value in enumerate(row.values(), start=1):
            ws.cell(row=start_row + offset, column=col, value=value)

    # Set row height
    for r in range(1, ws.max_row + 1):
        ws.row_dimensions[r].height = row_height

    # Apply formatting for cell borders, text alignment and cell colour fill
    for row in ws.iter_rows(
        min_row=1,
        max_row=ws.max_row,
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

    # Set page margins
    ws.page_margins = PageMargins(
        left=0.5,
        right=0.5,
        top=0.8,
        bottom=0.5,
        header=0.5,
        footer=0.5,
    )

    # Save workbook
    wb.save(save_path)
