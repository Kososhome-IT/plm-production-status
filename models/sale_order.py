from odoo import models, fields, _   # <-- ADDED _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        result = super().action_confirm()
        for order in self:
            for line in order.order_line:
                existing = self.env['production.status'].search([
                    ('sale_order_line_id', '=', line.id)
                ], limit=1)
                if not existing:
                    self.env['production.status'].create({
                        'sale_order_id': order.id,
                        'vendor_id':order.vendor_id.id,
                        'sales_team_id':order.team_id.id,
                        'vendor_ex_date': order.cus_ex_fact_date,
                        'po_issue_date': order.cus_po_issue_date,
                        'buyer_order_no': order.cus_buyer_order_no,
                        'sale_order_line_id': line.id,
                        'product_id': line.product_id.id,
                        'quantity': line.product_uom_qty,
                        'partner_name': order.partner_id.id,
                    })
        return result


    def action_view_production(self):
        """Smart button action to view Merchant TnA"""
        self.ensure_one()

        tna = self.env['production.status'].search([
            ('sale_order_id', '=', self.id)
        ], limit=1)

        if not tna:
            raise UserError(_('No Merchant TnA record found for this Sale Order.'))

        return {
            'type': 'ir.actions.act_window',
            'name': 'Merchant TnA',
            'res_model': 'production.status',
            'view_mode': 'form',
            'res_id': tna.id,
            'target': 'current',
        }
