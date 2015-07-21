from Products.CMFCore.utils import getToolByName

default_profile = 'profile-ruddocom.policy:default'

def upgrade_1_to_2(context):
    context.runImportStepFromProfile(default_profile, 'propertiestool')
