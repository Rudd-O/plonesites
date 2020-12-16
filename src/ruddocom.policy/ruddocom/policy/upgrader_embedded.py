#!/usr/bin/env python

import sys

from Products.CMFPlone.utils import get_installer
import transaction


productstoupgrade = sys.argv[3:]

commit = True
if "-n" in productstoupgrade:
    commit = False
    productstoupgrade.remove("-n")

if not productstoupgrade:
    raise Exception(
        "the product(s) to upgrade must " "be specified after the upgrade subcommand"
    )

if len(productstoupgrade) != 2:
    raise Exception("the product to upgrade must follow the name (ID) of the site")

siteid, productid = productstoupgrade

qi = get_installer(app[siteid])  # pylint:disable=invalid-name,used-before-assignment
qi.upgrade_product(productid)

if commit:
    t = transaction.get()
    t.note("Upgraded %s on %s" % (productid, siteid))
    t.commit()
    print("Product %s successfully upgraded on %s." % (productid, siteid))
else:
    print("Product %s upgraded in simulation mode on %s."% (productid, siteid))
