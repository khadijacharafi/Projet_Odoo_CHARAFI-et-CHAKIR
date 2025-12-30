# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Sac(models.Model):
    _name = 'sac_style_defect_recycling.sac'
    _description = 'Gestion des sacs'
    _inherit = ['mail.thread', 'mail.activity.mixin'] 
    _order = 'date_creation desc, name'

    name = fields.Char(
        string='Référence',
        required=True,
        copy=False,
        readonly=True,
        default='Nouveau',
        tracking=True
    )
    
    type_sac = fields.Selection([
        ('plastique', 'Plastique'),
        ('papier', 'Papier'),
        ('sac_main', 'Sac à Main'),
        ('sac_dos', 'Sac à Dos'),
        ('sac_voyage', 'Sac de Voyage'),
    ], string='Type de sac', required=True, tracking=True)
    
    etat = fields.Selection([
        ('nouveau', 'Nouveau'),
        ('en_stock', 'En Stock'),
        ('vendu', 'Vendu'),
        ('recycle', 'Recyclé'),
        ('defectueux', 'Défectueux'),
        ('ok', 'OK')
    ], string='État', default='nouveau', required=True, tracking=True)

    # ===== IMAGES =====
    image_1920 = fields.Image(string='Image', max_width=1920, max_height=1920)
    image_128 = fields.Image(related='image_1920', max_width=128, max_height=128, store=True)
    image_256 = fields.Image(related='image_1920', max_width=256, max_height=256, store=True)

    # ===== PRIX =====
    prix_achat = fields.Float(string='Prix d\'Achat', digits='Product Price')
    prix = fields.Float(string='Prix de Vente', digits='Product Price', required=True, default=0.0)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    
    marge = fields.Monetary(
        string='Marge',
        compute='_compute_marge',
        store=True,
        currency_field='currency_id'
    )
    
    taux_marge = fields.Float(
        string='Taux de Marge (%)',
        compute='_compute_marge',
        store=True
    )

    # ===== STOCK =====
    quantite = fields.Integer(string='Quantité', default=1)
    quantite_min = fields.Integer(string='Stock Minimum', default=5)
    emplacement = fields.Char(string='Emplacement')
    code_barre = fields.Char(string='Code-Barres')

    # ===== CARACTÉRISTIQUES =====
    taille = fields.Char(string='Dimensions')
    poids = fields.Float(string='Poids (kg)')
    matiere = fields.Char(string='Matériau')
    couleur = fields.Char(string='Couleur')
    nb_compartiments = fields.Integer(string='Compartiments', default=1)
    fermeture = fields.Char(string='Fermeture')
    doublure = fields.Char(string='Doublure')
    marque = fields.Char(string='Marque')
    origine = fields.Char(string='Origine')

    # ===== QUALITÉ =====
    etat_physique = fields.Selection([
        ('neuf', 'Neuf'),
        ('excellent', 'Excellent'),
        ('bon', 'Bon'),
        ('moyen', 'Moyen'),
        ('mauvais', 'Mauvais')
    ], string='État Physique', default='bon')
    
    note_qualite = fields.Selection([
        ('1', '⭐'),
        ('2', '⭐⭐'),
        ('3', '⭐⭐⭐'),
        ('4', '⭐⭐⭐⭐'),
        ('5', '⭐⭐⭐⭐⭐')
    ], string='Note', default='3')

    # ===== DATES =====
    date_creation = fields.Date(
        string='Date de Création',
        default=fields.Date.today,
        required=True
    )
    date_vente = fields.Date(string='Date de Vente')

    # ===== DESCRIPTIONS =====
    description = fields.Html(string='Description')
    note_interne = fields.Text(string='Notes Internes')

    # ===== AUTRES =====
    active = fields.Boolean(default=True)
    color = fields.Integer(string='Couleur Kanban', default=0)

    # ===== CALCULS =====
    @api.depends('prix', 'prix_achat')
    def _compute_marge(self):
        for record in self:
            record.marge = record.prix - record.prix_achat
            if record.prix_achat > 0:
                record.taux_marge = (record.marge / record.prix_achat) * 100
            else:
                record.taux_marge = 0.0

    # ===== CRÉATION AVEC SÉQUENCE =====
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nouveau') == 'Nouveau':
                vals['name'] = self.env['ir.sequence'].next_by_code('sac.sequence') or 'SAC-NEW'
        return super(Sac, self).create(vals_list)