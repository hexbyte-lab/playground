# Contact Management System (C + SQLite)

This project is an **improved version** of my previous [Contact Management System in C](https://github.com/hexbyte-lab/Contact-Management-System).  
While the earlier version stored data in files, this one uses an **SQLite database** for persistent storage, better performance, and easier data management.

A simple, terminal-based **Contact Management System** written in C, demonstrating core CRUD operations (Create, Read, Update, Delete) with modular code design.

---

## Features

- Add new contacts (name, phone, note)
- View all saved contacts
- Edit contact details by ID
- Delete contacts with confirmation
- Modular structure (`add_contact.c`, `view_contact.c`, etc.)
- SQLite-based storage for persistence

---


## Features

- Add new contacts  
- View all contacts  
- Edit existing contacts  
- Delete contacts  
- Data stored persistently using SQLite  
- Simple command-line interface (CLI)


---

## Requirements

- **C Compiler** (GCC, clang, etc.)
- **SQLite3** development files  
  - On Windows: place `sqlite3.c`, `sqlite3.h`, and `sqlite3.dll` in your project folder.

---

##  How to Build and Run

### **Compile**
 gcc main.c add_contact.c view_contact.c edit_contact.c delete_contact.c db.c sqlite3.c -o contacts.exe -lws2_32
./contacts.exe

## How It Works

Each main feature is split into a separate file for modularity:

| File | Description |
|------|--------------|
| `main.c` | The entry point; displays menu and handles user input |
| `db.c` / `db.h` | Handle database connection, creation, and closing |
| `add_contact.c` | Add new contact to database |
| `view_contact.c` | Display all saved contacts |
| `edit_contact.c` | Update contact information |
| `delete_contact.c` | Remove a contact by ID |
| `sqlite3.*` | SQLite database engine files |
