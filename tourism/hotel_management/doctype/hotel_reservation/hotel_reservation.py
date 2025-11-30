# Copyright (c) 2024, Omar Ahmed Sabry and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, getdate, date_diff


class HotelReservation(Document):
	def validate(self):
		self.calculate_nights()
		self.calculate_totals()
		self.validate_dates()
	
	def calculate_nights(self):
		if self.check_in_date and self.check_out_date:
			self.nights = date_diff(self.check_out_date, self.check_in_date)
			if self.nights < 1:
				self.nights = 1
	
	def calculate_totals(self):
		self.total_room_rate = flt(self.nights or 1) * flt(self.rate_per_night) * flt(self.number_of_rooms or 1)
		self.balance_amount = flt(self.total_room_rate) - flt(self.advance_amount)
	
	def validate_dates(self):
		if self.check_in_date and self.check_out_date:
			if getdate(self.check_out_date) <= getdate(self.check_in_date):
				frappe.throw(_("Check Out Date must be after Check In Date"))
	
	def on_submit(self):
		self.status = "Confirmed"
	
	def on_cancel(self):
		self.status = "Cancelled"


@frappe.whitelist()
def create_hotel_folio(reservation_name):
	"""Create Hotel Folio from Reservation"""
	reservation = frappe.get_doc("Hotel Reservation", reservation_name)
	
	if reservation.hotel_folio:
		frappe.throw(_("Hotel Folio already exists for this reservation"))
	
	if reservation.status not in ["Confirmed", "Draft"]:
		frappe.throw(_("Cannot create folio for {0} reservation").format(reservation.status))
	
	folio = frappe.new_doc("Hotel Folio")
	folio.folio_type = "Reservation"
	folio.hotel = reservation.hotel
	folio.room_type = reservation.room_type
	folio.check_in_date = reservation.check_in_date
	folio.check_out_date = reservation.check_out_date
	folio.customer = reservation.customer
	folio.guest_name = reservation.contact_person
	folio.contact_phone = reservation.contact_phone
	folio.contact_email = reservation.contact_email
	folio.rate_per_night = reservation.rate_per_night
	folio.number_of_guests = len(reservation.guests) or 1
	folio.remarks = reservation.special_requests
	folio.reservation = reservation.name
	
	folio.insert(ignore_permissions=True)
	
	reservation.db_set("hotel_folio", folio.name)
	reservation.db_set("status", "Checked In")
	
	return folio.name


@frappe.whitelist()
def confirm_reservation(reservation_name):
	"""Confirm a reservation"""
	reservation = frappe.get_doc("Hotel Reservation", reservation_name)
	if reservation.docstatus == 0:
		reservation.submit()
	return reservation


@frappe.whitelist()
def cancel_reservation(reservation_name):
	"""Cancel a reservation"""
	reservation = frappe.get_doc("Hotel Reservation", reservation_name)
	if reservation.docstatus == 1:
		reservation.cancel()
	elif reservation.docstatus == 0:
		reservation.status = "Cancelled"
		reservation.save()
	return reservation


@frappe.whitelist()
def mark_no_show(reservation_name):
	"""Mark reservation as No Show"""
	reservation = frappe.get_doc("Hotel Reservation", reservation_name)
	reservation.db_set("status", "No Show")
	return reservation

