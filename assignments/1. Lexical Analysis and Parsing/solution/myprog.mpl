begin
int: a b c;
float: x y;
char: ch;

a = 5;
b = a + 3;

if (a > 0) begin
  x = b * 2;
end else begin
  ch = 97;
end

while (x < 100) begin
  x = x + 10;
end
end
