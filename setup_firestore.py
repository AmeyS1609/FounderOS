"""Create placeholder docs for each collection, then remove them (Firestore 'setup')."""

from __future__ import annotations

from services.firebase import SERVER_TIMESTAMP, check_permissions, get_db, init_firebase


def main() -> None:
    check_permissions()
    init_firebase()
    db = get_db()
    cols = ("briefings", "emails", "leads", "candidates", "conversations")
    for name in cols:
        ref = db.collection(name).document("_placeholder")
        ref.set({"placeholder": True, "created_at": SERVER_TIMESTAMP})
        snap = ref.get()
        if snap.exists:
            ref.delete()
        print(f"Collection {name}: OK")
    print("Firestore setup complete")


if __name__ == "__main__":
    main()
