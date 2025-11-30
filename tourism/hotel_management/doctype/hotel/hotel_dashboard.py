# Copyright (c) 2024, Omar Ahmed Sabry and contributors
# For license information, please see license.txt

from frappe import _


def get_data():
	return {
		"heatmap": True,
		"heatmap_message": _("This is based on the Hotel Folios created against this Hotel"),
		"fieldname": "hotel",
		"transactions": [
			{
				"label": _("Operations"),
				"items": ["Hotel Folio", "Hotel Reservation"]
			},
			{
				"label": _("Rooms"),
				"items": ["Hotel Room Master"]
			},
			{
				"label": _("Contracts"),
				"items": ["Tourism Contract"]
			}
		]
	}
