# Copyright (c) 2024, Omar Ahmed Sabry and contributors
# For license information, please see license.txt

import frappe
from frappe.utils.nestedset import NestedSet


class Hotel(NestedSet):
	nsm_parent_field = "parent_hotel"

	def validate(self):
		self.update_region_info()
		self.validate_parent()

	def update_region_info(self):
		"""Update city, state, country from region if selected"""
		if self.region:
			region = frappe.get_doc("Region", self.region)
			if not self.city:
				self.city = region.city
			if not self.state:
				self.state = region.state
			if not self.country:
				self.country = region.country

	def validate_parent(self):
		"""Validate that parent hotel is a group"""
		if self.parent_hotel:
			parent = frappe.get_value("Hotel", self.parent_hotel, "is_group")
			if not parent:
				frappe.throw(
					frappe._("Parent Hotel {0} must be a group").format(self.parent_hotel)
				)

	def on_update(self):
		super().on_update()
		self.validate_one_root()

	def on_trash(self):
		# Check if this hotel has any child hotels
		if frappe.db.exists("Hotel", {"parent_hotel": self.name}):
			frappe.throw(
				frappe._("Cannot delete {0} as it has child hotels").format(self.name)
			)
		super().on_trash()
