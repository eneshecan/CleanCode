import clang.cindex

clang.cindex.Config.set_library_path('/usr/lib/llvm-3.5/lib/')


class custom_text:
    def __init__(self):
        self.HEADER    = '\033[95m'
        self.OKBLUE    = '\033[94m'
        self.OKGREEN   = '\033[92m'
        self.WARNING   = '\033[93m'
        self.FAIL      = '\033[91m'
        self.ENDC      = '\033[0m'
        self.BOLD      = '\033[1m'
        self.UNDERLINE = '\033[4m'

    def underlined(self, message):
        return self.UNDERLINE + message + self.ENDC

    def useful_link(self, message):
        return self.OKBLUE + "Useful Link: " + self.ENDC + message + '\n'

    def useful_doc(self, message):
        return self.OKBLUE + "Useful Document: " + self.ENDC + message + '\n'

    def warning(self):
        return self.WARNING + "WARNING: " + self.ENDC

    def comment(self, message):
        return self.OKGREEN + message + self.ENDC


custom_text_ = custom_text()
is_var_init = False


def is_var_initialized(cursor):
    for c in cursor.get_children():
        if "LITERAL" in str(c.kind) or c.kind == clang.cindex.CursorKind.DECL_REF_EXPR:
            global is_var_init
            is_var_init = True

        is_var_initialized(c)


def inspect_variable(cursor):
    global is_var_init
    is_var_init = False

    is_var_initialized(cursor)

    if not is_var_init:
        print custom_text_.warning() + "Uninitialized variable " + custom_text_.underlined(cursor.spelling) + " at line " + \
              str(cursor.location.line) + " column " + str(cursor.location.column)

    if 'unsigned' in cursor.type.get_canonical().spelling:
        print custom_text_.warning() + "Unsigned data type can introduce bugs, try to aviod if possible, " + \
              custom_text_.underlined(cursor.spelling) + " at line " + \
              str(cursor.location.line) + " column " + str(cursor.location.column) + ".\n" +\
              custom_text_.useful_link("https://google.github.io/styleguide/cppguide.html, On Unsigned Integers")


def inspect_func(cursor):
    if (cursor.extent.end.line - cursor.extent.start.line) > 7:
        print custom_text_.warning() + "Function " + custom_text_.underlined(cursor.spelling) + \
              " is too long. It is better to extract functions from it." + "\n" + \
              custom_text_.useful_doc("Robert C. Martin, Clean Code, Chapter 3:Functions")


# Only works for functions now
def inspect_comp_stmt(cursor):
    parent = cursor.semantic_parent
    if parent:
        if parent.location.line == cursor.location.line:
            print custom_text_.warning() + "You may leave braces which start at line " + str(cursor.location.line) + \
                  " on their own in a line to indicate them as a sign of scope."


def inspect_using_directive(cursor):
    namespace_ref = cursor.get_children().next()
    print custom_text_.warning() + "Avoid " + custom_text_.underlined("using") + " directives to prevent confusions, instead try to use " + \
          custom_text_.underlined(str(namespace_ref.displayname) + "::<member>")


def inspect_comment(cursor):
    print custom_text_.warning() + "You may try to remove the comment " + custom_text_.comment(cursor.raw_comment) + \
          " and embed into the name " + custom_text_.underlined(cursor.spelling) + "\n" + \
          " at line " + str(cursor.location.line) + " column " + str(cursor.location.column) +  \
          ", so that the reader will be able to infer its meaning by just reading it.\n" + \
          custom_text_.useful_doc("Robert C. Martin, Clean Code, Chapter 2: Meaningful Names")
