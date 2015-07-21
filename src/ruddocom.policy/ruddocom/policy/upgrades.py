from Products.CMFCore.utils import getToolByName

default_profile = 'profile-ruddocom.policy:default'

def upgrade_1_to_2(context):
    context.runImportStepFromProfile(default_profile, 'propertiestool')

def upgrade_2_to_3(context):
    l = context.getSite().acl_users.session
    l.timeout = 604800
    l.cookie_lifetime = 7
    l.secure = True
