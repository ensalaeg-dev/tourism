// Copyright (c) 2024, Omar Ahmed Sabry and contributors
// For license information, please see license.txt

frappe.ui.form.on('Hotel', {
	refresh: function(frm) {
		// Add tree view button
		frm.add_custom_button(__('View Tree'), function() {
			frappe.set_route('Tree', 'Hotel');
		}, __('View'));

		// Filter parent_hotel to only show groups
		frm.set_query('parent_hotel', function() {
			return {
				filters: {
					'is_group': 1,
					'name': ['!=', frm.doc.name]
				}
			};
		});

		if (!frm.is_new()) {
			// Add Room button
			frm.add_custom_button(__('Add Room'), function() {
				frappe.new_doc('Hotel Room Master', {
					hotel: frm.doc.name
				});
			}, __('Actions'));

			// View Child Hotels button (only for groups)
			if (frm.doc.is_group) {
				frm.add_custom_button(__('View Child Hotels'), function() {
					frappe.set_route('List', 'Hotel', {
						parent_hotel: frm.doc.name
					});
				}, __('View'));
			}
			
			// View Rooms button
			frm.add_custom_button(__('View Rooms'), function() {
				frappe.set_route('List', 'Hotel Room Master', {
					hotel: frm.doc.name
				});
			}, __('View'));
			
			// View Folios button
			frm.add_custom_button(__('View Folios'), function() {
				frappe.set_route('List', 'Hotel Folio', {
					hotel: frm.doc.name
				});
			}, __('View'));
			
			// View Reservations button
			frm.add_custom_button(__('View Reservations'), function() {
				frappe.set_route('List', 'Hotel Reservation', {
					hotel: frm.doc.name
				});
			}, __('View'));
			
			// New Folio button
			frm.add_custom_button(__('New Folio'), function() {
				frappe.new_doc('Hotel Folio', {
					hotel: frm.doc.name
				});
			}, __('Create'));
			
			// New Reservation button
			frm.add_custom_button(__('New Reservation'), function() {
				frappe.new_doc('Hotel Reservation', {
					hotel: frm.doc.name
				});
			}, __('Create'));
			
			// Room Availability Report
			frm.add_custom_button(__('Room Availability'), function() {
				frappe.set_route('query-report', 'Room Availability', {
					hotel: frm.doc.name
				});
			}, __('Reports'));
			
			// Show room summary in dashboard
			frappe.call({
				method: 'frappe.client.get_count',
				args: {
					doctype: 'Hotel Room Master',
					filters: {
						hotel: frm.doc.name
					}
				},
				callback: function(r) {
					if (r.message) {
						frm.dashboard.add_indicator(__('Total Rooms: {0}', [r.message]), 'blue');
					}
				}
			});
			
			frappe.call({
				method: 'frappe.client.get_count',
				args: {
					doctype: 'Hotel Room Master',
					filters: {
						hotel: frm.doc.name,
						status: 'Available'
					}
				},
				callback: function(r) {
					if (r.message) {
						frm.dashboard.add_indicator(__('Available: {0}', [r.message]), 'green');
					}
				}
			});
			
			frappe.call({
				method: 'frappe.client.get_count',
				args: {
					doctype: 'Hotel Room Master',
					filters: {
						hotel: frm.doc.name,
						status: 'Occupied'
					}
				},
				callback: function(r) {
					if (r.message) {
						frm.dashboard.add_indicator(__('Occupied: {0}', [r.message]), 'red');
					}
				}
			});
		}
	},
	
	region: function(frm) {
		if (frm.doc.region) {
			frappe.db.get_doc('Region', frm.doc.region).then(function(r) {
				if (r) {
					if (!frm.doc.city) frm.set_value('city', r.city);
					if (!frm.doc.state) frm.set_value('state', r.state);
					if (!frm.doc.country) frm.set_value('country', r.country);
				}
			});
		}
	},

	is_group: function(frm) {
		// If un-checking is_group, check if there are child hotels
		if (!frm.doc.is_group && !frm.is_new()) {
			frappe.call({
				method: 'frappe.client.get_count',
				args: {
					doctype: 'Hotel',
					filters: {
						parent_hotel: frm.doc.name
					}
				},
				callback: function(r) {
					if (r.message && r.message > 0) {
						frappe.msgprint(__('Cannot uncheck Is Group as this hotel has {0} child hotel(s)', [r.message]));
						frm.set_value('is_group', 1);
					}
				}
			});
		}
	}
});

// Child table events for Hotel Room
frappe.ui.form.on('Hotel Room', {
	room_type: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		if (row.room_type) {
			frappe.db.get_doc('Room Type', row.room_type).then(function(r) {
				if (r) {
					frappe.model.set_value(cdt, cdn, 'price_per_night', r.base_price);
				}
			});
		}
	}
});

// Tree view settings
frappe.treeview_settings['Hotel'] = {
	breadcrumb: 'Hotel Management',
	title: __('Hotels'),
	get_tree_root: false,
	filters: [
		{
			fieldname: 'region',
			fieldtype: 'Link',
			options: 'Region',
			label: __('Region')
		}
	],
	get_tree_nodes: 'frappe.desk.treeview.get_children',
	add_tree_node: 'frappe.desk.treeview.add_node',
	menu_items: [
		{
			label: __('New Hotel'),
			action: function() {
				frappe.new_doc('Hotel');
			},
			condition: 'frappe.boot.user.can_create.indexOf("Hotel") !== -1'
		}
	],
	onload: function(treeview) {
		treeview.make_tree();
	},
	onrender: function(node) {
		if (node.data && node.data.star_rating) {
			$('<span class="text-muted small ml-2">' + node.data.star_rating + '</span>')
				.appendTo(node.$tree_link);
		}
	},
	extend_toolbar: true
};
