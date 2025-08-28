def post_remove_partner_name_unique_index(cr, registry):
    cr.execute("DROP INDEX IF EXISTS partner_unique_person_name_per_company;")
    cr.execute("DROP INDEX IF EXISTS partner_unique_person_name_unaccent_per_company;")
