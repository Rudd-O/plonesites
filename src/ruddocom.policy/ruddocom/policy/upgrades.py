from Products.CMFCore.utils import getToolByName

default_profile = 'profile-ruddocom.policy:default'

def upgrade_to_8(context):
    context.runImportStepFromProfile(default_profile, 'registry')
