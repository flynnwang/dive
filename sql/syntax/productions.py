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


    select_list: asterisk | select_sublist;

    select_sublist: derived_column | select_sublist COMMA derived_column;
    
    derived_column: value_expr;


    outfile_clause: INTO OUTFILE string;


    group_by_clause: GROUP BY grouping_column_list;

    grouping_column_list: column | grouping_column_list COMMA column;


    order_by_clause: ORDER BY sort_spec_list;

    sort_spec_list: ordering_spec | sort_spec_list COMMA ordering_spec;

    ordering_spec: column | column ASC | column DESC;


    where_clause: WHERE search_condition;

    having_clause: HAVING search_condition;

    search_condition: boolean_value_expr;


    limit_clause: LIMIT NUMBER;


    boolean_value_expr: boolean_term | boolean_value_expr OR boolean_term;

    boolean_term: boolean_factor | boolean_term AND boolean_factor;

    boolean_factor: [ NOT ] boolean_primary;

    boolean_primary: predicate | value_expr_primary;


    predicate: comparison_predicate
             | in_predicate
             | like_predicate;

    like_predicate: column [ NOT ] LIKE value_expr;

    in_predicate: column [ NOT ] IN in_predicate_value;

    in_predicate_value: LEFT_PAREN in_value_list RIGHT_PAREN;

    in_value_list: value_expr | in_value_list  COMMA value_expr;

    comparison_predicate: value_expr comparator value_expr;


    value_expr_primary: LEFT_PAREN boolean_value_expr RIGHT_PAREN;


    attribute_function: IDENTIFIER LEFT_PAREN function_argument RIGHT_PAREN;

    function_argument: column | asterisk;


    value_expr: string
              | number 
              | column
              | attribute_function;

    comparator: EQUAL | LESS_THAN | LESS_THAN_OR_EQUAL
              | GREATER_THAN | GREATER_THAN_OR_EQUAL;

    asterisk: ASTERISK;

    string: STRING;

    number: NUMBER; 

    column: IDENTIFIER;

    table_name: IDENTIFIER;
"""


node_classes = {x.__name__: x
                for x in locals().values() if (isclass(x)
                                               and issubclass(x, Node))}
