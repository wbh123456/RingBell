import matchAndSend
import form_extraction

def main():
    form_extraction.extract(is_listener = False)
    form_extraction.organize_form()
    matchAndSend.matchAndSend()

if __name__ == '__main__':
    main()