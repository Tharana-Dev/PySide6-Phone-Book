# My Phone Book

A small desktop contact manager built with **PySide6 (Qt for Python)**.
Add contacts through a form, view them in a list, delete them — and everything
persists to disk as JSON between sessions.

---

## Features

- Add contacts (first name, last name, phone, email)
- View all contacts in a scrollable list
- Multi-select and delete contacts
- Automatic save on close, automatic load on start
- Graceful handling of missing or corrupted data files
- Two-tab interface: **Add Data** / **View Contacts**

---

## Requirements

- Python 3.10+ (uses `list[Contact] | None` type hints)
- PySide6

Install:

```bash
pip install PySide6
```

---

## Running

```bash
python main.py
```

On first run, `contacts.json` is created automatically in the working directory.

---

## Project Structure

```
.
├── main.py            # entry point: builds app, loads/saves data, shows window
├── main_window.py     # QMainWindow: owns the book + panels, wires signals
├── input_panel.py     # form for entering a new contact
├── list_panel.py      # scrollable list of contacts with delete
├── model.py           # Contact dataclass + ContactBook (data + JSON I/O)
└── contacts.json      # auto-generated data file
```

---

## Architecture

The app follows a simple **model / view / controller** split.

### `model.py` — the data

- **`Contact`** — a frozen dataclass holding `first_name`, `last_name`,
  `phone`, `email`. Rejects blank fields at construction time.
- **`ContactBook`** — holds a list of `Contact`s. Provides `add`, `remove`,
  `save`, and `load`. This is the **single source of truth** — no other
  part of the app stores contacts.

### `input_panel.py` — the form view

A `QWidget` with four `QLineEdit`s and Add / Reset buttons.
Emits one signal:

```python
contact_added = Signal(str, str, str, str)   # (first, last, phone, email)
```

It never touches the data. It emits; someone else decides what happens.

### `list_panel.py` — the list view

A `QWidget` with a `QListWidget` and a Delete button.
Emits one signal:

```python
delete_requested = Signal(list)   # list of selected row indices
```

Exposes one method:

```python
refresh(contacts)   # wipe and redraw the list from a snapshot
```

Like `InputPanel`, it holds no data of its own — it renders whatever it's
handed and forgets it.

### `main_window.py` — the controller

Owns the `ContactBook` and both panels. Its only job is to wire them:

- When `InputPanel.contact_added` fires → add to book → refresh list.
- When `ContactListPanel.delete_requested` fires → remove from book → refresh list.

Both handlers follow the same three-step pattern:

```
mutate the book  →  refresh the list  →  (done)
```

### `main.py` — the process

Loads the book from `contacts.json` at startup, hands it to `MainWindow`,
saves on quit. Knows nothing about widgets.

---

## Data Flow

```
User clicks Add
  → InputPanel emits contact_added(first, last, phone, email)
  → MainWindow._add_contact receives it
  → ContactBook.add(...)
  → ContactListPanel.refresh(book.contacts)
  → user sees the new row (tab auto-switches to View Contacts)

User selects rows and clicks Delete
  → ContactListPanel emits delete_requested([rows])
  → MainWindow._delete_contact iterates rows in DESCENDING order
  → ContactBook.remove(row) for each
  → ContactListPanel.refresh(book.contacts)
```

**Why descending order?** Deleting index 1 first shifts index 3 down to 2.
Iterating in reverse prevents deleting the wrong contact.

---

## Persistence

- **On startup:** `main.py` calls `book.load("contacts.json")`.
  - Missing file → treated as first run, file is created empty.
  - Corrupted file → warning dialog, app starts with an empty book.
- **On quit:** `app.aboutToQuit` triggers `book.save("contacts.json")`.

The JSON format is a plain array of contact objects:

```json
[
  {
    "first_name": "Ada",
    "last_name": "Lovelace",
    "phone": "0123456789",
    "email": "ada@example.com"
  }
]
```

---

## Extending

The architecture is designed so features can be **added**, not **restructured**:

- **Click a row to edit** — store the full `Contact` on each list item via
  `UserRole`, emit an `edit_requested(Contact)` signal, populate the form.
- **Confirm before delete** — wrap the delete handler in a `QMessageBox.question`.
- **Search / filter** — add a `QLineEdit` above the list, filter before
  calling `refresh`.
- **Sort by name** — sort `book.contacts` before refreshing.

None of these require changing the model/view/controller boundaries.

---

## Known Limitations

- Fixed window size (500×400)
- Save happens only on clean exit (crash = lost changes since last save)
- No search, sort, or edit
- Single file for all contacts (no multi-address-book support)
