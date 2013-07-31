# -*- coding: utf-8 -*-
"""
    based on: http://www.andrew.cmu.edu/user/shadow/sql/sql3bnf.sep93.txt
"""

from select import SelectCore, TableExpr, TableName
from columns import ResultColumnGroup, ResultColumn
import comparator
from conditions import (SearchCondition, BooleanTerm, BooleanFactor,
                        BooleanPrimary, RowValueDesignator, Number, String)
from where import WhereClause, EmptyClause


productions = [
    ("select_core : SELECT result_columns table_expr", SelectCore),

    ("result_columns : result_column", ResultColumnGroup),
    ("result_columns : result_columns COMMA result_column", ResultColumnGroup),
    ("result_column : IDENTIFIER", ResultColumn),

    ("table_expr : FROM table_name where_clause", TableExpr),
    ("table_name : IDENTIFIER", TableName),

    ("where_clause : WHERE search_condition", WhereClause),
    ("where_clause : empty_where_clause", WhereClause),
    ("empty_where_clause : ", EmptyClause),

    ("search_condition : boolean_term", SearchCondition),
    ("search_condition : search_condition OR boolean_term", SearchCondition),
    ("boolean_term : boolean_factor", BooleanTerm),
    ("boolean_term : boolean_term AND boolean_factor", BooleanTerm),
    ("boolean_factor : boolean_primary", BooleanFactor),
    ("boolean_factor : NOT boolean_primary", BooleanFactor),
    ("boolean_primary : row_value_designator comp_op row_value_designator",
        BooleanPrimary),

    ("row_value_designator : IDENTIFIER", RowValueDesignator),
    ("row_value_designator : NUMBER", Number),
    ("row_value_designator : STRING", String),

    ("comp_op : EQUAL", comparator.Equal),
    ("comp_op : LESS_THAN", comparator.LessThan),
    ("comp_op : LESS_THAN_OR_EQUAL", comparator.LessThanOrEqual),
    ("comp_op : GREATER_THAN", comparator.GreaterThan),
    ("comp_op : GREATER_THAN_OR_EQUAL", comparator.GreaterThanOrEqual),
    ("comp_op : LIKE", comparator.LikeComparator),

]
