from market.market import Market
import time
import traceback
import pendulum
from service.base_service import add_ohlcv_records


def add_ohlcv(m, symbols, tf):
    print('add_ohlcv')
    # 分钟
    step = 1000
    time_z = 'Asia/Shanghai'
    # k线类型
    # tf = '1m'
    start = pendulum.datetime(2017, 1, 1, tzinfo=time_z)
    # end = pendulum.datetime(2018, 8, 22, tzinfo='Asia/Shanghai')
    start_timestamp = start.int_timestamp
    end_timestamp = pendulum.today(time_z).subtract(days=60).int_timestamp
    # print(start_timestamp, end_timestamp)

    # symbols = ['EOS/USDT', 'ETH/USDT']
    i = 0
    for symbol in symbols:
        for x in range(end_timestamp, start_timestamp, -step * 60):
            try:
                i += 1
                time_m = (x - step * 60) * 1000
                print(i, symbol, time_m, pendulum.from_timestamp(time_m / 1000, time_z).to_datetime_string())
                # time_10m = pendulum.now().subtract(minutes=x - step).int_timestamp * 1000
                klines_m = m.exchange.fetch_ohlcv(symbol, tf, since=time_m, limit=step)
                t0 = klines_m[0][0]
                t1 = klines_m[-1][0]
                print(len(klines_m), pendulum.from_timestamp(t0 / 1000, time_z).to_datetime_string(),
                      pendulum.from_timestamp(t1 / 1000, time_z).to_datetime_string(), (t1 - t0) / 1000 / 60,
                      klines_m)
                if t0 > time_m:
                    print(111, '已经到最早的数据了, 跳出')
                    break
                klines_list = []
                for kl in klines_m:
                    klines_dict = dict()
                    klines_dict['e'] = m.ex_name
                    klines_dict['s'] = symbol
                    klines_dict['tf'] = tf
                    klines_dict['t'] = kl[0]
                    klines_dict['o'] = kl[1]
                    klines_dict['h'] = kl[2]
                    klines_dict['l'] = kl[3]
                    klines_dict['c'] = kl[4]
                    klines_dict['v'] = kl[5]
                    klines_list.append(klines_dict)
                # 入库
                add_ohlcv_records(klines_list)
                # 防止速度过快
                if i % 10 == 0:
                    time.sleep(1)
            except Exception as e:
                print('error', 'add_ohlcv')
                traceback.print_exc()
                time.sleep(10)


if __name__ == '__main__':
    # 交易所
    ex_names = ['binance']
    for ex_name in ex_names:
        try:
            m1 = Market(ex_name)
            print(m1.ex_name)
            # ms = self.exchange.fetch_markets()
            ms = m1.exchange.load_markets(reload=True)
            ms_count = len(ms)
            print('markets', ms_count)
            symbols = []
            for s in ms:
                base_currency = s.split('/')[0]
                quote_currency = s.split('/')[1]
                if quote_currency not in ['USDT', 'BTC', 'ETH']:
                    continue
                # print(s)
                symbols.append(s)
            add_ohlcv(m1, symbols, '1m')
        except Exception as e:
            print('error', 'load_markets')
            time.sleep(3)
