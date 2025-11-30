# Copyright (c) 2024, Omar Ahmed Sabry and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, add_days, getdate


class TourPackage(Document):
	def validate(self):
		self.calculate_totals()
		self.calculate_selling_price()
	
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
			restaurant.total_amount = flt(restaurant.meals_count) * flt(restaurant.rate_per_person)
			self.total_restaurant_cost += flt(restaurant.total_amount)
		
		# Calculate transportation costs
		self.total_transportation_cost = 0
		for transport in self.transportations:
			transport.total_amount = flt(transport.days) * flt(transport.rate_per_day)
			self.total_transportation_cost += flt(transport.total_amount)
		
		# Calculate guide costs
		self.total_guide_cost = 0
		for guide in self.guides:
			guide.total_amount = flt(guide.days) * flt(guide.rate)
			self.total_guide_cost += flt(guide.total_amount)
		
		# Calculate attraction costs
		self.total_attraction_cost = 0
		for attraction in self.attractions:
			attraction.total_amount = flt(attraction.qty) * flt(attraction.entry_fee)
			self.total_attraction_cost += flt(attraction.total_amount)
		
		# Calculate total cost
		self.total_cost = (
			flt(self.total_hotel_cost) +
			flt(self.total_restaurant_cost) +
			flt(self.total_transportation_cost) +
			flt(self.total_guide_cost) +
			flt(self.total_attraction_cost) +
			flt(self.base_price)
		)
	
	def calculate_selling_price(self):
		"""Calculate selling price based on total cost and profit margin"""
		if self.total_cost and self.profit_margin:
			self.selling_price = flt(self.total_cost) * (1 + flt(self.profit_margin) / 100)
		else:
			self.selling_price = self.total_cost


@frappe.whitelist()
def generate_itinerary(package_name, arrival_date, departure_date):
	"""Generate itinerary based on arrival and departure dates"""
	package = frappe.get_doc("Tour Package", package_name)
	
	arrival = getdate(arrival_date)
	departure = getdate(departure_date)
	
	if arrival > departure:
		frappe.throw(_("Departure date cannot be before arrival date"))
	
	# Clear existing itinerary
	package.itinerary = []
	
	# Generate itinerary for each day
	current_date = arrival
	day_number = 1
	
	while current_date <= departure:
		itinerary_row = {
			"day_number": day_number,
			"date": current_date,
			"title": f"Day {day_number}"
		}
		
		# Assign hotel for the day (except last day)
		if current_date < departure and package.hotels:
			# Simple assignment - first hotel
			itinerary_row["hotel"] = package.hotels[0].hotel
		
		# Assign transportation if available
		if package.transportations:
			itinerary_row["transportation"] = package.transportations[0].transportation
		
		package.append("itinerary", itinerary_row)
		
		current_date = add_days(current_date, 1)
		day_number += 1
	
	package.save()
	return package.itinerary


@frappe.whitelist()
def update_prices_from_contracts(package_name):
	"""Update package prices from active contracts"""
	package = frappe.get_doc("Tour Package", package_name)
	
	# Update hotel prices
	for hotel in package.hotels:
		contract_rate = get_contract_rate("Hotel", hotel.hotel, hotel.room_type)
		if contract_rate:
			hotel.rate_per_night = contract_rate
	
	# Update restaurant prices
	for restaurant in package.restaurants:
		contract_rate = get_contract_rate("Restaurant", restaurant.restaurant, restaurant.meal_type)
		if contract_rate:
			restaurant.rate_per_person = contract_rate
	
	# Update transportation prices
	for transport in package.transportations:
		contract_rate = get_contract_rate("Transportation", transport.transportation, transport.vehicle)
		if contract_rate:
			transport.rate_per_day = contract_rate
	
	package.save()
	frappe.msgprint(_("Prices updated from contracts"))
	return package


def get_contract_rate(contract_type, entity, sub_entity=None):
	"""Get rate from active contract"""
	from frappe.utils import nowdate
	
	filters = {
		"status": "Active",
		"docstatus": 1,
		"start_date": ("<=", nowdate()),
		"end_date": (">=", nowdate())
	}
	
	if contract_type == "Hotel":
		filters["contract_type"] = ["in", ["Hotel", "Combined"]]
		contracts = frappe.get_all("Tourism Contract", filters=filters, pluck="name")
		
		for contract_name in contracts:
			contract = frappe.get_doc("Tourism Contract", contract_name)
			for item in contract.hotel_items:
				if item.hotel == entity:
					if not sub_entity or item.room_type == sub_entity:
						return item.rate_per_night
	
	elif contract_type == "Restaurant":
		filters["contract_type"] = ["in", ["Restaurant", "Combined"]]
		contracts = frappe.get_all("Tourism Contract", filters=filters, pluck="name")
		
		for contract_name in contracts:
			contract = frappe.get_doc("Tourism Contract", contract_name)
			for item in contract.restaurant_items:
				if item.restaurant == entity:
					if not sub_entity or item.meal_type == sub_entity:
						return item.rate_per_person
	
	elif contract_type == "Transportation":
		filters["contract_type"] = ["in", ["Transportation", "Combined"]]
		contracts = frappe.get_all("Tourism Contract", filters=filters, pluck="name")
		
		for contract_name in contracts:
			contract = frappe.get_doc("Tourism Contract", contract_name)
			for item in contract.transportation_items:
				if item.transportation == entity:
					if not sub_entity or item.vehicle == sub_entity:
						return item.rate_per_day
	
	return None


@frappe.whitelist()
def reset_prices(package_name):
	"""Reset all prices to zero"""
	package = frappe.get_doc("Tour Package", package_name)
	
	for hotel in package.hotels:
		hotel.rate_per_night = 0
		hotel.total_amount = 0
	
	for restaurant in package.restaurants:
		restaurant.rate_per_person = 0
		restaurant.total_amount = 0
	
	for transport in package.transportations:
		transport.rate_per_day = 0
		transport.total_amount = 0
	
	for guide in package.guides:
		guide.rate = 0
		guide.total_amount = 0
	
	for attraction in package.attractions:
		attraction.entry_fee = 0
		attraction.total_amount = 0
	
	package.base_price = 0
	package.save()
	frappe.msgprint(_("All prices have been reset"))
	return package

