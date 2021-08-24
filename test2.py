import requests
import argparse


parser = argparse.ArgumentParser(description="Input country")
parser.add_argument('-c', '--country', type=str, default='all',
                    help='Country code')
args = parser.parse_args()

country = vars(args)["country"]


def main():
    base_url = "https://corona-api.com/"
    url = base_url + "timeline"
    if country and country != "all":
        url = base_url + f"countries/{country}"

    resp = requests.get(url)
    json_resp = resp.json()
    status = resp.status_code

    if status == 200:
        if country == "all":
            data = json_resp["data"][0]
            date = data["date"]
            active = data["active"]
            confirmed = data["confirmed"]
            deaths = data["deaths"]
        else:
            data = json_resp["data"]
            date = data["updated_at"].split("T")[0]
            active = data["latest_data"]["critical"]
            confirmed = data["latest_data"]["confirmed"]
            deaths = data["latest_data"]["deaths"]
        print(f"API OK - status = {status} | date = {date},active = {active},confirmed = {confirmed},deaths = {deaths}")
    else:
        print(f"API ERROR - status = {status} | message = {json_resp['message']}")
    output = f""


if __name__ == '__main__':
    main()
