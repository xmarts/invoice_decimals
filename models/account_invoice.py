
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
            #    amount= line.amount_total
            #    valor = round(amount, 2)
            #    line.write({'amount_total': valor})
            for l in invoice.invoice_line_ids:
                redondeo = round(l.price_unit, 2)
                l.write({'price_unit': redondeo})
            #    redondeo = round(l.price_subtotal, 2)
            #    l.write({'price_subtotal': redondeo})
            iva = self.amount_untaxed * 0.16
            invoice.write({'amount_tax': iva})
            suma = self.amount_untaxed + iva
            invoice.write({'amount_total_signed': suma})
            invoice.write({'amount_total': suma})

            #    for t in  l.invoice_line_tax_ids:
            #        monto= t.amount_total
            #amount_untax_redondeo= round(invoice.amount_untaxed,2)
            #invoice.write({'amount_untaxed': amount_untax_redondeo})
            #amount_tax_redondeo = round(invoice.amount_tax, 2)
            #invoice.write({'amount_tax': amount_tax_redondeo})
            #amount_total_redondeo = round(invoice.amount_total, 2)
            #invoice.write({'amount_total': amount_total_redondeo})
            #amount_total_signed_redondeo = round(invoice.amount_total_signed, 2)
            #invoice.write({'amount_total_signed': amount_total_signed_redondeo})
            #residual_redondeo = round(invoice.residual, 2)
            #invoice.write({'residual': residual_redondeo})
            invoice_tax = self.env['account.invoice.tax'].search([('invoice_id','=',invoice.id)])
            for i in invoice_tax:
            #    x_redondeo = round(i.amount_total, 2)
                i.write({'amount_total': iva})
                i.write({'amount': iva})
    def compute_amount(self):
        round_curr = self.currency_id.round
        amount_untaxed = sum(line.price_subtotal for line in self.invoice_line_ids)
        self.write({'amount_untaxed': amount_untaxed})
        amount_tax = sum(round_curr(line.amount_total) for line in self.tax_line_ids)
        self.write({'amount_tax': amount_tax})
        amount_total = self.amount_untaxed + self.amount_tax
        self.write({'amount_total': amount_total})
        amount_total_company_signed = self.amount_total
        amount_untaxed_signed = self.amount_untaxed
        if self.currency_id and self.company_id and self.currency_id != self.company_id.currency_id:
            currency_id = self.currency_id.with_context(date=self.date_invoice)
            amount_total_company_signed = currency_id.compute(self.amount_total, self.company_id.currency_id)
            amount_untaxed_signed = currency_id.compute(self.amount_untaxed, self.company_id.currency_id)
        sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
        amount_total_company_signed = amount_total_company_signed * sign
        self.write({'amount_total_company_signed': amount_total_company_signed})
        amount_total_signed = self.amount_total * sign
        self.write({'amount_total_signed': amount_total_signed})
        amount_untaxed_signed = amount_untaxed_signed * sign
        self.write({'amount_untaxed_signed': amount_untaxed_signed})

