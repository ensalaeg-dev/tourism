# Copyright (c) 2024, Omar Ahmed Sabry and contributors
# For license information, please see license.txt

from frappe import _


def get_data():
	return {
		"fieldname": "region",
		"non_standard_fieldnames": {},
		"transactions": [
			{
				"label": _("Masters"),
				"items": ["Hotel", "Restaurant", "Transportation", "Attraction", "Guide"]
			},
			{
				"label": _("Packages"),
				"items": ["Tour Package", "Tour Registration"]
			},
			{
				"label": _("Contracts"),
				"items": ["Tourism Contract"]
			}
		]
	}

