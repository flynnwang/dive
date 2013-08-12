# -*- coding: utf-8 -*-
"""
    based on:

    http://www.andrew.cmu.edu/user/shadow/sql/sql3bnf.sep93.txt
    http://www.antlr3.org/grammar/1347528470063/MySQL.g
"""

from inspect import isclass
from comparator import *
from select import *
from conditions import *
from clauses import *
from functions import *
from predicate import *
from datamodel import *

select_bnf = """
    select_expr: SELECT select_list [outfile_clause] FROM table_name
        [ where_clause ]
        [ group_by_clause ] [ having_clause ]
        [ order_by_clause ] [ limit_clause ];


    outfile_clause: INTO OUTFILE string;


    select_list: asterisk | select_sublist;

    select_sublist: column | attribute_function
                  | select_sublist COMMA select_sublist;


    group_by_clause: GROUP BY grouping_column_list;

    grouping_column_list: column { COMMA column };


    order_by_clause: ORDER BY sort_spec_list;

    sort_spec_list: ordering_spec { COMMA ordering_spec };

    ordering_spec: column | column ASC | column DESC;


    where_clause: WHERE search_condition;

    having_clause: HAVING search_condition;

    search_condition: boolean_value_expr;


    limit_clause: LIMIT NUMBER;


    boolean_value_expr: boolean_term { OR boolean_term };

    boolean_term: boolean_factor { AND boolean_factor };

    boolean_factor: [ NOT ] boolean_primary;

    boolean_primary: predicate | value_expr_primary;

    value_expr_primary: LEFT_PAREN boolean_value_expr RIGHT_PAREN;
    

    predicate: comparison_predicate
             | in_predicate
             | like_predicate;

    like_predicate: column [ NOT ] LIKE value_expr;


    in_predicate: column [ NOT ] IN in_predicate_value;

    in_predicate_value: LEFT_PAREN in_value_list RIGHT_PAREN;

    in_value_list: value_expr { COMMA value_expr };


    comparison_predicate: row_value_designator comparator row_value_designator;


    asterisk: ASTERISK;

    column: IDENTIFIER;

    table_name: IDENTIFIER;

    attribute_function: IDENTIFIER LEFT_PAREN column RIGHT_PAREN;

    row_value_designator: value_expr;

    value_expr: STRING | NUMBER | IDENTIFIER;

    comparator: EQUAL | LESS_THAN | LESS_THAN_OR_EQUAL
              | GREATER_THAN | GREATER_THAN_OR_EQUAL;

    string: STRING;
"""
    

node_classes = {x.__name__: x
                for x in locals().values() if (isclass(x)
                                               and issubclass(x, Node))}
