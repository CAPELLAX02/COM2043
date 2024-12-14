%{
#include <stdio.h>
#include <stdlib.h>

int yylex(void);
int yyerror(char *s) {
   fprintf(stderr, "syntax error\n");
   return 0;
}
%}

%token TBEGIN TEND IF ELSE WHILE INT FLOAT CHAR
%token IDENT NUMBER
%token ASSIGN PLUS MINUS MUL DIV
%token EQ NEQ LT GT LE GE AND OR
%token LPAREN RPAREN COLON SEMI

%left OR
%left AND
%nonassoc EQ NEQ LT GT LE GE
%left PLUS MINUS
%left MUL DIV

%%
program:
    TBEGIN declarations statements TEND { printf("OK\n"); }
    ;

declarations:
    declarations declaration
    | /* empty */
    ;

declaration:
    type COLON varlist SEMI
    ;

type:
    INT
    | FLOAT
    | CHAR
    ;

varlist:
    varlist IDENT
    | IDENT
    ;

statements:
    statements statement
    | /* empty */
    ;

statement:
    declaration
    | assignment
    | if_statement
    | while_statement
    ;

assignment:
    IDENT ASSIGN expr SEMI
    ;

if_statement:
    IF LPAREN bool_expr RPAREN TBEGIN statements TEND
    | IF LPAREN bool_expr RPAREN TBEGIN statements TEND ELSE TBEGIN statements TEND
    ;

while_statement:
    WHILE LPAREN bool_expr RPAREN TBEGIN statements TEND
    ;

expr:
    expr PLUS term
    | expr MINUS term
    | term
    ;

term:
    term MUL factor
    | term DIV factor
    | factor
    ;

factor:
    LPAREN expr RPAREN
    | IDENT
    | NUMBER
    ;

bool_expr:
    bool_expr OR bool_term
    | bool_expr AND bool_term
    | bool_term
    ;

bool_term:
    LPAREN bool_expr RPAREN
    | expr relop expr
    ;

relop:
    EQ
    | NEQ
    | LT
    | GT
    | LE
    | GE
    ;

%%
#include "lex.yy.c"
int main() {
    return yyparse();
}
