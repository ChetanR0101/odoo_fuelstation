from odoo import models,fields,api

class FuelStation_for_cal(models.Model):
    _name='fuelstation.cal'
    fuel_type = fields.Many2one(comodel_name ="fuelstation.fueldata",string="Fuel Type") 


class FuelStation_in_stock(models.Model):
    _name= "fuelstation.instock"
    _description ="IN Fuel Record"
    name = fields.Char("Recived By")
    date = fields.Datetime("Date:")
    fuel_type = fields.Many2one(comodel_name ="fuelstation.fueldata",string="Fuel Type") 
    instock_qut= fields.Float("IN stock Quantity")
    avl_qut = fields.Float(string="Currently Avilable Quantity",related='fuel_type.avl_qut')


    @api.depends('instock_qut')
    def _update_stock(self):
        for rec in self:
            rec.fuel_type.avl_qut += rec.instock_qut 
        self.updated_stock= rec.fuel_type.avl_qut
        
    updated_stock= fields.Float(string="Updated Stock",compute=_update_stock,  store=True)



   

class FuelStation_out_stock(models.Model):
    _name="fuelstation.outstock"
    _description ="OUT Fuel Record"
    name = fields.Char("Customer Name")
    date = fields.Datetime("Date:")
    fuel_type = fields.Many2one(comodel_name ="fuelstation.fueldata",string="Fuel Type")
    order_qut= fields.Float("Fuel Quantity in Ltrs")
    fuel_price= fields.Float(string="Fuel Price",related='fuel_type.price')  
    avl_qut = fields.Float(string="Available Fuel",related='fuel_type.avl_qut')


     # for Total price
    # @api.depends('fuel_type','fuel_price','order_qut')
    # @api.onchange('fuel_type'or 'fuel_price')
    # def _cal_total(self):
    #     for rec in self:
    #         rec.total_price= rec.order_qut* rec.fuel_price
    #     self.total_price= rec.total_price

    # total_price = fields.Float(string="Total Cost",compute=_cal_total,store=True)

    # To Update stock
    @api.depends('order_qut')
    def _update_stock(self):
        for rec in self:
            rec.fuel_type.avl_qut -= rec.order_qut 
        self.updated_stock= rec.fuel_type.avl_qut

    updated_stock= fields.Float(string="Updated Stock",compute=_update_stock,  store=True)


class FuelStation_fuel_data(models.Model):
    _name="fuelstation.fueldata"
    name= fields.Char(string= "Fuel Type")
    price= fields.Float(string="Fuel Price")
    avl_qut= fields.Float(" Available Fuel")

class FuelStation_transection_rec(models.Model):
    _name="fuelstation.record"
    _inherit="fuelstation.outstock"


class FuelStation_fuel_price(models.Model):
    _name= "fuelstation.fuelprice"
    name= fields.Char(string= "Fuel Type")
    fuel_type = fields.Many2one(comodel_name ="fuelstation.fueldata",string="Fuel Type")
    fuel_price= fields.Float(string="Fuel Price",related='fuel_type.price',readonly=False) 


class FuelStation_avl_stock(models.Model):
    _name= "fuelstation.avlstock"
    name= fields.Char(string= "Fuel Type")
    fuel_type = fields.Many2one(comodel_name ="fuelstation.fueldata",string="Fuel Type")
    avl_qut = fields.Float(string="Fuel Quantity in Ltrs",related='fuel_type.avl_qut',readonly=False, store=True)