import glob
from os.path import basename, dirname, isfile
from TeleBot import MOD_LOAD, LOG, MOD_NOLOAD


def list_all_modules():
    module_paths = glob.glob(dirname(__file__) + "/*.py")
    all_modules = [
        basename(f)[:-3]
        for f in module_paths
        if isfile(f) and f.endswith(".py") and not f.endswith('__init__.py')
    ]

    if MOD_LOAD or MOD_NOLOAD:
        to_load = MOD_LOAD 
        all_modules = sorted(set(all_modules) - set(to_load))
        to_load.extend(all_modules)

        if MOD_NOLOAD:
            LOG.print(f"[bold yellow]ɴᴏᴛ ʟᴏᴀᴅɪɴɢ: {MOD_NOLOAD}")
            return [item for item in to_load if item not in MOD_NOLOAD]

        return to_load

    return all_modules


ALL_MODULES = list_all_modules()
LOG.print(f"[bold yellow]ᴍᴏᴅᴜʟᴇꜱ ᴛᴏ ʟᴏᴀᴅ: {str(ALL_MODULES)}")
__all__ = ALL_MODULES + ["ALL_MODULES"]
