# Copyright (c) 2024, Omar Ahmed Sabry and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, getdate


class TourRegistration(Document):
	def validate(self):
		self.validate_dates()
		self.calculate_total_pax()
		self.calculate_totals()
		self.calculate_grand_total()
	
	def validate_dates(self):
		if self.arrival_date and self.departure_date:
			if getdate(self.arrival_date) > getdate(self.departure_date):
				frappe.throw(_("Departure date cannot be before arrival date"))
	
	def calculate_total_pax(self):
		self.total_pax = flt(self.number_of_adults) + flt(self.number_of_children)
	
	def calculate_totals(self):
		"""Calculate total costs for each component"""
		# Calculate hotel costs
		self.total_hotel_cost = 0
		for hotel in self.hotels:
			hotel.total_amount = flt(hotel.nights) * flt(hotel.rate_per_night)
			self.total_hotel_cost += flt(hotel.total_amount)
		
		# Calculate restaurant costs
		self.total_restaurant_cost = 0
		for restaurant in self.restaurants:
			restaurant.total_amount = flt(restaurant.pax) * flt(restaurant.rate_per_person)
			self.total_restaurant_cost += flt(restaurant.total_amount)
		
		# Calculate transportation costs
		self.total_transportation_cost = 0
		for transport in self.transportations:
			transport.total_amount = flt(transport.rate)
			self.total_transportation_cost += flt(transport.total_amount)
		
		# Calculate guide costs
		self.total_guide_cost = 0
		for guide in self.guides:
			guide.total_amount = flt(guide.hours) * flt(guide.rate)
			self.total_guide_cost += flt(guide.total_amount)
		
		# Calculate attraction costs
		self.total_attraction_cost = 0
		for attraction in self.attractions:
			attraction.total_amount = flt(attraction.pax) * flt(attraction.entry_fee)
			self.total_attraction_cost += flt(attraction.total_amount)
		
		# Calculate total cost
		self.total_cost = (
			flt(self.total_hotel_cost) +
			flt(self.total_restaurant_cost) +
			flt(self.total_transportation_cost) +
			flt(self.total_guide_cost) +
			flt(self.total_attraction_cost)
		)
	
	def calculate_grand_total(self):
		self.grand_total = flt(self.total_cost) - flt(self.discount_amount)
	
	def on_submit(self):
		self.status = "Confirmed"
	
	def on_cancel(self):
		self.status = "Cancelled"


@frappe.whitelist()
def get_package_details(tour_package):
	"""Get all details from tour package for tour registration"""
	package = frappe.get_doc("Tour Package", tour_package)
	
	details = {
		"package_name": package.package_name,
		"region": package.region,
		"package_category": package.package_category,
		"hotels": [],
		"restaurants": [],
		"transportations": [],
		"guides": [],
		"attractions": []
	}
	
	# Copy hotels
	for hotel in package.hotels:
		details["hotels"].append({
			"hotel": hotel.hotel,
			"room_type": hotel.room_type,
			"nights": hotel.nights,
			"rate_per_night": hotel.rate_per_night,
			"total_amount": hotel.total_amount
		})
	
	# Copy restaurants
	for restaurant in package.restaurants:
		details["restaurants"].append({
			"restaurant": restaurant.restaurant,
			"meal_type": restaurant.meal_type,
			"rate_per_person": restaurant.rate_per_person
		})
	
	# Copy transportations
	for transport in package.transportations:
		details["transportations"].append({
			"transportation": transport.transportation,
			"vehicle": transport.vehicle,
			"rate": transport.rate_per_day
		})
	
	# Copy guides
	for guide in package.guides:
		details["guides"].append({
			"guide": guide.guide,
			"service_type": guide.service_type,
			"rate": guide.rate
		})
	
	# Copy attractions
	for attraction in package.attractions:
		details["attractions"].append({
			"attraction": attraction.attraction,
			"entry_fee": attraction.entry_fee
		})
	
	return details


def create_crm_opportunity(doc, method=None):
	"""Create CRM Opportunity from Tour Registration"""
	if doc.crm_opportunity:
		return
	
	# Check if Opportunity doctype exists
	if not frappe.db.exists("DocType", "Opportunity"):
		return
	
	try:
		opportunity = frappe.new_doc("Opportunity")
		opportunity.opportunity_from = "Customer"
		opportunity.party_name = doc.customer
		opportunity.opportunity_type = "Sales"
		opportunity.status = "Open"
		opportunity.source = "Tour Registration"
		opportunity.opportunity_amount = doc.grand_total
		opportunity.insert(ignore_permissions=True)
		
		doc.db_set("crm_opportunity", opportunity.name)
		frappe.msgprint(_("CRM Opportunity {0} created").format(opportunity.name))
	except Exception as e:
		frappe.log_error(f"Error creating CRM Opportunity: {str(e)}")


@frappe.whitelist()
def create_lead_from_registration(registration_name):
	"""Create CRM Lead from Tour Registration"""
	reg = frappe.get_doc("Tour Registration", registration_name)
	
	if reg.crm_lead:
		frappe.throw(_("Lead already exists for this registration"))
	
	# Check if Lead doctype exists
	if not frappe.db.exists("DocType", "Lead"):
		frappe.throw(_("Lead DocType not found"))
	
	lead = frappe.new_doc("Lead")
	lead.lead_name = reg.contact_person or reg.customer_name
	lead.email_id = reg.contact_email
	lead.mobile_no = reg.contact_phone
	lead.source = "Tour Registration"
	lead.status = "Lead"
	lead.insert(ignore_permissions=True)
	
	reg.db_set("crm_lead", lead.name)
	
	return lead.name

