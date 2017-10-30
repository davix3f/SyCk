from os import system as shell

def custom_import(modules_list, pip_version):
    """
    modules_list: entry a list of modules to import (ex: 'custom_import(["re", "os", "module"])' )
    pip_version: valid entries: 2 or 3, depending on the program's python version
    """
    failed_imports = []
    for index, module in enumerate(modules_list):
        print("Trying to import %s" % module)
        try:
            exec("import %s" %module)
            print("Success!\n")
        except ImportError:
            print("Module %s can't be imported since it doesn't exists or is not installed.\n Will be added to failed_imports" % module)
            failed_imports.append(module)

    if len(failed_imports)>0:
        existing = []
        if input("Perform search about items in failed imports?\nFailed imports:-- {0} --\n[y/n] ".format(failed_imports)) == "y":
            for item in failed_imports:
                 print("Looking for %s" % item)
                 searchfor = shell("pip{0} -q search {1}".format(pip_version, item))
                 if searchfor == 0:
                     print("Found package(s) for %s!" % item)
                     existing.append(item)
                 elif searchfor == 5888:
                     print("Search did not return any result for %s" % item)
                 elif searchfor == 512:
                     print("Network issue: pip{0} can't be contacted")

            if input("Wish to install the following required modules?\n %s\n[y/n]" % existing) == "y":
                for module in existing:
                    print("pip{0} install {1}".format(pip_version, module))
    exit()
