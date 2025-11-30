# Copyright (c) 2024, Omar Ahmed Sabry and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{
			"fieldname": "name",
			"label": _("Folio"),
			"fieldtype": "Link",
			"options": "Hotel Folio",
			"width": 120
		},
		{
			"fieldname": "hotel",
			"label": _("Hotel"),
			"fieldtype": "Link",
			"options": "Hotel",
			"width": 150
		},
		{
			"fieldname": "guest_name",
			"label": _("Guest Name"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "room_type",
			"label": _("Room Type"),
			"fieldtype": "Link",
			"options": "Room Type",
			"width": 100
		},
		{
			"fieldname": "check_in_date",
			"label": _("Check In"),
			"fieldtype": "Datetime",
			"width": 140
		},
		{
			"fieldname": "check_out_date",
			"label": _("Check Out"),
			"fieldtype": "Datetime",
			"width": 140
		},
		{
			"fieldname": "nights",
			"label": _("Nights"),
			"fieldtype": "Int",
			"width": 60
		},
		{
			"fieldname": "total_amount",
			"label": _("Total Amount"),
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"fieldname": "paid_amount",
			"label": _("Paid"),
			"fieldtype": "Currency",
			"width": 100
		},
		{
			"fieldname": "balance_amount",
			"label": _("Balance"),
			"fieldtype": "Currency",
			"width": 100
		},
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Data",
			"width": 100
		}
	]


def get_data(filters):
	conditions = get_conditions(filters)
	
	data = frappe.db.sql("""
		SELECT
			name,
			hotel,
			guest_name,
			room_type,
			check_in_date,
			check_out_date,
			nights,
			total_amount,
			paid_amount,
			balance_amount,
			status
		FROM `tabHotel Folio`
		WHERE 1=1
		{conditions}
		ORDER BY creation DESC
	""".format(conditions=conditions), filters, as_dict=1)
	
	return data


def get_conditions(filters):
	conditions = ""
	
	if filters.get("hotel"):
		conditions += " AND hotel = %(hotel)s"
	
	if filters.get("status"):
		conditions += " AND status = %(status)s"
	
	if filters.get("from_date"):
		conditions += " AND check_in_date >= %(from_date)s"
	
	if filters.get("to_date"):
		conditions += " AND check_in_date <= %(to_date)s"
	
	if filters.get("customer"):
		conditions += " AND customer = %(customer)s"
	
	return conditions

