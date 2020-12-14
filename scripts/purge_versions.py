from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFEditions.utilities import dereference

self = app[sys.argv[-1]].aq_base

policy = getToolByName(self.context, 'portal_purgepolicy')
catalog = getToolByName(self.context, 'portal_catalog')

for count, brain in enumerate(catalog()):
    obj = brain.getObject()

    # only purge old content
    if obj.created() < (DateTime() - 30):
        obj, history_id = dereference(obj)
        # policy.beforeSaveHook(history_id, obj)
        print('purged object ' + obj.absolute_url_path())
