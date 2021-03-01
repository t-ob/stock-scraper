import logging

import time

import requests

import twilio.rest

# import winsound


# https://www.twilio.com/docs/whatsapp/quickstart/python
TWILIO_ACCOUNT_SID = "XXX"
TWILIO_AUTH_TOKEN = "XXX"
TWILIO_FROM = "XXX"  # eg. 'whatsapp:+14155238886' see above documentation
TWILIO_TO = "XXX"  # eg. 'whatsapp:<YOUR NUMBER>'


FORMAT = "%(asctime)s %(message)s"

logging.basicConfig(format=FORMAT)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def main():
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    twilio_client = twilio.rest.Client(account_sid, auth_token)

    urls = [
        # ("https://www.wessexmill.co.uk/acatalog/Bread_Flour.html", ["we have suspended our online shop"]),
        # ("https://www.wessexmill.co.uk/acatalog/Strong-White-Bread-Flour-1.5kg-X002S.html", ["Apologies we are offline"]),
        # ("https://www.shipton-mill.com/flour-direct-shop/flour/organic-flour", ["Our shop is temporarily closed"]),
        # ("https://www.shipton-mill.com/queue", ["we don't have any delivery slots"]),
        # ("https://flour.co.uk/view/strong-organic-white", ["CURRENTLY CLOSED"]),
        # ("https://www.souschef.co.uk/products/bacheldre-organic-stoneground-rye-flour", ["Out of stock"]),
        # ("https://www.souschef.co.uk/products/bacheldre-organic-stoneground-unbleached-strong-white-flour", ["Out of stock"]),
        # ("https://www.souschef.co.uk/products/bacheldre-organic-stoneground-strong-wholemeal-flour", ["Out of stock"]),
        # ("https://www.lakeland.co.uk/32564/24-5cm-Oval-Dough-Proving-Basket", ["Currently not available"]),
        # https://www.dovesfarm.co.uk/products/organic-flour", ["SHOP CLOSED FOR TODAY", "SHOP CLOSED TEMPORARILY"])
        # ("https://www.chilternseeds.co.uk/", ["not accepting orders at the moment"]),
        (
            "https://www.aldi.co.uk/gardenline-hanging-egg-chair/p/804050451817800",
            ["Coming soon"],
        )
    ]

    suspended = {url: (True, True) for url, _ in urls}

    while True:
        for url, patterns in urls:
            try:
                resp = requests.get(url)
                resp.raise_for_status()
                suspended[url] = (
                    any(pattern in resp.text for pattern in patterns),
                    suspended[url][0],
                )
            except requests.RequestException:
                pass

        logger.info("❤")

        for url, _ in urls:
            is_suspended, was_suspended = suspended[url]
            if was_suspended and not is_suspended:
                # winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
                twilio_client.messages.create(
                    from_=TWILIO_FROM,
                    body=f"Your flour code is {url}",  # https://www.twilio.com/docs/whatsapp/tutorial/send-whatsapp-notification-messages-templates
                    to=TWILIO_TO,
                )
                logger.info(f"{url}")

        time.sleep(60)


if __name__ == "__main__":
    main()
