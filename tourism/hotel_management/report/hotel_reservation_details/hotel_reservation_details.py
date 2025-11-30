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
			"label": _("Reservation"),
			"fieldtype": "Link",
			"options": "Hotel Reservation",
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
			"fieldname": "room_type",
			"label": _("Room Type"),
			"fieldtype": "Link",
			"options": "Room Type",
			"width": 100
		},
		{
			"fieldname": "contact_person",
			"label": _("Guest"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "check_in_date",
			"label": _("Check In"),
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "check_out_date",
			"label": _("Check Out"),
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "nights",
			"label": _("Nights"),
			"fieldtype": "Int",
			"width": 60
		},
		{
			"fieldname": "number_of_rooms",
			"label": _("Rooms"),
			"fieldtype": "Int",
			"width": 60
		},
		{
			"fieldname": "total_room_rate",
			"label": _("Total Rate"),
			"fieldtype": "Currency",
			"width": 110
		},
		{
			"fieldname": "advance_amount",
			"label": _("Advance"),
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
			room_type,
			contact_person,
			check_in_date,
			check_out_date,
			nights,
			number_of_rooms,
			total_room_rate,
			advance_amount,
			balance_amount,
			status
		FROM `tabHotel Reservation`
		WHERE docstatus < 2
		{conditions}
		ORDER BY check_in_date DESC
	""".format(conditions=conditions), filters, as_dict=1)
	
	return data


def get_conditions(filters):
	conditions = ""
	
	if filters.get("hotel"):
		conditions += " AND hotel = %(hotel)s"
	
	if filters.get("room_type"):
		conditions += " AND room_type = %(room_type)s"
	
	if filters.get("status"):
		conditions += " AND status = %(status)s"
	
	if filters.get("from_date"):
		conditions += " AND check_in_date >= %(from_date)s"
	
	if filters.get("to_date"):
		conditions += " AND check_in_date <= %(to_date)s"
	
	if filters.get("customer"):
		conditions += " AND customer = %(customer)s"
	
	return conditions

