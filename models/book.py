from odoo import models, fields, api


class Book(models.Model):
    _name = "library.book"
    _description = "Library Book"
    _order = "name"

    name = fields.Char(
        string="Judul Buku",
        required=True,
    )

    author = fields.Char(
        string="Pengarang",
        required=True,
    )

    isbn = fields.Char(
        string="ISBN",
    )

    category_id = fields.Many2one(
        "library.category",
        string="Kategori",
    )

    total_copies = fields.Integer(
        string="Total Buku",
        default=1,
        required=True,
    )

    available_copies = fields.Integer(
        string="Buku Tersedia",
        compute="_compute_available",
        store=False,
    )

    active = fields.Boolean(
        string="Aktif",
        default=True,
    )

    _sql_constraints = [
        (
            "isbn_unique",
            "unique(isbn)",
            "ISBN sudah digunakan."
        )
    ]

    @api.depends("total_copies")
    def _compute_available(self):
        Borrowing = self.env["library.borrowing"]

        for rec in self:
            borrowed = Borrowing.search_count([
                ("book_id", "=", rec.id),
                ("state", "in", ["borrowed", "overdue"])
            ])

            rec.available_copies = max(rec.total_copies - borrowed, 0)


class Category(models.Model):
    _name = "library.category"
    _description = "Book Category"
    _order = "name"

    name = fields.Char(
        string="Nama Kategori",
        required=True,
    )