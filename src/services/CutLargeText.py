def cutLargeText(text):
        TEXT_MEDIUM_LENGTH = 40
        TEXT_HIGH_LENGTH = 80
        textLength = len(text)
        if textLength < TEXT_MEDIUM_LENGTH:
            return text
        if textLength >= TEXT_MEDIUM_LENGTH and textLength < TEXT_HIGH_LENGTH:
            firstHalf = text[:textLength//2]
            secondHalf = text[textLength//2:]
            firstHalf += '-\n'
            return firstHalf + secondHalf
        return "Too large text"