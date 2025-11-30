# Copyright (c) 2024, Omar Ahmed Sabry and contributors
# For license information, please see license.txt

from frappe import _


def get_data():
	return {
		"fieldname": "package_category",
		"non_standard_fieldnames": {},
		"transactions": [
			{
				"label": _("Packages"),
				"items": ["Tour Package"]
			},
			{
				"label": _("Bookings"),
				"items": ["Tour Registration"]
			}
		]
	}

