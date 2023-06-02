from Program import Program


def main():
    regex = r'\s*(\[.*\]|".*"|[A-Za-z0-9\.]+|.?)'
    text = """   
        
            main {
  set arr = [2, 3, 4]
  print arr
  set y = 1
  set x = 0
  set z = 0
  set counter = 1

  while y LEQ 10 then
      if y % 2 EQ 0 AND x GEQ 0 then
          print "Entro nell if"
          for set i in range (1, 5) then
              print "FOR: i = " + i
          endfor
          print "X vale " + x
      elseif 1 EQ 1 then
          print "Entro nell ELSEIF"
          while counter LT 5 then
              print "WHILE: counter = " + counter
              set z = z + counter
              set counter = counter + 1
          endwhile
          set counter = 1
          print "Z vale " + z
      else
          set counter = counter
      endif
      set y = y + 1
  endwhile
}
          }
    """
    prog = Program(text, regex)
    res = prog.mainBlock()
    print(prog.values())
    if res:
        print("")
    else:
        print("")


if __name__ == '__main__':
    main()
