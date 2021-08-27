from twse import twt49u


def main():
    service = twt49u.TWT49_Service()
    service.get("2003", "5", "5", "2021", "8", "27")

if __name__ == '__main__':
    print("==================== main ====================")
    main()
    print("==================== main ====================")