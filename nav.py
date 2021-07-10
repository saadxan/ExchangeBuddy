import config

from inquiry import *
from explore import *


def go_inquiry(ticker, i):
    bad_ticker_message = QErrorMessage()
    try:
        config.stk.insertWidget(i, InquiryCard(ticker))
    except IndexError:
        bad_ticker_message.showMessage("Ticker {:s} does not exist.".format(ticker))
    except ConnectionError:
        bad_ticker_message.showMessage("Connection error to Internet.\nPlease Try Again.".format(ticker))
    else:
        config.stk.setCurrentIndex(i)
        return
    bad_ticker_message.exec_()


def go_explore(sector, country, marketcap):
    config.stk.insertWidget(1, ExploreQuery(sector, country, marketcap))
    config.stk.setCurrentIndex(1)


def return_home():
    cur_index = config.stk.indexOf(config.stk.currentWidget())

    config.stk.removeWidget(config.stk.widget(cur_index))
    config.stk.widget(0).centralWidget().h_box.itemAt(1).widget().click()
    config.stk.setCurrentIndex(cur_index-1)

