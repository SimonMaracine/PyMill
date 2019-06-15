import pygame

pygame.scrap.init()


def get_clipboard() -> str:
    """Gets text from the clipboard if there is any.

    Returns:
        str: The text found.

    """
    text = ""
    types = pygame.scrap.get_types()
    print(types)
    for t in types:
        if "text" in t:
            clipboard: bytes = pygame.scrap.get(pygame.SCRAP_TEXT)
            try:
                text = clipboard.decode()
                print(str(text))
            except UnicodeDecodeError:
                print("Clipboard could not be decoded")
            break
    else:
        print("Clipboard doesn't contain text")
    return text
