
from openerp import models, fields, api, _, tools
from openerp.exceptions import UserError, RedirectWarning, ValidationError

import logging
_logger = logging.getLogger(__name__)
class AccountInvoice(models.Model):
    _inherit ='account.invoice'

    @api.multi
    def action_setting(self):
        for invoice in self:
            #for line in invoice.tax_line_ids:
            #3    amount= line.amount_total
            #    valor = round(amount, 2)
            #    line.write({'amount_total': valor})
             #   line.write({'amount': valor})
            for l in invoice.invoice_line_ids:
            #    redondeo = round(l.price_unit, 2)
            #    l.write({'price_unit': redondeo})
                redondeo = round(l.price_subtotal, 2)
                l.write({'price_subtotal': redondeo})
            #amount_untax_redondeo= round(invoice.amount_untaxed,2)
            #invoice.write({'amount_untaxed': amount_untax_redondeo})
            amount_tax_redondeo = round(invoice.amount_tax, 2)
            invoice.write({'amount_tax': amount_tax_redondeo})
            #amount_total_redondeo = round(invoice.amount_total, 2)
            #invoice.write({'amount_total': amount_total_redondeo})
            #amount_total_signed_redondeo = round(invoice.amount_total_signed, 2)
            #invoice.write({'amount_total_signed': amount_total_signed_redondeo})
            #residual_redondeo = round(invoice.residual, 2)
            #invoice.write({'residual': residual_redondeo})
            invoice_tax = self.env['account.invoice.tax'].search([('invoice_id','=',invoice.id)])
            for i in invoice_tax:
                x_redondeo = round(i.amount_total, 2)
                i.write({'amount_total': x_redondeo})

