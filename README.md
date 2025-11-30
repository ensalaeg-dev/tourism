# Tourism

An ERPNext module that manages tourism, tours and travels operations including hotel management, restaurant management, transportation management, and travel services.

## Features

### Tours And Travels

#### Configuration
- **Region**: Manage locations by city, state, and country
- **Package Category**: Categorize tour packages (Adventure, Beach, Cultural, etc.)
- **Travelling Season**: Manage seasonal pricing with price multipliers

#### Tours And Travels Setup
- **Tourism Contract**: Manage hotel-wise, restaurant-wise, and transportation-wise contracts with region-wise package contract types
- **Tour Package**: 
  - Manage region-wise package type and category
  - Hotel, restaurant, and transportation packages
  - Guide and attraction packages
  - Auto-generate itinerary based on arrival/departure dates
  - Update/reset prices from contracts
- **Tour Registration**:
  - Auto-fetch package details from tour packages
  - Support for with-package and without-package registrations
  - CRM integration (create Leads and Opportunities)

#### Key Reports
- Hotel Wise Contract
- Restaurant Wise Contract
- Transportation Wise Contract
- Tour Registration Report

### Hotel Management

#### Configuration
- **Room Type**: Manage room types with occupancy and pricing

#### Hotel Setup
- **Hotel**: Manage hotel facilities, rooms with features, and images
- **Hotel Folio**: Quick entry for walk-in customers, check-in/check-out management, and invoice generation

#### Key Reports
- Hotel Details
- Hotel Folio Details

### Restaurant Management

#### Configuration
- **Meal Type**: Manage meal types (Breakfast, Lunch, Dinner, etc.)

#### Restaurant Setup
- **Restaurant**: Manage restaurant facilities, meal types with pricing, and images

#### Key Reports
- Restaurant Details

### Transportation Management

#### Configuration
- **Vehicle**: Manage vehicles with transporter, capacity, and features

#### Transportation Setup
- **Transportation**: Manage vehicles with features and status

#### Key Reports
- Transportation Details

### Travel Services

#### Configuration
- **Attraction Service**: Manage attraction services with pricing
- **Guide Service**: Manage guide services with pricing types

#### Travel Services Setup
- **Attraction**: Manage attractions with services and features
- **Guide**: Manage guides with languages, experience, and pricing

#### Key Reports
- Attraction Details
- Guide Details

## Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app tourism
bench migrate
```

## Roles

The following roles are created during installation:
- **Tourism Manager**: Full access to all tourism modules
- **Tourism User**: Read access with limited create/edit permissions
- **Hotel Manager**: Full access to hotel management
- **Restaurant Manager**: Full access to restaurant management
- **Transportation Manager**: Full access to transportation management

## Default Data

After installation, the following default data is created:
- Package Categories (Adventure, Beach, Cultural, etc.)
- Travelling Seasons (Peak, Off, Shoulder)
- Meal Types (Breakfast, Lunch, Dinner, etc.)
- Room Types (Single, Double, Twin, Suite, etc.)

## Workspaces

The module provides the following workspaces in the Desk:
- Tours And Travels
- Hotel Management
- Restaurant Management
- Transportation Management
- Travel Services

## Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/tourism
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:
- ruff
- eslint
- prettier
- pyupgrade

## License

MIT
