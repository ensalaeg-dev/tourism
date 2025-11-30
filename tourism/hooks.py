app_name = "tourism"
app_title = "Tourism"
app_publisher = "Omar Ahmed Sabry"
app_description = "An ERPNext module that manages tourism"
app_email = "ensala.eg@gmail.com"
app_license = "mit"

# Apps
# ------------------

required_apps = ["erpnext"]

# Each item in the list will be shown as an app in the apps page
add_to_apps_screen = [
	{
		"name": "tourism",
		"logo": "/assets/tourism/images/tourism-logo.png",
		"title": "Tourism",
		"route": "/app/tours-and-travels",
	}
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/tourism/css/tourism.css"
# app_include_js = "/assets/tourism/js/tourism.js"

# include js, css files in header of web template
# web_include_css = "/assets/tourism/css/tourism.css"
# web_include_js = "/assets/tourism/js/tourism.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "tourism/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Tour Package": "tours_and_travels/doctype/tour_package/tour_package.js",
	"Tour Registration": "tours_and_travels/doctype/tour_registration/tour_registration.js",
	"Hotel": "hotel_management/doctype/hotel/hotel.js",
	"Hotel Folio": "hotel_management/doctype/hotel_folio/hotel_folio.js",
	"Hotel Reservation": "hotel_management/doctype/hotel_reservation/hotel_reservation.js",
	"Hotel Room Master": "hotel_management/doctype/hotel_room_master/hotel_room_master.js",
	"Room Type": "hotel_management/doctype/room_type/room_type.js",
}

# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "tourism/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "tourism.utils.jinja_methods",
# 	"filters": "tourism.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "tourism.install.before_install"
after_install = "tourism.setup.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "tourism.uninstall.before_uninstall"
# after_uninstall = "tourism.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "tourism.utils.before_app_install"
# after_app_install = "tourism.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "tourism.utils.before_app_uninstall"
# after_app_uninstall = "tourism.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

notification_config = "tourism.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Tour Registration": {
		"after_insert": "tourism.tours_and_travels.doctype.tour_registration.tour_registration.create_crm_opportunity",
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"tourism.tasks.all"
# 	],
# 	"daily": [
# 		"tourism.tasks.daily"
# 	],
# 	"hourly": [
# 		"tourism.tasks.hourly"
# 	],
# 	"weekly": [
# 		"tourism.tasks.weekly"
# 	],
# 	"monthly": [
# 		"tourism.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "tourism.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "tourism.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "tourism.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["tourism.utils.before_request"]
# after_request = ["tourism.utils.after_request"]

# Job Events
# ----------
# before_job = ["tourism.utils.before_job"]
# after_job = ["tourism.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"tourism.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Fixtures
# --------
fixtures = [
	{
		"doctype": "Custom Field",
		"filters": [["module", "in", ["Tourism", "Tours And Travels", "Hotel Management", "Restaurant Management", "Transportation Management", "Travel Services"]]]
	},
	{
		"doctype": "Property Setter",
		"filters": [["module", "in", ["Tourism", "Tours And Travels", "Hotel Management", "Restaurant Management", "Transportation Management", "Travel Services"]]]
	},
]
