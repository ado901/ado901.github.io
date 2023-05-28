from Program import Program


def main():
    regex = r'\s*(\[.*\]|".*"|[A-Za-z0-9\.]+|.?)'
    text = """   
        
            main {
              set arr = [1,2,3,4,5]
              print arr
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
