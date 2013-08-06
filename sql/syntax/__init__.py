# -*- coding: utf-8 -*-
"""
    based on: http://www.andrew.cmu.edu/user/shadow/sql/sql3bnf.sep93.txt
"""

import comparator
from select import (SelectStatement, TableName, SelectList, Column,
                    SelectSubList, Asterisk)
from conditions import (SearchCondition, BooleanTerm, BooleanFactor,
                        BooleanPrimary, RowValueDesignator, Number, String)
from clauses import (WhereClause, EmptyClause, EmptyGroupbyClause,
                     GroupByClause, GroupingColumnList, HavingClause,
                     OrderByClause, SortSepcList, OrderingSpec,
                     EmptyOrderByClause)
from functions import AttributeFunction


productions = [
    ("""select_stat : SELECT select_list
                      FROM table_name 
                      where_clause
                      groupby_clause 
                      having_clause
                      orderby_clause""",
        SelectStatement),

    ("select_list : asterisk", SelectList),
    ("select_list : select_sublist", SelectList),

    ("select_sublist : column", SelectSubList),
    ("select_sublist : attribute_function", SelectSubList),
    ("select_sublist : select_sublist COMMA select_sublist", SelectSubList),

    ("asterisk : ASTERISK", Asterisk),

    # TODO: rename column -> value expression
    ("column : IDENTIFIER", Column),

    ('attribute_function : IDENTIFIER LEFT_PAREN column RIGHT_PAREN',
        AttributeFunction),

    ("table_name : IDENTIFIER", TableName),

    ("where_clause : WHERE search_condition", WhereClause),
    ("where_clause : empty_where_clause", WhereClause),
    ("empty_where_clause : ", EmptyClause),

    ("groupby_clause : GROUP BY grouping_column_list", GroupByClause),
    ("grouping_column_list : grouping_column_list COMMA column",
        GroupingColumnList),
    ("grouping_column_list : column", GroupingColumnList),
    ("groupby_clause : empty_groupby_clause", GroupByClause),
    ("empty_groupby_clause : ", EmptyGroupbyClause),

    ("having_clause : HAVING search_condition", HavingClause),
    ("having_clause : empty_having_clasue ", HavingClause),
    ("empty_having_clasue : ", EmptyClause),

    ("""orderby_clause :
        ORDER BY sort_specification_list""", OrderByClause),
    ("orderby_clause : empty_orderby_clasue ", OrderByClause),
    ("empty_orderby_clasue : ", EmptyOrderByClause),
    ("sort_specification_list : ordering_specification", SortSepcList),
    ("""sort_specification_list :
        sort_specification_list COMMA ordering_specification""", SortSepcList),
    ("ordering_specification : column", OrderingSpec),
    ("ordering_specification : column ASC", OrderingSpec),
    ("ordering_specification : column DESC", OrderingSpec),

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
