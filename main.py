from bittrex import bittrex
from tkinter import *
import datetime
import webbrowser

btx2 = bittrex.Bittrex(None, None, api_version=bittrex.API_V2_0)


def market_market(market):
    """Opens the order page of the specified market.

    Args:
            market: An unfiltered string containing the market and its price change. i.e. 16% BTC-NXT
    """
    market = market.split()[1]
    webbrowser.open(
        "https://bittrex.com/Market/Index?MarketName={}".format(market), new=0)


def update_candidate_markets(listbox, date_label, time_label):
    """Finds candidate markets (markets with 10% or greater daily price change).

    Args:
            listbox: The list to store the candidate markets.
            date_label: The date of this procedure's latest execution. 
            time_label: The time of this procedure's latest execution.
    """
    listbox.delete(0, END)

    result = btx2.get_market_summaries()

    candidate_markets = []

    if result["success"]:
        for market in result["result"]:

            change_24h = (market["Summary"]["Last"] - market["Summary"]
                          ["PrevDay"]) / market["Summary"]["PrevDay"]

            if change_24h >= 0.1:
                listbox.insert(END, ("{}%  {}").format(
                    round(change_24h * 100, 1), market["Summary"]["MarketName"]))

        dt = datetime.datetime.utcnow()

        date_label["text"] = dt.strftime("%b %d, %Y")
        time_label["text"] = dt.strftime("%H:%M:%S %p")


def init_gui():

    root = Tk()
    root.resizable(width=False, height=False)
    root.title("Bittrex Pump n' Dump Finder")

    listbox = Listbox(root, height=15)
    listbox.grid(row=0, column=1, rowspan=5)

    scrollbar = Scrollbar(root, orient=VERTICAL)
    listbox["yscrollcommand"] = scrollbar.set
    scrollbar["command"] = listbox.yview
    scrollbar.grid(row=0, column=1, rowspan=5, sticky="ns" + E)

    label = Label(root, text="Last Update (UTC):")
    label.grid(row=2, column=0, padx=(5, 0), pady=(50, 0), sticky=W)

    date_label = Label(root)
    date_label.grid(row=3, column=0, padx=(5, 0), sticky=W)

    time_label = Label(root)
    time_label.grid(row=4, column=0, padx=(5, 0), sticky=W)

    market_button = Button(root, text="Market", bg="red", fg="white",
                          width=10, command=lambda: market_market(listbox.get(ACTIVE)))
    market_button.grid(row=0, column=0, padx=(15, 15), pady=(50, 0))

    refresh_button = Button(root, text="Refresh", bg="blue", fg="white", width=10,
                            command=lambda: update_candidate_markets(listbox, date_label, time_label))
    refresh_button.grid(row=1, column=0, pady=(5, 0))

    update_candidate_markets(listbox, date_label, time_label)

    root.mainloop()


init_gui()
