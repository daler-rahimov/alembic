import re

from sqlalchemy import schema
from sqlalchemy import types as sqltypes
# from sqlalchemy.ext.compiler import compiles
from sqlalchemy.ext.compiler import compiles

from .base import AddColumn
from .base import format_table_name

from .base import alter_table
from .base import AlterColumn
from .base import ColumnDefault
from .base import ColumnName
from .base import ColumnNullable
from .base import ColumnType
from .base import format_column_name
from .base import format_server_default
from .impl import DefaultImpl
from .. import util
from ..autogenerate import compare
from ..util.compat import string_types
from ..util.sqla_compat import _is_type_bound
from ..util.sqla_compat import sqla_100
from sqlalchemy import types as sqltypes
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import Column
from sqlalchemy.schema import CreateIndex
from sqlalchemy.sql.expression import ClauseElement
from sqlalchemy.sql.expression import Executable

from .base import AddColumn
from .base import alter_column
from .base import alter_table
from .base import ColumnDefault
from .base import ColumnName
from .base import ColumnNullable
from .base import ColumnType
from .base import format_column_name
from .base import format_server_default
from .base import format_table_name
from .base import format_type
from .base import RenameTable
from .impl import DefaultImpl
from .. import util

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

def informix_add_column(compiler, column, **kw):
    return "ADD %s" % compiler.get_column_specification(column, **kw)


def alter_table(compiler, name, schema):
    return "ALTER TABLE %s" % format_table_name(compiler, name, schema)


@compiles(ColumnType, "informix")
def visit_column_type(element, compiler, **kw):
    return "%s %s %s" % (
        alter_table(compiler, element.table_name, element.schema),
        alter_column(compiler, element.column_name),
        format_type(compiler, element.type_),
    )