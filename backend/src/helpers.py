import pkgutil


def load_modules(package_path, from_module=None):
    modules = [name for _, name, _ in pkgutil.iter_modules([package_path])]
    for mod in modules:
        list_ = [from_module] if from_module is not None else None
        full_module_name = "{}.{}".format(from_module, mod)
        __import__(full_module_name, fromlist=list_)


from app import app

@app.get('/fuck-the-world')
def mySuperRoute():
    pass