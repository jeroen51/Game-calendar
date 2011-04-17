from django.utils.translation import ugettext as _

def getmonths():
    months = [ _('January'), 
               _('February'), 
               _('March'), 
               _('April'), 
               _('May'), 
               _('June'), 
               _('July'), 
               _('August'), 
               _('September'),
               _('October'),
               _('November'),
               _('December') ]
    return months

def getmonthname(monthnr):
    return getmonths()[monthnr - 1]
