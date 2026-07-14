{
    "name": "Peminjaman Buku",
    "version": "19.0.1.0.0",
    "category": "Library",
    "summary": "peminjaman buku",
    "depends": ["base"],
    "data": [
    "security/ir.model.access.csv",

    "data/sequence.xml",

    "views/book_views.xml",
    "views/borrowing_views.xml",
    ],
    "installable": True,
    "application": True,
}
