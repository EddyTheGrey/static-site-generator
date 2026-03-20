import textnode
def main():
    obj =textnode.TextNode("This is some anchor text", textnode.TextType.LINK, "https://www.boot.dev")
    print('TextNode('+str(obj)+')')

if __name__ == "__main__":
    main()