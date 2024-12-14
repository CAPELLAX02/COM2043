%{
#include <stdio.h>
#include <stdlib.h>
%}

%%

"begin"         { return TBEGIN; }
"end"           { return TEND; }
"if"            { return IF; }
"else"          { return ELSE; }
"while"         { return WHILE; }

"int"           { return INT; }
"float"         { return FLOAT; }
"char"          { return CHAR; }

"=="            { return EQ; }
"!="            { return NEQ; }
"<="            { return LE; }
">="            { return GE; }
"<"             { return LT; }
">"             { return GT; }
"&&"            { return AND; }
"||"            { return OR; }

":"             { return COLON; }
";"             { return SEMI; }
"("             { return LPAREN; }
")"             { return RPAREN; }
"="             { return ASSIGN; }

"+"             { return PLUS; }
"-"             { return MINUS; }
"*"             { return MUL; }
"/"             { return DIV; }

[0-9]+          { return NUMBER; }
[A-Za-z][A-Za-z0-9]* { return IDENT; }

[ \t\n\r]+      { /* boşlukları yoksay */ }

.               { return yytext[0]; }

%%

int yywrap() { return 1; }
