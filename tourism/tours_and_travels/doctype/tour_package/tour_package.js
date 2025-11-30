// Copyright (c) 2024, Omar Ahmed Sabry and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tour Package', {
	refresh: function(frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(__('Generate Itinerary'), function() {
				frappe.prompt([
					{
						label: 'Arrival Date',
						fieldname: 'arrival_date',
						fieldtype: 'Date',
						reqd: 1
					},
					{
						label: 'Departure Date',
						fieldname: 'departure_date',
						fieldtype: 'Date',
						reqd: 1
					}
				], function(values) {
					frappe.call({
						method: 'tourism.tours_and_travels.doctype.tour_package.tour_package.generate_itinerary',
						args: {
							package_name: frm.doc.name,
							arrival_date: values.arrival_date,
							departure_date: values.departure_date
						},
						callback: function(r) {
							if (r.message) {
								frm.reload_doc();
								frappe.msgprint(__('Itinerary generated successfully'));
							}
						}
					});
				}, __('Generate Itinerary'), __('Generate'));
			}, __('Actions'));
			
			frm.add_custom_button(__('Update Prices from Contracts'), function() {
				frappe.call({
					method: 'tourism.tours_and_travels.doctype.tour_package.tour_package.update_prices_from_contracts',
					args: {
						package_name: frm.doc.name
					},
					callback: function(r) {
						if (r.message) {
							frm.reload_doc();
						}
					}
				});
			}, __('Actions'));
			
			frm.add_custom_button(__('Reset Prices'), function() {
				frappe.confirm(__('Are you sure you want to reset all prices to zero?'), function() {
					frappe.call({
						method: 'tourism.tours_and_travels.doctype.tour_package.tour_package.reset_prices',
						args: {
							package_name: frm.doc.name
						},
						callback: function(r) {
							if (r.message) {
								frm.reload_doc();
							}
						}
					});
				});
			}, __('Actions'));
		}
	},
	
	duration_days: function(frm) {
		if (frm.doc.duration_days) {
			frm.set_value('duration_nights', frm.doc.duration_days - 1);
		}
	}
});

// Child table calculations
frappe.ui.form.on('Tour Package Hotel', {
	nights: function(frm, cdt, cdn) {
		calculate_hotel_total(frm, cdt, cdn);
	},
	rate_per_night: function(frm, cdt, cdn) {
		calculate_hotel_total(frm, cdt, cdn);
	}
});

frappe.ui.form.on('Tour Package Restaurant', {
	meals_count: function(frm, cdt, cdn) {
		calculate_restaurant_total(frm, cdt, cdn);
	},
	rate_per_person: function(frm, cdt, cdn) {
		calculate_restaurant_total(frm, cdt, cdn);
	}
});

frappe.ui.form.on('Tour Package Transportation', {
	days: function(frm, cdt, cdn) {
		calculate_transportation_total(frm, cdt, cdn);
	},
	rate_per_day: function(frm, cdt, cdn) {
		calculate_transportation_total(frm, cdt, cdn);
	}
});

frappe.ui.form.on('Tour Package Guide', {
	days: function(frm, cdt, cdn) {
		calculate_guide_total(frm, cdt, cdn);
	},
	rate: function(frm, cdt, cdn) {
		calculate_guide_total(frm, cdt, cdn);
	}
});

frappe.ui.form.on('Tour Package Attraction', {
	qty: function(frm, cdt, cdn) {
		calculate_attraction_total(frm, cdt, cdn);
	},
	entry_fee: function(frm, cdt, cdn) {
		calculate_attraction_total(frm, cdt, cdn);
	}
});

function calculate_hotel_total(frm, cdt, cdn) {
	var row = locals[cdt][cdn];
	row.total_amount = (row.nights || 0) * (row.rate_per_night || 0);
	frm.refresh_field('hotels');
}

function calculate_restaurant_total(frm, cdt, cdn) {
	var row = locals[cdt][cdn];
	row.total_amount = (row.meals_count || 0) * (row.rate_per_person || 0);
	frm.refresh_field('restaurants');
}

function calculate_transportation_total(frm, cdt, cdn) {
	var row = locals[cdt][cdn];
	row.total_amount = (row.days || 0) * (row.rate_per_day || 0);
	frm.refresh_field('transportations');
}

function calculate_guide_total(frm, cdt, cdn) {
	var row = locals[cdt][cdn];
	row.total_amount = (row.days || 0) * (row.rate || 0);
	frm.refresh_field('guides');
}

function calculate_attraction_total(frm, cdt, cdn) {
	var row = locals[cdt][cdn];
	row.total_amount = (row.qty || 0) * (row.entry_fee || 0);
	frm.refresh_field('attractions');
}

