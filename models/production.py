from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProductionStatus(models.Model):
    _name = 'production.status'
    _description = 'Merchant Time and Action'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'production_status'

    production_status = fields.Char(
        string='PS#', 
        required=True, 
        copy=False, 
        readonly=True, 
        default='New'
    )
    # State
    state = fields.Selection([
        ('new', 'New'),
        ('onhold', 'On Hold'),
        ('hold', 'Hold'),
        ('material_procurment', 'Material procurment'),
        ('cancel', 'Cancel')
    ], string='Status', default='new', tracking=True)
    # SO and Vendor Information
    sale_order_id = fields.Many2one(
        'sale.order', 
        string='Sale Order', 
        tracking=True, 
        ondelete='cascade'
    )
    sale_order_line_id = fields.Many2one('sale.order.line', string='Sale Order Line', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity', required=True)
    buyer_product_code = fields.Char('Buyer Product Code')
    po_issue_date = fields.Date(string='PO Issue Date', related='sale_order_id.cus_po_issue_date',tracking=True)
    proforma_number = fields.Char('Proforma Number')
    vendor_id = fields.Many2one(
        'res.partner', 
        string='Vendor', 
        tracking=True,
        domain=[('supplier_rank', '>', 0)]
    )
    sales_team_id = fields.Many2one('crm.team', string='Sales Team', tracking=True) 
    partner_name = fields.Many2one(
        'res.partner', 
        string='Partner Name', 
        required=True, 
        tracking=True, 
        domain=[('customer_rank', '>', 0)]
    )
    vendor_product_code = fields.Char('Vendor Product Code')
    vendor_ex_date = fields.Date(string='Vendor Ex Date', related='sale_order_id.cus_ex_fact_date', tracking=True)
    so_number = fields.Char(
        string='SO#', 
        related='sale_order_id.name', 
        store=True,
        readonly=True
    )
    buyer_order_no = fields.Char(string='Buyer Order No', related='sale_order_id.cus_buyer_order_no',tracking=True)
    sales_person_id = fields.Many2one('res.users', string='Sales Person', tracking=True)
    
    @api.model
    def create(self, vals):
        if vals.get('production_status', 'New') == 'New':
            vals['production_status'] = self.env['ir.sequence'].next_by_code('production.status') or 'New'
        return super(ProductionStatus, self).create(vals)
    