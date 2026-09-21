#!/usr/bin/env python3
def generate_hsheet(h_ki_totals, h_df, h_cheps, h_loscams, h_maxi_total):

    import datetime
    import math
    from pathlib import Path
    from typing import cast

    import pandas as pd
    from openpyxl import load_workbook
    from openpyxl.cell.cell import MergedCell
    from openpyxl.reader.excel import load_workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.page import PageMargins

    # Date & Time
    today = datetime.datetime.now(datetime.timezone.utc).astimezone().strftime("%Y_%m_%d")

    rows_per_page = 49
    bottom_offset = 3

    # Spreadsheet column widths
    #                A   B   C  D   E   F   G
    column_widths = [12, 11 ,9 ,13 ,12 ,13 ,22]

    # Column header strings
    headers = ["ID", "Variety", "Order QTY", "Pallet QTY", "Roll Type", "Pallet Type", f"WEIGHTS {today}"]

    # Save Path
    save_path = Path.home() / "Desktop" / f"WeightSheet_{today}.xlsx"

    # Calculate number of 50s for h_ki_totals, then dividing amoungst the pallet types
    fifty_pallets = math.ceil(h_ki_totals / 50)
    h_50s = fifty_pallets - (h_cheps + h_loscams)

    # Maxi logic
    full_maxis, maxi_remainder = divmod(h_maxi_total, 20)

    # H 50 Template
    h_50 = {
        'col2': "Kikuyu",       # Variety
        'col3': h_ki_totals,    # Order QTY
        'col4': 50,             # Pallet QTY
        'col5': "Small",        # Roll Type
        'col6': "H"             # Pallet Type
    }

    # H 50 Chep Template
    chep_50 = {
        'col2': "Kikuyu",       # Variety
        'col3': h_ki_totals,    # Order QTY
        'col4': 50,             # Pallet QTY
        'col5': "Small",        # Roll Type
        'col6': "Chep"          # Pallet Type
    }

    # H 50 Loscam Template
    loscam_50 = {
        'col2': "Kikuyu",       # Variety
        'col3': h_ki_totals,    # Order QTY
        'col4': 50,             # Pallet QTY
        'col5': "Small",        # Roll Type
        'col6': "Loscam"        # Pallet Type
    }

    # H Maxi template
    maxi = {
        'col2': "Kikuyu",       # Variety
        'col3': h_maxi_total,   # Order QTY
        'col4': 20,             # Pallet QTY
        'col5': "MAXI",         # Roll Type
        'col6': "MAXI"          # Pallet Type
    }

    # Multiply apropriate amount of rows for each pallet type
    insert_h_50s = pd.DataFrame([h_50] * h_50s)
    insert_cheps = pd.DataFrame([chep_50] * h_cheps)
    insert_loscams = pd.DataFrame([loscam_50] * h_loscams)
    insert_full_maxis = pd.DataFrame([maxi] * full_maxis)

    # Finish maxi logic and append all blocks of rows
    if maxi_remainder > 0:
        part_maxi = maxi.copy()
        part_maxi['col4'] = maxi_remainder
        insert_part_maxi = pd.DataFrame([part_maxi])
        h_df = pd.concat([h_df, insert_full_maxis, insert_part_maxi, insert_h_50s, insert_cheps, insert_loscams], ignore_index=True)
    else:
        h_df = pd.concat([h_df, insert_full_maxis, insert_h_50s, insert_cheps, insert_loscams], ignore_index=True)

    h_df.to_excel(save_path, index=False)

    wb = load_workbook(save_path)
    ws = wb.active

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

    # Save workbook
    wb.save(save_path)
