#!/usr/bin/env python

import os
import logging
import transaction
import sys

from Products.CMFPlone.Portal import PloneSite


productstoupgrade = sys.argv[3:]

commit = True
if productstoupgrade and productstoupgrade[0] == "-n":
    commit = False
    productstoupgrade = productstoupgrade[1:]

if not productstoupgrade:
    raise Exception(
        "the product(s) to upgrade must "
        "be specified after the upgrade subcommand"
    )

installed = dict()
for a in (s for s in app.values() if isinstance(s, PloneSite)):
    ip = dict((x['id'], x) for x in a.portal_quickinstaller.listInstalledProducts())
    installed.update((x, True) for x in ip)

for p in productstoupgrade:
    if p not in installed:
        raise Exception("Product %s is not installed in any site" % p)

changed = ""

for a in (s for s in app.values() if isinstance(s, PloneSite)):
    ip = dict((x['id'], x) for x in a.portal_quickinstaller.listInstalledProducts())
    for i, data in ip.items():
        if i not in productstoupgrade: continue
        ui = a.portal_quickinstaller.upgradeInfo(i)
        installedVersion, newVersion = ui['installedVersion'], ui['newVersion']
        if installedVersion != newVersion:
            for k, v in ui.items():
                print "in: %s: before: %s: %s=%s" % (a.__name__, i, k, v)
            a.portal_quickinstaller.upgradeProduct(i)
            uia = a.portal_quickinstaller.upgradeInfo(i)
            for k, v in uia.items():
                print "in: %s: after:  %s: %s=%s" % (a.__name__, i, k, v)
            if changed == "":
                changed = "Upgrade: "
            else:
                changed = changed + ", "
            changed = changed + "%s from %s to %s" % (
                a.__name__, installedVersion, newVersion
            )

if commit:
    if changed:
        t = transaction.get()
        t.note(changed)
        t.commit()
