# Copyright (c) 2024, Omar Ahmed Sabry and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class HotelRoomMaster(Document):
	def validate(self):
		self.set_price_from_room_type()
	
	def set_price_from_room_type(self):
		if self.room_type and not self.price_per_night:
			room_type = frappe.get_doc("Room Type", self.room_type)
			self.price_per_night = room_type.base_price
			self.max_occupancy = room_type.max_occupancy
			self.extra_bed_available = room_type.extra_bed_available
			self.extra_bed_price = room_type.extra_bed_price


@frappe.whitelist()
def update_room_status(room_name, status, folio=None, guest=None, check_in=None, checkout=None):
	"""Update room status and occupancy info"""
	room = frappe.get_doc("Hotel Room Master", room_name)
	room.status = status
	room.current_folio = folio
	room.current_guest = guest
	room.check_in_date = check_in
	room.expected_checkout = checkout
	room.save(ignore_permissions=True)
	return room


@frappe.whitelist()
def get_available_rooms(hotel, room_type=None, check_in_date=None, check_out_date=None):
	"""Get available rooms for a hotel"""
	filters = {
		"hotel": hotel,
		"status": "Available"
	}
	if room_type:
		filters["room_type"] = room_type
	
	rooms = frappe.get_all("Hotel Room Master", filters=filters, fields=["name", "room_number", "room_type", "floor", "price_per_night"])
	return rooms


@frappe.whitelist()
def mark_for_cleaning(room_name):
	"""Mark room for cleaning after checkout"""
	room = frappe.get_doc("Hotel Room Master", room_name)
	room.status = "Cleaning"
	room.current_folio = None
	room.current_guest = None
	room.check_in_date = None
	room.expected_checkout = None
	room.save(ignore_permissions=True)
	return room


@frappe.whitelist()
def mark_available(room_name):
	"""Mark room as available after cleaning"""
	room = frappe.get_doc("Hotel Room Master", room_name)
	room.status = "Available"
	room.save(ignore_permissions=True)
	return room

