from .subtitlefile import SubtitleFile

def main():
    while True:
        result = input(">")

        if result == "q":
            break

        file = SubtitleFile(result)

        print(f"Found {len(file.subtitles)} subtitles")

        for sub in file.subtitles:
            print(sub)


if __name__ == "__main__":
    main()