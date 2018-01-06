#!/usr/bin/python

import sys
import clang.enumerations
import clang.cindex
from analyzer import *

clang.cindex.Config.set_library_path('/usr/lib/llvm-4.0/lib')

log_file = None

class Level(int):
    '''Represents currently visited level of the tree'''

    def show(self, *args):
        log_file.write('\t' * self + ' '.join(map(str, args)) + '\n')

    def __add__(self, inc):
        return Level(super(Level, self).__add__(inc))


def is_valid_type(t):
    return t.kind != clang.cindex.TypeKind.INVALID


def qualifiers(t):
    q = set()
    if t.is_const_qualified(): q.add('const')
    if t.is_volatile_qualified(): q.add('volatile')
    if t.is_restrict_qualified(): q.add('restrict')
    return q


def show_type(t, level, title):
    level.show(title, str(t.kind), ' '.join(qualifiers(t)))
    if is_valid_type(t.get_pointee()):
        show_type(t.get_pointee(), level + 1, 'points to:')


def show_ast(cursor, level=Level()):
    if '/usr/' not in str(cursor.location.file):

        level.show(cursor.kind, cursor.spelling, cursor.displayname, cursor.location)

        if cursor.kind == clang.cindex.CursorKind.VAR_DECL:
            inspect_variable(cursor)

        elif cursor.kind == clang.cindex.CursorKind.FUNCTION_DECL:
            inspect_func(cursor)

        elif cursor.kind == clang.cindex.CursorKind.COMPOUND_STMT:
            inspect_comp_stmt(cursor)

        elif cursor.kind == clang.cindex.CursorKind.USING_DIRECTIVE:
            inspect_using_directive(cursor)

        if cursor.raw_comment:
            inspect_comment(cursor)

        if is_valid_type(cursor.type):
            show_type(cursor.type, level + 1, 'type:')
            show_type(cursor.type.get_canonical(), level + 1, 'canonical type:')
        for c in cursor.get_children():
            show_ast(c, level + 1)


def check_args(argv):
    if len(argv) == 2:
        if not (sys.argv[1].split('.')[1] == 'cpp' or sys.argv[1].split('.')[1] == 'h'):
            print "Please provide a C++ source code or header as argument"
            exit()
        return sys.argv[1]
    elif len(argv) < 2:
        print "Provide a C++ source code or header as argument"
        exit()
    else:
        print "Too much arguments!"
        exit()


if __name__ == '__main__':
    filename = check_args(sys.argv)

    log_file = open(filename + '.log', 'w')

    index = clang.cindex.Index.create()
    tu = index.parse(filename)

    log_file.write('Translation unit: ' + tu.spelling + '\n\n')

    # for f in tu.get_includes():
    #    log_file.write('\t' * f.depth + f.include.name + '\n')

    show_ast(tu.cursor)

    log_file.close()
