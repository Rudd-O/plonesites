from ZODB.POSException import POSKeyError
def error_finder(folder, exception=POSKeyError, stop_on_first=None):
    """ start at the given folderish object.
    If stop_on_first is true, quit after one exception;
    otherwise, keep going through the whole tree."""
    for id, next_item in folder.objectItems():
        try:
            next_item.getId()
        except exception:
            print `exception`, "in folder",
            print  '/'.join(folder.getPhysicalPath()),
            print "at id:", id
            if stop_on_first:
                raise "done"   # hack to break out of recursion
        else:
            # no error, recurse if it's objectManagerish
            if hasattr(next_item.aq_base, 'objectItems'):
                error_finder(next_item, exception, stop_on_first)

error_finder(app, stop_on_first=False)
