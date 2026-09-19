# Dariora Backend - Odoo

Custom Odoo backend for Dariora Academy learning platform.

## Project Structure

```
dariora-backend-odoo/
├── custom_addons/          # Custom Odoo modules
│   └── dariora_academy/    # Main academy module
│       ├── models/         # Python models (Course, etc.)
│       ├── views/          # XML UI definitions
│       ├── controllers/    # API controllers
│       ├── security/       # Access control rules
│       └── __manifest__.py # Module metadata
├── odoo/                   # Odoo source code (git submodule)
└── .venv/                  # Python virtual environment
```

## Setup

### Prerequisites
- Python 3.10+
- PostgreSQL 12+
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/dashaaaa21/dariora-backend-odoo.git
cd dariora-backend-odoo
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install Odoo:
```bash
cd odoo
pip install -e .
cd ..
```

4. Create PostgreSQL user:
```bash
createuser -s dariora
```

5. Start Odoo:
```bash
cd odoo
python odoo-bin --addons-path=addons,../custom_addons --db_user=dariora
```

6. Access Odoo at `http://localhost:8069`

## Modules

### dariora_academy
Main module for Dariora Academy with course management.

**Features:**
- Course model with name, description, price, is_published fields
- List and form views for course management
- Menu: Dariora Academy → Courses

**Installation:**
- In Odoo UI: Apps → Search "Dariora Academy" → Install

## Development

### Adding Models
Add Python classes in `custom_addons/dariora_academy/models/`

### Adding Views
Add XML definitions in `custom_addons/dariora_academy/views/`

### Database Migrations
Update module in Odoo UI or use:
```bash
python odoo-bin -d dariora_academy -u dariora_academy
```

## License

LGPL-3
