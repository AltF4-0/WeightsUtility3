import datetime

from openpyxl import Workbook

from hsheet import generate_hsheet

today = datetime.datetime.now(datetime.timezone.utc).astimezone().strftime("%Y_%m_%d")

h_ki_totals = 1420
h_ki_parts_h_pallets = 0
h_ki_parts_chep_pallets = 2
h_ki_parts_loscam_pallets = 0
h_ki_parts_total = 20
h_cheps = 2
h_loscams = 3
h_maxi_total = 315

wb = Workbook()
ws = wb.active

# Column header strings
headers = ["ID", "Variety", "Order QTY", "Pallet QTY", "Roll Type", "Pallet Type", f"WEIGHTS {today}"]
ws.append(headers)

generate_hsheet(wb, h_ki_totals, h_ki_parts_total, h_ki_parts_h_pallets, h_ki_parts_chep_pallets, h_ki_parts_loscam_pallets, h_cheps, h_loscams, h_maxi_total, today)
