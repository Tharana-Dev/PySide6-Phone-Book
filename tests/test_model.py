import json
from pathlib import Path

import pytest

from model import Contact, ContactBook


# ---------- Contact ----------

def test_contact_valid():
    c = Contact("Ada", "Lovelace", "123", "ada@example.com")
    assert c.first_name == "Ada"
    assert c.last_name == "Lovelace"
    assert c.phone == "123"
    assert c.email == "ada@example.com"


def test_contact_frozen():
    c = Contact("Ada", "Lovelace", "123", "ada@example.com")
    with pytest.raises(Exception):
        c.first_name = "Bob"


@pytest.mark.parametrize("fields", [
    ("", "Lovelace", "123", "a@b.com"),
    ("Ada", "", "123", "a@b.com"),
    ("Ada", "Lovelace", "", "a@b.com"),
    ("Ada", "Lovelace", "123", ""),
    ("   ", "Lovelace", "123", "a@b.com"),
    ("Ada", "   ", "123", "a@b.com"),
    ("Ada", "Lovelace", "   ", "a@b.com"),
    ("Ada", "Lovelace", "123", "   "),
])
def test_contact_blank_fields(fields):
    with pytest.raises(ValueError):
        Contact(*fields)


# ---------- ContactBook.add ----------

def test_add_appends_and_returns():
    book = ContactBook()
    c = book.add("Ada", "Lovelace", "123", "a@b.com")
    assert book.contacts == [c]
    assert c.first_name == "Ada"


def test_add_multiple():
    book = ContactBook()
    book.add("Ada", "Lovelace", "1", "a@b.com")
    book.add("Alan", "Turing", "2", "t@b.com")
    assert len(book.contacts) == 2


def test_add_blank_raises():
    book = ContactBook()
    with pytest.raises(ValueError):
        book.add("", "Lovelace", "123", "a@b.com")
    assert book.contacts == []


def test_init_from_list():
    c = Contact("Ada", "Lovelace", "123", "a@b.com")
    book = ContactBook([c])
    assert book.contacts == [c]


# ---------- ContactBook.remove ----------

def test_remove_returns_contact():
    book = ContactBook()
    a = book.add("Ada", "Lovelace", "1", "a@b.com")
    b = book.add("Alan", "Turing", "2", "t@b.com")
    assert book.remove(0) == a
    assert book.contacts == [b]


def test_remove_negative_index():
    book = ContactBook()
    book.add("Ada", "Lovelace", "1", "a@b.com")
    book.add("Alan", "Turing", "2", "t@b.com")
    assert book.remove(-1).first_name == "Alan"


def test_remove_out_of_range():
    book = ContactBook()
    with pytest.raises(IndexError):
        book.remove(0)


# ---------- save / load ----------

def test_save_writes_json(tmp_path: Path):
    book = ContactBook()
    book.add("Ada", "Lovelace", "123", "a@b.com")
    path = tmp_path / "contacts.json"

    book.save(path)

    data = json.loads(path.read_text(encoding="utf-8"))
    assert data == [{
        "first_name": "Ada",
        "last_name": "Lovelace",
        "phone": "123",
        "email": "a@b.com",
    }]


def test_save_empty_book(tmp_path: Path):
    path = tmp_path / "contacts.json"
    ContactBook().save(path)
    assert json.loads(path.read_text(encoding="utf-8")) == []


def test_load_roundtrip(tmp_path: Path):
    book = ContactBook()
    book.add("Ada", "Lovelace", "123", "a@b.com")
    book.add("Alan", "Turing", "456", "t@b.com")
    path = tmp_path / "contacts.json"

    book.save(path)

    other = ContactBook()
    other.load(path)
    assert other.contacts == book.contacts


def test_load_replaces_existing(tmp_path: Path):
    path = tmp_path / "contacts.json"
    path.write_text(
        json.dumps([{"first_name": "Ada", "last_name": "Lovelace",
                     "phone": "1", "email": "a@b.com"}]),
        encoding="utf-8",
    )

    book = ContactBook()
    book.add("Old", "Name", "999", "o@b.com")
    book.load(path)

    assert len(book.contacts) == 1
    assert book.contacts[0].first_name == "Ada"


def test_load_not_a_list(tmp_path: Path):
    path = tmp_path / "contacts.json"
    path.write_text(json.dumps({"first_name": "Ada"}), encoding="utf-8")

    with pytest.raises(ValueError):
        ContactBook().load(path)


def test_load_blank_field_rejected(tmp_path: Path):
    path = tmp_path / "contacts.json"
    path.write_text(
        json.dumps([{"first_name": "", "last_name": "Lovelace",
                     "phone": "1", "email": "a@b.com"}]),
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        ContactBook().load(path)


def test_load_missing_field(tmp_path: Path):
    path = tmp_path / "contacts.json"
    path.write_text(
        json.dumps([{"first_name": "Ada", "phone": "1"}]),
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        ContactBook().load(path)

def test_contact_strips_whitespace():
    c = Contact("  Ada  ", "  Lovelace  ", "  123  ", "  a@b.com  ")
    assert c.first_name == "Ada"
    assert c.last_name == "Lovelace"
    assert c.phone == "123"
    assert c.email == "a@b.com"