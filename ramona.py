import cmd
from ramona.model import Model
from ramona.library import Library


class RamonaShell(cmd.Cmd):
    curr_options = []
    model = Model()
    library = Library()
    prompt = "ramona > "
    ERR = "*** ERROR:"

    def on_err(self, errstr):
        print(f"{self.ERR} {errstr}")

    def do_dir(self, dir):
        'add a directory of files to the library'
        try:
            self.library.pushdir(dir)
        except:
            self.on_err(f"dir: exeception for '{dir}'")
        self.do_lib(None)

    def do_talk(self, arg):
        'generate a sentence using the current model'
        if self.model is None or self.model.states is None:
            print("model not ready.  try 'load' command.")
            return
        print(' '.join(self.model.generate()))

    def do_set(self, arg):
        'toggle selections from the library'
        for a in arg.split():
            if a == '*':
                self.library.set_all_checked(True)
                break
            elif a == '/':
                self.library.set_all_checked(False)
                break
            elif a.startswith('~'):
                self.library.check_by_re(a[1:])
            if a.isdigit():
                self.library.toggle(int(a))
        self.do_lib(None)

    def do_lib(self, arg):
        'list the contents of the library'
        print("\n".join(self.library.list()))

    def do_load(self, arg):
        'load/unload the checked files.  loaded+checked means unload, unloaded+checked means load'
        # if any file is loaded and checked, we need to unload that file
        # which is impossible to do, so we need to reset and then reload all
        reload = any((f['loaded'] and f['checked']) for f in self.library.files)
        if reload:
            self.model.reset()
            for f in self.library.files:
                if f['loaded']:
                    # reload so:
                    # loaded and checked become unloaded and unchecked (so will not load)
                    # loaded and unchecked becomes unloaded and checked (so will reload)
                    f['checked'] = not f['checked']
                f['loaded'] = False
        recalculate = False
        for f in self.library.files:
            if f['checked'] and not f['loaded']:
                print(f"loading {f['path']}")
                ff = open(f['path'])
                self.model.add_text(ff.read())
                f['loaded'] = True
                recalculate = True
        if recalculate:
            print(f"recalculating...")
            self.model.recalculate()
            print(f"Done.")
        self.library.set_all_checked(False)
        self.do_lib(None)

    def do_reset(self, arg):
        'reset the library and the model to empty'
        self.library.reset()
        self.model.reset()

    def do_quit(self, arg):
        'quit the program'
        exit(0)

if __name__ == '__main__':
    shell = RamonaShell()
    shell.do_dir('./data')
    shell.cmdloop()
