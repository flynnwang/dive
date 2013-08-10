# -*- coding: utf-8 -*-
"""
    based on: http://www.andrew.cmu.edu/user/shadow/sql/sql3bnf.sep93.txt
"""

from inspect import isclass
from node import Node
from comparator import Comparator
from select import (SelectStatement, TableName, SelectList, Column,
                    SelectSublist, Asterisk)
from conditions import (SearchCondition, BooleanTerm, BooleanFactor,
                        BooleanPrimary, RowValueDesignator)
from clauses import (WhereClause, EmptyGroupbyClause,
                     GroupByClause, GroupingColumnList, HavingClause,
                     OrderByClause, SortSpecList, OrderingSpec,
                     EmptyOrderByClause, LimitClause)
from functions import AttributeFunction


select_bnf = """
    select_statement : SELECT select_list FROM table_name
        [where_clause]
        [group_by_clause] [having_clause]
        [order_by_clause] [limit_clause];

    select_list : asterisk | select_sublist;

    select_sublist : column 
        | attribute_function
        | select_sublist COMMA select_sublist;

    asterisk : ASTERISK;

    column : IDENTIFIER;

    table_name : IDENTIFIER;

    attribute_function : IDENTIFIER LEFT_PAREN column RIGHT_PAREN;

    where_clause : WHERE search_condition;
    search_condition : boolean_term {OR boolean_term};
    boolean_term : boolean_factor {AND boolean_factor};
    boolean_factor : [NOT] boolean_primary;

    group_by_clause : GROUP BY grouping_column_list;
    grouping_column_list : column | grouping_column_list COMMA column;

    having_clause : HAVING search_condition;

    order_by_clause : ORDER BY sort_spec_list;

    sort_spec_list : ordering_spec 
        { COMMA ordering_spec };
    ordering_spec : column | column ASC | column DESC;

    limit_clause : LIMIT NUMBER;

    boolean_primary : row_value_designator comparator row_value_designator;
    row_value_designator : STRING | NUMBER | IDENTIFIER;
    comparator : EQUAL | LESS_THAN | LESS_THAN_OR_EQUAL 
            | GREATER_THAN | GREATER_THAN_OR_EQUAL | LIKE;
"""


node_classes = {x.__name__: x
                for x in locals().values() if (isclass(x) 
                                               and issubclass(x, Node))}
