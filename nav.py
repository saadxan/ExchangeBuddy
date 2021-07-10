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
    explore_query = ExploreQuery(sector, country, marketcap)
    config.stk.insertWidget(1, explore_query)
    config.stk.setCurrentIndex(1)
    if len(config.stk.widget(1).layout().itemAt(1).widget().results) == 0:
        suspend_query()


def return_home():
    cur_index = config.stk.indexOf(config.stk.currentWidget())

    config.stk.removeWidget(config.stk.widget(cur_index))
    config.stk.widget(0).centralWidget().h_box.itemAt(1).widget().click()
    config.stk.setCurrentIndex(cur_index-1)


def suspend_query():
    config.stk.removeWidget(config.stk.widget(1))
    config.stk.setCurrentIndex(0)

