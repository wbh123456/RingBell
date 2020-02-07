import matchAndSend
import form_extraction
import config
import sys

def main():
    config.config(sys.argv)
    form_extraction.extract(is_listener = False)
    form_extraction.organize_form()
    matchAndSend.matchAndSend()

if __name__ == '__main__':
    main()