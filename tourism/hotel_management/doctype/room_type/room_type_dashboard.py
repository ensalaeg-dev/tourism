# Copyright (c) 2024, Omar Ahmed Sabry and contributors
# For license information, please see license.txt

from frappe import _


def get_data():
	return {
		"fieldname": "room_type",
		"transactions": [
			{
				"label": _("Rooms"),
				"items": ["Hotel Room Master"]
			},
			{
				"label": _("Operations"),
				"items": ["Hotel Folio", "Hotel Reservation"]
			}
		]
	}
