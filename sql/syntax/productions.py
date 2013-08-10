# -*- coding: utf-8 -*-
"""
    based on: http://www.andrew.cmu.edu/user/shadow/sql/sql3bnf.sep93.txt
"""

from inspect import isclass
from comparator import *
from select import *
from conditions import *
from clauses import *
from functions import *


select_bnf = """
    select_statement: SELECT select_list FROM table_name
        [ where_clause ]
        [ group_by_clause ] [ having_clause ]
        [ order_by_clause ] [ limit_clause ];

    select_list: asterisk | select_sublist;

    select_sublist: column 
        | attribute_function
        | select_sublist COMMA select_sublist;

    asterisk: ASTERISK;

    column: IDENTIFIER;

    table_name: IDENTIFIER;

    attribute_function: IDENTIFIER LEFT_PAREN column RIGHT_PAREN;

    where_clause: WHERE search_condition;

    group_by_clause: GROUP BY grouping_column_list;
    grouping_column_list: column | grouping_column_list COMMA column;

    having_clause: HAVING search_condition;

    order_by_clause: ORDER BY sort_spec_list;

    sort_spec_list: ordering_spec 
        { COMMA ordering_spec };
    ordering_spec: column | column ASC | column DESC;

    limit_clause: LIMIT NUMBER;


    search_condition: boolean_value_expr;

    boolean_value_expr: boolean_term { OR boolean_term };

    boolean_term: boolean_factor { AND boolean_factor };

    boolean_factor: [ NOT ] boolean_primary;

    boolean_primary: predicate;
    
    predicate: comparison_predicate | in_predicate;

    in_predicate: row_value_designator [ NOT ] IN in_predicate_value;

    in_predicate_value: LEFT_PAREN in_value_list RIGHT_PAREN;

    in_value_list: value_expr { COMMA value_expr };

    comparison_predicate: row_value_designator comparator row_value_designator;

    row_value_designator: value_expr;

    value_expr: STRING | NUMBER | IDENTIFIER;

    comparator: EQUAL | LESS_THAN | LESS_THAN_OR_EQUAL
              | GREATER_THAN | GREATER_THAN_OR_EQUAL | LIKE;
"""

# TODO
    #row_value_designator: value_expr
                        #| LEFT_PAREN row_value_designator_list RIGHT_PAREN;

    #row_value_designator_list: value_expr { COMMA value_expr};
    

node_classes = {x.__name__: x
                for x in locals().values() if (isclass(x)
                                               and issubclass(x, Node))}
