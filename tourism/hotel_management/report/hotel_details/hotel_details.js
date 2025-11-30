// Copyright (c) 2024, Omar Ahmed Sabry and contributors
// For license information, please see license.txt

frappe.query_reports["Hotel Details"] = {
	"filters": [
		{
			"fieldname": "region",
			"label": __("Region"),
			"fieldtype": "Link",
			"options": "Region"
		},
		{
			"fieldname": "star_rating",
			"label": __("Star Rating"),
			"fieldtype": "Select",
			"options": "\n1 Star\n2 Star\n3 Star\n4 Star\n5 Star"
		},
		{
			"fieldname": "status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": "\nActive\nInactive\nUnder Renovation"
		},
		{
			"fieldname": "city",
			"label": __("City"),
			"fieldtype": "Data"
		}
	]
};

