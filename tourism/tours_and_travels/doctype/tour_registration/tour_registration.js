// Copyright (c) 2024, Omar Ahmed Sabry and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tour Registration', {
	refresh: function(frm) {
		if (!frm.is_new()) {
			// Add CRM buttons
			if (!frm.doc.crm_lead) {
				frm.add_custom_button(__('Create Lead'), function() {
					frappe.call({
						method: 'tourism.tours_and_travels.doctype.tour_registration.tour_registration.create_lead_from_registration',
						args: {
							registration_name: frm.doc.name
						},
						callback: function(r) {
							if (r.message) {
								frm.reload_doc();
								frappe.msgprint(__('Lead {0} created', [r.message]));
							}
						}
					});
				}, __('CRM'));
			}
			
			if (frm.doc.crm_lead) {
				frm.add_custom_button(__('View Lead'), function() {
					frappe.set_route('Form', 'Lead', frm.doc.crm_lead);
				}, __('CRM'));
			}
			
			if (frm.doc.crm_opportunity) {
				frm.add_custom_button(__('View Opportunity'), function() {
					frappe.set_route('Form', 'Opportunity', frm.doc.crm_opportunity);
				}, __('CRM'));
			}
		}
	},
	
	tour_package: function(frm) {
		if (frm.doc.tour_package && frm.doc.registration_type === 'With Package') {
			frappe.call({
				method: 'tourism.tours_and_travels.doctype.tour_registration.tour_registration.get_package_details',
				args: {
					tour_package: frm.doc.tour_package
				},
				callback: function(r) {
					if (r.message) {
						var details = r.message;
						
						// Set basic fields
						frm.set_value('region', details.region);
						frm.set_value('package_category', details.package_category);
						
						// Clear and populate child tables
						frm.clear_table('hotels');
						details.hotels.forEach(function(hotel) {
							var row = frm.add_child('hotels');
							row.hotel = hotel.hotel;
							row.room_type = hotel.room_type;
							row.nights = hotel.nights;
							row.rate_per_night = hotel.rate_per_night;
							row.total_amount = hotel.total_amount;
						});
						
						frm.clear_table('restaurants');
						details.restaurants.forEach(function(restaurant) {
							var row = frm.add_child('restaurants');
							row.restaurant = restaurant.restaurant;
							row.meal_type = restaurant.meal_type;
							row.rate_per_person = restaurant.rate_per_person;
							row.pax = frm.doc.total_pax || 1;
						});
						
						frm.clear_table('transportations');
						details.transportations.forEach(function(transport) {
							var row = frm.add_child('transportations');
							row.transportation = transport.transportation;
							row.vehicle = transport.vehicle;
							row.rate = transport.rate;
						});
						
						frm.clear_table('guides');
						details.guides.forEach(function(guide) {
							var row = frm.add_child('guides');
							row.guide = guide.guide;
							row.service_type = guide.service_type;
							row.rate = guide.rate;
							row.hours = 1;
						});
						
						frm.clear_table('attractions');
						details.attractions.forEach(function(attraction) {
							var row = frm.add_child('attractions');
							row.attraction = attraction.attraction;
							row.entry_fee = attraction.entry_fee;
							row.pax = frm.doc.total_pax || 1;
						});
						
						frm.refresh_fields();
						frappe.msgprint(__('Package details loaded'));
					}
				}
			});
		}
	},
	
	number_of_adults: function(frm) {
		calculate_total_pax(frm);
	},
	
	number_of_children: function(frm) {
		calculate_total_pax(frm);
	},
	
	discount_amount: function(frm) {
		frm.set_value('grand_total', (frm.doc.total_cost || 0) - (frm.doc.discount_amount || 0));
	}
});

function calculate_total_pax(frm) {
	frm.set_value('total_pax', (frm.doc.number_of_adults || 0) + (frm.doc.number_of_children || 0));
}

// Child table calculations
frappe.ui.form.on('Tour Registration Hotel', {
	nights: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		row.total_amount = (row.nights || 0) * (row.rate_per_night || 0);
		frm.refresh_field('hotels');
	},
	rate_per_night: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		row.total_amount = (row.nights || 0) * (row.rate_per_night || 0);
		frm.refresh_field('hotels');
	}
});

frappe.ui.form.on('Tour Registration Restaurant', {
	pax: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		row.total_amount = (row.pax || 0) * (row.rate_per_person || 0);
		frm.refresh_field('restaurants');
	},
	rate_per_person: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		row.total_amount = (row.pax || 0) * (row.rate_per_person || 0);
		frm.refresh_field('restaurants');
	}
});

frappe.ui.form.on('Tour Registration Guide', {
	hours: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		row.total_amount = (row.hours || 0) * (row.rate || 0);
		frm.refresh_field('guides');
	},
	rate: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		row.total_amount = (row.hours || 0) * (row.rate || 0);
		frm.refresh_field('guides');
	}
});

frappe.ui.form.on('Tour Registration Attraction', {
	pax: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		row.total_amount = (row.pax || 0) * (row.entry_fee || 0);
		frm.refresh_field('attractions');
	},
	entry_fee: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		row.total_amount = (row.pax || 0) * (row.entry_fee || 0);
		frm.refresh_field('attractions');
	}
});

