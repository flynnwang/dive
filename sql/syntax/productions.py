# -*- coding: utf-8 -*-
"""
    based on: http://www.andrew.cmu.edu/user/shadow/sql/sql3bnf.sep93.txt
"""

from comparator import Comparator
from select import (SelectStatement, TableName, SelectList, Column,
                    SelectSubList, Asterisk)
from conditions import (SearchCondition, BooleanTerm, BooleanFactor,
                        BooleanPrimary, RowValueDesignator)
from clauses import (WhereClause, EmptyGroupbyClause,
                     GroupByClause, GroupingColumnList, HavingClause,
                     OrderByClause, SortSepcList, OrderingSpec,
                     EmptyOrderByClause, LimitClause)
from functions import AttributeFunction


productions = [
    ("""select_stat : SELECT select_list
                      FROM table_name where_clause
                      groupby_clause having_clause
                      orderby_clause
                      limit_clause""",
        SelectStatement),

    ("select_list : asterisk | select_sublist", SelectList),
    ("""select_sublist : column 
                       | attribute_function 
                       | select_sublist COMMA select_sublist""",
        SelectSubList),

    ("asterisk : ASTERISK", Asterisk),
    # TODO: rename column -> value expression
    ("column : IDENTIFIER", Column),
    ("table_name : IDENTIFIER", TableName),
    ('attribute_function : IDENTIFIER LEFT_PAREN column RIGHT_PAREN',
        AttributeFunction),

    ("where_clause : WHERE search_condition | ", WhereClause),

    ("""groupby_clause : GROUP BY grouping_column_list
                       | empty_groupby_clause""", GroupByClause),
    ("""grouping_column_list : column
                             | grouping_column_list COMMA column""",
        GroupingColumnList),
    ("empty_groupby_clause : ", EmptyGroupbyClause),

    ("having_clause : HAVING search_condition | ", HavingClause),

    ("""orderby_clause : ORDER BY sort_specification_list
                       | empty_orderby_clasue """, OrderByClause),
    ("empty_orderby_clasue : ", EmptyOrderByClause),
    ("""sort_specification_list : ordering_specification
                     | sort_specification_list COMMA ordering_specification""",
        SortSepcList),
    ("""ordering_specification : column
                               | column ASC
                               | column DESC""", OrderingSpec),

    ("limit_clause : LIMIT NUMBER | ", LimitClause),

    ("""search_condition : boolean_term
                         | search_condition OR boolean_term""",
        SearchCondition),
    ("""boolean_term : boolean_factor
                     | boolean_term AND boolean_factor""", BooleanTerm),
    ("""boolean_factor : boolean_primary
                       | NOT boolean_primary""", BooleanFactor),
    ("boolean_primary : row_value_designator comp_op row_value_designator",
        BooleanPrimary),

    ("""row_value_designator : STRING 
                             | NUMBER 
                             | IDENTIFIER""",
        RowValueDesignator),

    ("""comp_op : EQUAL 
                | LESS_THAN | LESS_THAN_OR_EQUAL
                | GREATER_THAN | GREATER_THAN_OR_EQUAL
                | LIKE""", 
        Comparator),
]
