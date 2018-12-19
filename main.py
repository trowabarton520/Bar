import time
import Bar_Passed


def main():
    x = True
    count = 0
    while x:
        Bar_Passed.main()
        count += 1
        print(count)
        time.sleep(60)


if __name__ == '__main__':
    main()
