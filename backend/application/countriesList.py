## Countries supporrted by news api.
## recommendation - regional headlines for users

names_string = "aearataubebgbrcachcncocuczdeegfrgbgrhkhuidieilinitjpkrltlvmamxmyngnlnonzphplptrorsrusasesgsiskthtrtwuausveza"

countries = [] 
[countries.append((names_string[i].upper()+names_string[i+1].upper())) for i in range(0,len(names_string),2)]
print(countries)