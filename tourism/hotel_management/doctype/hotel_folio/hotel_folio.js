// Copyright (c) 2024, Omar Ahmed Sabry and contributors
// For license information, please see license.txt

frappe.ui.form.on('Hotel Folio', {
	refresh: function(frm) {
		if (!frm.is_new()) {
			// Check In button
			if (frm.doc.status === 'Draft') {
				frm.add_custom_button(__('Check In'), function() {
					frappe.call({
						method: 'tourism.hotel_management.doctype.hotel_folio.hotel_folio.check_in',
						args: {
							folio_name: frm.doc.name
						},
						callback: function(r) {
							if (r.message) {
								frm.reload_doc();
								frappe.msgprint(__('Guest checked in successfully'));
							}
						}
					});
				}, __('Actions'));
			}
			
			// Check Out button
			if (frm.doc.status === 'Checked In') {
				frm.add_custom_button(__('Check Out'), function() {
					frappe.call({
						method: 'tourism.hotel_management.doctype.hotel_folio.hotel_folio.check_out',
						args: {
							folio_name: frm.doc.name
						},
						callback: function(r) {
							if (r.message) {
								frm.reload_doc();
								frappe.msgprint(__('Guest checked out successfully'));
							}
						}
					});
				}, __('Actions'));
			}
			
			// Create Invoice button
			if (!frm.doc.sales_invoice && frm.doc.customer) {
				frm.add_custom_button(__('Create Invoice'), function() {
					frappe.call({
						method: 'tourism.hotel_management.doctype.hotel_folio.hotel_folio.create_sales_invoice',
						args: {
							folio_name: frm.doc.name
						},
						callback: function(r) {
							if (r.message) {
								frm.reload_doc();
								frappe.msgprint(__('Sales Invoice {0} created', [r.message]));
							}
						}
					});
				}, __('Actions'));
			}
			
			// View Invoice button
			if (frm.doc.sales_invoice) {
				frm.add_custom_button(__('View Invoice'), function() {
					frappe.set_route('Form', 'Sales Invoice', frm.doc.sales_invoice);
				}, __('Actions'));
			}
		}
	},
	
	hotel: function(frm) {
		// Could fetch default room rate from hotel
	},
	
	room_type: function(frm) {
		if (frm.doc.room_type) {
			frappe.db.get_value('Room Type', frm.doc.room_type, 'base_price', function(r) {
				if (r && r.base_price) {
					frm.set_value('rate_per_night', r.base_price);
				}
			});
		}
	},
	
	check_in_date: function(frm) {
		calculate_nights(frm);
	},
	
	check_out_date: function(frm) {
		calculate_nights(frm);
	},
	
	rate_per_night: function(frm) {
		calculate_totals(frm);
	},
	
	paid_amount: function(frm) {
		frm.set_value('balance_amount', (frm.doc.total_amount || 0) - (frm.doc.paid_amount || 0));
	}
});

function calculate_nights(frm) {
	if (frm.doc.check_in_date && frm.doc.check_out_date) {
		var check_in = frappe.datetime.str_to_obj(frm.doc.check_in_date);
		var check_out = frappe.datetime.str_to_obj(frm.doc.check_out_date);
		var nights = frappe.datetime.get_diff(check_out, check_in);
		if (nights < 1) nights = 1;
		frm.set_value('nights', nights);
		calculate_totals(frm);
	}
}

function calculate_totals(frm) {
	var room_charges = (frm.doc.nights || 1) * (frm.doc.rate_per_night || 0);
	frm.set_value('room_charges', room_charges);
	frm.set_value('total_room_charges', room_charges);
	
	var total_services = 0;
	(frm.doc.services || []).forEach(function(service) {
		total_services += (service.qty || 0) * (service.rate || 0);
	});
	frm.set_value('total_services', total_services);
	
	var total = room_charges + total_services;
	frm.set_value('total_amount', total);
	frm.set_value('balance_amount', total - (frm.doc.paid_amount || 0));
}

frappe.ui.form.on('Hotel Folio Service', {
	hotel_service: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		if (row.hotel_service) {
			frappe.db.get_doc('Hotel Service', row.hotel_service).then(function(r) {
				if (r) {
					frappe.model.set_value(cdt, cdn, 'service_type', r.service_category);
					frappe.model.set_value(cdt, cdn, 'description', r.service_name);
					frappe.model.set_value(cdt, cdn, 'rate', r.default_rate);
					frappe.model.set_value(cdt, cdn, 'amount', (row.qty || 1) * r.default_rate);
					frm.refresh_field('services');
					calculate_totals(frm);
				}
			});
		}
	},
	qty: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		row.amount = (row.qty || 0) * (row.rate || 0);
		frm.refresh_field('services');
		calculate_totals(frm);
	},
	rate: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		row.amount = (row.qty || 0) * (row.rate || 0);
		frm.refresh_field('services');
		calculate_totals(frm);
	},
	services_remove: function(frm) {
		calculate_totals(frm);
	}
});

