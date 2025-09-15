

-- Tabla de Contactos
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    company TEXT,
    company_level TEXT,
    job_title TEXT,
    referred_by TEXT,
    email TEXT,
    phone TEXT,
    mobile_phone TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    country TEXT,
    postal_code TEXT,
    website TEXT,
    source TEXT,
    status TEXT DEFAULT 'Cliente potencial',
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Oportunidades
CREATE TABLE IF NOT EXISTS opportunities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    contact_id INTEGER NOT NULL,
    value REAL NOT NULL,
    stage TEXT NOT NULL DEFAULT 'Prospección',
    probability INTEGER DEFAULT 10,
    close_date DATE,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (contact_id) REFERENCES contacts (id)
);

-- Tabla de Actividades
CREATE TABLE IF NOT EXISTS activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL, -- 'call', 'email', 'meeting', 'task'
    subject TEXT NOT NULL,
    description TEXT,
    related_to INTEGER, -- contact_id or opportunity_id
    related_type TEXT, -- 'contact' or 'opportunity'
    due_date DATETIME,
    completed BOOLEAN DEFAULT FALSE,
    completed_date DATETIME,
    priority TEXT DEFAULT 'media',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Interacciones
CREATE TABLE IF NOT EXISTS interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contact_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    subject TEXT,
    description TEXT,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    duration INTEGER, -- in minutes
    outcome TEXT,
    FOREIGN KEY (contact_id) REFERENCES contacts (id)
);

-- Tabla de Etiquetas
CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    color TEXT DEFAULT '#007bff'
);

-- Tabla de relación Contacto-Etiqueta
CREATE TABLE IF NOT EXISTS contact_tags (
    contact_id INTEGER,
    tag_id INTEGER,
    PRIMARY KEY (contact_id, tag_id),
    FOREIGN KEY (contact_id) REFERENCES contacts (id),
    FOREIGN KEY (tag_id) REFERENCES tags (id)
);