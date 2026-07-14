from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Borrowing(models.Model):
    _name = "library.borrowing"
    _description = "Peminjaman Buku"
    _order = "borrow_date desc"

    name = fields.Char(
        string="Referensi",
        readonly=True,
        copy=False,
        default="New",
    )

    book_id = fields.Many2one(
        "library.book",
        string="Buku",
        required=True,
    )

    borrower_id = fields.Many2one(
        "res.partner",
        string="Peminjam",
        required=True,
    )

    borrow_date = fields.Date(
        string="Tanggal Pinjam",
        default=fields.Date.today,
        required=True,
    )

    due_date = fields.Date(
        string="Jatuh Tempo",
        default=lambda self: fields.Date.add(fields.Date.today(), days=7),
        required=True,
    )

    return_date = fields.Date(
        string="Tanggal Kembali",
        readonly=True,
    )

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("borrowed", "Dipinjam"),
            ("overdue", "Terlambat"),
            ("returned", "Dikembalikan"),
            ("cancel", "Dibatalkan"),
        ],
        string="Status",
        default="draft",
        tracking=True,
    )

    notes = fields.Text(
        string="Catatan",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = (
                    self.env["ir.sequence"].next_by_code("library.borrowing")
                    or "New"
                )
        return super().create(vals_list)

    @api.constrains("borrow_date", "due_date")
    def _check_due_date(self):
        for rec in self:
            if (
                rec.borrow_date
                and rec.due_date
                and rec.due_date < rec.borrow_date
            ):
                raise ValidationError(
                    "Tanggal jatuh tempo tidak boleh sebelum tanggal pinjam."
                )

    def action_borrow(self):
        self.ensure_one()

        if self.book_id.available_copies <= 0:
            raise ValidationError(
                "Stok buku habis."
            )

        self.state = "borrowed"

    def action_return(self):
        self.ensure_one()

        self.write({
            "state": "returned",
            "return_date": fields.Date.today(),
        })

    def action_cancel(self):
        self.ensure_one()

        self.state = "cancel"

    def action_check_overdue(self):
        today = fields.Date.today()

        overdue = self.search([
            ("state", "=", "borrowed"),
            ("due_date", "<", today),
        ])

        overdue.write({
            "state": "overdue",
        })

        return True