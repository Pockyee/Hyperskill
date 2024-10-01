formatters = ["plain", "bold", "italic", "header", "link", "inline-code", "new-line"]

def plain(content):
 return content

def bold(content):
 return "**" + content + "**"

def italic(content):
 return "*" + content + "*"

def inline_code(content):
 return "`" + content + "`"

def link(label, url):
 return "[" + label + "]" + "(" + url + ")"

def header(content, level):
 return "#" * int(level) + " " + content + "\n"

def new_line():
 return "\n"

form = ""
text = ""
while True:
 form = input("Choose a formatter:")
 if form == "plain":
  text += plain(input("Text:"))
  print(text)
  pass
 elif form == "bold":
  text += bold(input("Text:"))
  print(text)
  pass
 elif form == "italic":
  text += italic(input("Text:"))
  print(text)
  pass
 elif form == "inline-code":
  text += inline_code(input("Text:"))
  print(text)
  pass
 elif form == "link":
  label = input("Label:")
  url = input("URL:")
  text += link(label, url)
  print(text)
  pass
 elif form == "header":
  while True:
   level = input("Level:")
   if 1 <= int(level) <= 6:
    break
   else:
    print("The level should be within the range of 1 to 6")
  content = input("Text:")
  text += header(content, level)
  print(text)
  pass
 elif form == "new-line":
  text += new_line()
  print(text)
  pass
 elif form == "!help":
  print("""Available formatters: plain bold italic header link inline-code new-line\nSpecial commands: !done""")
 elif form == "!done":
  break
 else:
  print("Unknown formatting type or command")


