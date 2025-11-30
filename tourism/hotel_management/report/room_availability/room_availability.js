// Copyright (c) 2024, Omar Ahmed Sabry and contributors
// For license information, please see license.txt

frappe.query_reports["Room Availability"] = {
	"filters": [
		{
			"fieldname": "hotel",
			"label": __("Hotel"),
			"fieldtype": "Link",
			"options": "Hotel"
		},
		{
			"fieldname": "room_type",
			"label": __("Room Type"),
			"fieldtype": "Link",
			"options": "Room Type"
		},
		{
			"fieldname": "status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": "\nAvailable\nOccupied\nReserved\nMaintenance\nCleaning\nOut of Order"
		},
		{
			"fieldname": "floor",
			"label": __("Floor"),
			"fieldtype": "Data"
		}
	]
};

