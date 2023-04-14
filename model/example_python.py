import base64

import requests


def main():
    with open("monke.jpg", "rb") as f:
        base64_message = base64.b64encode(f.read()).decode('utf-8')

    response = requests.post(
        url="http://91.77.160.33:5000/predictions",
        json={"input": {"image": f"data:image/png;base64,{base64_message}"}}
    ).json()

    print(response)
    print(response["output"])

    response = requests.post(
        url="http://91.77.160.33:5000/predictions",
        json={
            "input": {
                "image": "https://play-lh.googleusercontent.com/T_vA5l9W1-XYTmgr3gCB2MBd7QmA-iG0wcm09_IFWNB-4gOpnS"
                         "-tYNEmcalwdixSyw"
            }
        }
    ).json()

    print(response)
    print(response["output"])


if __name__ == "__main__":
    main()
