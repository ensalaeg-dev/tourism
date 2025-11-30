import frappe
from frappe import _


def after_install():
	"""Setup default data after installation"""
	create_default_roles()
	create_default_data()


def create_default_roles():
	"""Create default roles for Tourism module"""
	roles = [
		{"role_name": "Tourism Manager", "desk_access": 1},
		{"role_name": "Tourism User", "desk_access": 1},
		{"role_name": "Hotel Manager", "desk_access": 1},
		{"role_name": "Restaurant Manager", "desk_access": 1},
		{"role_name": "Transportation Manager", "desk_access": 1},
	]

	for role in roles:
		if not frappe.db.exists("Role", role["role_name"]):
			doc = frappe.new_doc("Role")
			doc.role_name = role["role_name"]
			doc.desk_access = role.get("desk_access", 1)
			doc.insert(ignore_permissions=True)


def create_default_data():
	"""Create default master data"""
	# Create default Package Categories
	package_categories = [
		"Adventure",
		"Beach",
		"Cultural",
		"Eco Tourism",
		"Family",
		"Honeymoon",
		"Pilgrimage",
		"Wildlife",
	]

	for category in package_categories:
		if not frappe.db.exists("Package Category", category):
			doc = frappe.new_doc("Package Category")
			doc.category_name = category
			doc.insert(ignore_permissions=True)

	# Create default Travelling Seasons
	seasons = [
		{"season_name": "Peak Season", "description": "High demand period"},
		{"season_name": "Off Season", "description": "Low demand period"},
		{"season_name": "Shoulder Season", "description": "Moderate demand period"},
	]

	for season in seasons:
		if not frappe.db.exists("Travelling Season", season["season_name"]):
			doc = frappe.new_doc("Travelling Season")
			doc.season_name = season["season_name"]
			doc.description = season.get("description")
			doc.insert(ignore_permissions=True)

	# Create default Meal Types
	meal_types = [
		"Breakfast",
		"Lunch",
		"Dinner",
		"Brunch",
		"All Inclusive",
	]

	for meal_type in meal_types:
		if not frappe.db.exists("Meal Type", meal_type):
			doc = frappe.new_doc("Meal Type")
			doc.meal_type_name = meal_type
			doc.insert(ignore_permissions=True)

	# Create default Room Types
	room_types = [
		{"room_type_name": "Single", "description": "Single occupancy room"},
		{"room_type_name": "Double", "description": "Double occupancy room"},
		{"room_type_name": "Twin", "description": "Twin beds room"},
		{"room_type_name": "Suite", "description": "Luxury suite"},
		{"room_type_name": "Deluxe", "description": "Deluxe room"},
		{"room_type_name": "Family", "description": "Family room"},
	]

	for room_type in room_types:
		if not frappe.db.exists("Room Type", room_type["room_type_name"]):
			doc = frappe.new_doc("Room Type")
			doc.room_type_name = room_type["room_type_name"]
			doc.description = room_type.get("description")
			doc.insert(ignore_permissions=True)

	frappe.db.commit()

