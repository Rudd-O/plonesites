# -*- extra stuff goes here -*-

# monkey patches

from Products.CMFCore.utils import getToolByName
from plone.app.contenttypes.migration.vocabularies import ATCT_LIST


from plone.app.contenttypes.migration.browser import ATCTMigratorHelpers


def objects_to_be_migrated(self):
    """ Return the number of AT objects in the portal """
    catalog = getToolByName(self.context, "portal_catalog")
    #import pdb; pdb.set_trace()
    query = {'meta_type': [i['old_meta_type'] for i in ATCT_LIST.values()]}
    #if HAS_MULTILINGUAL and 'Language' in catalog.indexes():
    #    query['Language'] = 'all'
    brains = catalog(query)
    self._objects_to_be_migrated = len(brains)
    return self._objects_to_be_migrated


ATCTMigratorHelpers.objects_to_be_migrated = objects_to_be_migrated


from plone.locking.interfaces import ILockable
from OFS.interfaces import IOrderedContainer
from Products.contentmigration.basemigrator.migrator import BaseMigrator

def migrate(self, unittest=0):
    """Migrates the object
    """
    beforeChange, afterChange = self.getMigrationMethods()

    # Unlock according to plone.locking:
    lockable = ILockable(self.old, None)
    if lockable and lockable.locked():
        lockable.unlock()
    # Unlock according to webdav:
    if self.old.wl_isLocked():
        self.old.wl_clearLocks()

    for method in beforeChange:
        __traceback_info__ = (self, method, self.old, self.orig_id)
        # may raise an exception, catch it later
        method()
    # preserve position on rename
    self.need_order = IOrderedContainer.providedBy(self.parent)
    if self.need_order:
        self._position = self.parent.getObjectPosition(self.orig_id)
    self.renameOld()
    self.createNew()

    for method in afterChange:
        __traceback_info__ = (self, method, self.old, self.orig_id)
        # may raise an exception, catch it later
        try:
            method()
        except:
            pass

    self.reorder()
    self.remove()

BaseMigrator.migrate = migrate
