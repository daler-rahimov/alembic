from sqlalchemy.ext.compiler import compiles
from .base import AddColumn
from .base import ColumnDefault
from .base import alter_column
from .base import alter_table
from .base import ColumnType
from .base import format_table_name
from .base import format_type
from .impl import DefaultImpl


class InformixSQLImpl(DefaultImpl):
    __dialect__ = "informix"

    transactional_ddl = False

    def create_index(self, index):
        # this likely defaults to None if not present, so get()
        # should normally not return the default value.  being
        # defensive in any case
        pass


@compiles(AddColumn, "informix")
def visit_add_column(element, compiler, **kw):
    return "%s %s" % (
        alter_table(compiler, element.table_name, element.schema),
        informix_add_column(compiler, element.column, **kw),
    )

@compiles(ColumnType, "informix")
def visit_column_type(element, compiler, **kw):
    return "%s %s %s" % (
        alter_table(compiler, element.table_name, element.schema),
        alter_column(compiler, element.column_name),
        element.type_,
    )


@compiles(ColumnDefault, "informix")
def visit_column_default(element, compiler, **kw):
    return "%s ADD %s NOT NULL DEFAULT %S" % (
        alter_table(compiler, element.table_name, element.schema),
        element.column_name,
        informix_add_column(compiler, element.column, **kw),
    )


def informix_add_column(compiler, column, **kw):
    return "ADD %s" % compiler.get_column_specification(column, **kw)


def alter_table(compiler, name, schema):
    return "ALTER TABLE %s" % format_table_name(compiler, name, schema)


