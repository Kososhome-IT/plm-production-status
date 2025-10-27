from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        result = super().action_confirm()
        for order in self:
            for line in order.order_line:
                self.env['production.status'].create({
                    'sale_order_line_id': line.id,
                    'product_id': line.product_id.id,
                    'quantity': line.product_uom_qty,
                    'partner_name':order.partner_id.id
                    # Add other necessary fields here (product, qty, etc.)
                })
        return result
