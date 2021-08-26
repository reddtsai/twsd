from twse import twt49u


def main():
    service = twt49u.TWT49_Service()
    service.get("2021", "1", "1", "2021", "8", "23")

if __name__ == '__main__':
    print("==================== main ====================")
    main()
    print("==================== main ====================")